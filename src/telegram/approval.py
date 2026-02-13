from __future__ import annotations

import os
from dataclasses import asdict
from uuid import uuid4

from src.agents.automation_policy import choose_auto_approve_tier, tier_allows_auto_approve
from src.signals.models import TradeSignal
from src.telegram.client import TelegramClient, TelegramConfig


class ApprovalGate:
    """Approval gate with Telegram integration fallback + optional controlled automation."""

    def __init__(self, required: bool = True, timeout_seconds: int = 20):
        self.required = required
        self.timeout_seconds = timeout_seconds
        self.last_offset = 0
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.client = TelegramClient(TelegramConfig(token, chat_id), timeout_seconds) if token and chat_id else None

    def _policy_auto_approve(self, signal: TradeSignal, request_id: str) -> tuple[bool, str, str] | None:
        enabled = os.getenv("AUTO_APPROVE_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
        if not enabled:
            return None

        symbols_raw = os.getenv("AUTO_APPROVE_SYMBOLS", "")
        symbols = {s.strip().upper() for s in symbols_raw.split(",") if s.strip()}
        tier = choose_auto_approve_tier(signal.confidence)
        allowed_tiers_raw = os.getenv("AUTO_APPROVE_ALLOWED_TIERS", "tier-1,tier-2")
        allowed_tiers = {t.strip().lower() for t in allowed_tiers_raw.split(",") if t.strip()}

        min_conf = float(os.getenv("AUTO_APPROVE_MIN_CONFIDENCE", "0.0"))
        if signal.confidence < min_conf:
            return None
        if not tier_allows_auto_approve(tier, signal.symbol, symbols, allowed_tiers=allowed_tiers):
            return None

        return True, f"policy-auto:{tier}", request_id

    def request_with_meta(self, signal: TradeSignal) -> tuple[bool, str, str]:
        if not self.required:
            return True, "bypass", ""

        request_id = uuid4().hex[:10]

        policy_decision = self._policy_auto_approve(signal, request_id)
        if policy_decision is not None:
            return policy_decision

        payload = asdict(signal)

        if not self.client:
            print("APPROVAL_REQUEST_FALLBACK", payload)
            return False, "fallback", request_id

        text = (
            f"Trade approval needed\n"
            f"Symbol: {signal.symbol}\n"
            f"Side: {signal.side}\n"
            f"Entry: {signal.entry}\n"
            f"Stop: {signal.stop}\n"
            f"TP: {signal.take_profit}\n"
            f"Confidence: {signal.confidence:.2f}\n"
            f"ID: {request_id}"
        )
        self.client.send_approval_request(text=text, request_id=request_id)
        decision, new_offset = self.client.wait_for_decision(request_id, start_offset=self.last_offset)
        self.last_offset = new_offset
        return bool(decision), "telegram", request_id

    def request(self, signal: TradeSignal) -> bool:
        decision, _source, _id = self.request_with_meta(signal)
        return decision
