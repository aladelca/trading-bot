from __future__ import annotations

import os
from dataclasses import asdict
from uuid import uuid4

from src.signals.models import TradeSignal
from src.telegram.client import TelegramClient, TelegramConfig


class ApprovalGate:
    """Approval gate with Telegram integration fallback."""

    def __init__(self, required: bool = True, timeout_seconds: int = 20):
        self.required = required
        self.timeout_seconds = timeout_seconds
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.client = TelegramClient(TelegramConfig(token, chat_id), timeout_seconds) if token and chat_id else None

    def request_with_meta(self, signal: TradeSignal) -> tuple[bool, str, str]:
        if not self.required:
            return True, "bypass", ""

        request_id = uuid4().hex[:10]
        payload = asdict(signal)

        if not self.client:
            print("APPROVAL_REQUEST_FALLBACK", payload)
            return True, "fallback", request_id

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
        decision = bool(self.client.wait_for_decision(request_id))
        return decision, "telegram", request_id

    def request(self, signal: TradeSignal) -> bool:
        decision, _source, _id = self.request_with_meta(signal)
        return decision
