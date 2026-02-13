from __future__ import annotations

import os
from dataclasses import asdict

import requests

from src.broker.base import BrokerClient, OrderRequest
from src.broker.questrade.auth import QuestradeToken, refresh_access_token
from src.execution.errors import classify_broker_error
from src.execution.idempotency import build_order_idempotency_key
from src.execution.retry import RetryPolicy, with_retry
from src.execution.validation import validate_order_matrix
from src.execution.validation_rollout import resolve_validation_mode


class QuestradeClient(BrokerClient):
    """Questrade adapter with token refresh + account helpers."""

    def __init__(self, client_id: str = "", refresh_token: str = "", practice: bool = True):
        self.client_id = client_id
        self.refresh_token = refresh_token
        self.practice = practice
        self.token: QuestradeToken | None = None

    def ensure_token(self) -> QuestradeToken | None:
        if not self.refresh_token:
            return None
        self.token = refresh_access_token(self.refresh_token)
        return self.token

    def _headers(self) -> dict:
        token = self.token or self.ensure_token()
        if not token:
            return {}
        return {"Authorization": f"Bearer {token.access_token}"}

    def get_accounts(self) -> list[dict]:
        token = self.token or self.ensure_token()
        if not token:
            return []
        response = requests.get(f"{token.api_server}v1/accounts", headers=self._headers(), timeout=15)
        response.raise_for_status()
        return response.json().get("accounts", [])

    def get_buying_power(self) -> float:
        token = self.token or self.ensure_token()
        if not token:
            return 10000.0
        accounts = self.get_accounts()
        if not accounts:
            return 0.0
        account_id = accounts[0].get("number")
        response = requests.get(
            f"{token.api_server}v1/accounts/{account_id}/balances",
            headers=self._headers(),
            timeout=15,
        )
        response.raise_for_status()
        per_currency = response.json().get("perCurrencyBalances", [])
        for row in per_currency:
            if row.get("currency") in {"CAD", "USD"}:
                return float(row.get("buyingPower", 0.0))
        return 0.0

    def resolve_symbol_id(self, symbol: str) -> int | None:
        token = self.token or self.ensure_token()
        if not token:
            return None

        response = requests.get(
            f"{token.api_server}v1/symbols/search",
            headers=self._headers(),
            params={"prefix": symbol},
            timeout=15,
        )
        response.raise_for_status()
        symbols = response.json().get("symbols", [])

        exact = next((s for s in symbols if str(s.get("symbol", "")).upper() == symbol.upper()), None)
        if exact and exact.get("symbolId") is not None:
            return int(exact["symbolId"])

        if symbols and symbols[0].get("symbolId") is not None:
            return int(symbols[0]["symbolId"])

        return None

    def build_order_payload(self, account_id: str, order: OrderRequest, symbol_id: int) -> dict:
        return {
            "accountNumber": account_id,
            "symbolId": symbol_id,
            "quantity": order.quantity,
            "isAllOrNone": False,
            "isAnonymous": False,
            "orderType": order.order_type.upper(),
            "action": "Buy" if order.side.lower() == "buy" else "Sell",
            "timeInForce": "Day",
            "primaryRoute": "AUTO",
            "secondaryRoute": "AUTO",
        }

    def _submit_once(self, token: QuestradeToken, account_id: str, payload: dict, idem_key: str) -> dict:
        try:
            response = requests.post(
                f"{token.api_server}v1/accounts/{account_id}/orders",
                headers={**self._headers(), "X-Client-Request-Id": idem_key},
                json=payload,
                timeout=15,
            )
            if response.status_code >= 400:
                info = classify_broker_error(response.status_code, response.text)
                return {
                    "status": "error",
                    "broker": "questrade",
                    "error_category": info.category,
                    "reason": info.reason,
                    "http_status": response.status_code,
                    "rejection_source": "broker_api",
                    "telemetry": {
                        "phase": "submit",
                        "category": info.category,
                        "http_status": response.status_code,
                    },
                }
            return {"status": "submitted", "broker": "questrade", "response": response.json()}
        except requests.RequestException as exc:
            info = classify_broker_error(503, str(exc))
            return {
                "status": "error",
                "broker": "questrade",
                "error_category": info.category,
                "reason": info.reason,
                "message": str(exc),
                "rejection_source": "broker_transport",
                "telemetry": {
                    "phase": "submit",
                    "category": info.category,
                    "http_status": 503,
                },
            }

    def submit_order(self, order: OrderRequest, dry_run: bool = True, request_id: str = "") -> dict:
        validation = validate_order_matrix(order, broker="questrade")
        rollout = resolve_validation_mode(
            configured_mode=os.getenv("BROKER_VALIDATION_MODE", "enforce"),
            report_only_since_utc=os.getenv("BROKER_VALIDATION_REPORT_ONLY_SINCE_UTC", ""),
            report_only_max_minutes=int(os.getenv("BROKER_VALIDATION_REPORT_ONLY_MAX_MINUTES", "0")),
            auto_revert_enabled=os.getenv("BROKER_VALIDATION_AUTO_REVERT", "true").lower() in {"1", "true", "yes", "on"},
        )
        validation_mode = rollout["effective_mode"]

        validation_warning = None
        if not validation.ok:
            if validation_mode == "report_only":
                validation_warning = {
                    "reason": validation.reason,
                    "rejection_source": "pre_trade_validation",
                    "validation_mode": validation_mode,
                    "rollout": rollout,
                }
            else:
                return {
                    "status": "blocked",
                    "reason": validation.reason,
                    "broker": "questrade",
                    "rejection_source": "pre_trade_validation",
                    "validation_mode": validation_mode,
                    "rollout": rollout,
                }

        if dry_run:
            out = {"status": "dry-run", "broker": "questrade", **asdict(order)}
            if validation_warning:
                out["validation_warning"] = validation_warning
            return out

        token = self.token or self.ensure_token()
        if not token:
            return {"status": "blocked", "reason": "missing_token", "broker": "questrade"}

        accounts = self.get_accounts()
        if not accounts:
            return {"status": "blocked", "reason": "missing_account", "broker": "questrade"}

        symbol_id = self.resolve_symbol_id(order.symbol)
        if symbol_id is None:
            return {"status": "blocked", "reason": "missing_symbol_id", "broker": "questrade"}

        account_id = str(accounts[0].get("number"))
        payload = self.build_order_payload(account_id, order, symbol_id)
        idem_key = build_order_idempotency_key(order, request_id=request_id or "no-request-id")

        policy = RetryPolicy(max_attempts=3, base_delay_seconds=0.2, backoff_multiplier=2.0)
        result = with_retry(
            lambda: self._submit_once(token, account_id, payload, idem_key),
            should_retry=lambda r: r.get("status") == "error" and r.get("error_category") == "retryable",
            policy=policy,
        )
        result["idempotency_key"] = idem_key
        if validation_warning:
            result["validation_warning"] = validation_warning
        return result

    def place_order(self, order: OrderRequest) -> dict:
        return {"status": "paper-simulated", "broker": "questrade", **asdict(order)}
