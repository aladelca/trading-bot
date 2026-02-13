from __future__ import annotations

from dataclasses import asdict

import requests

from src.broker.base import BrokerClient, OrderRequest
from src.broker.questrade.auth import QuestradeToken, refresh_access_token


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

    def submit_order(self, order: OrderRequest, dry_run: bool = True) -> dict:
        if dry_run:
            return {"status": "dry-run", "broker": "questrade", **asdict(order)}

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
        response = requests.post(
            f"{token.api_server}v1/accounts/{account_id}/orders",
            headers=self._headers(),
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return {"status": "submitted", "broker": "questrade", "response": response.json()}

    def place_order(self, order: OrderRequest) -> dict:
        return {"status": "paper-simulated", "broker": "questrade", **asdict(order)}
