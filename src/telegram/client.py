from __future__ import annotations

import time
from dataclasses import dataclass

import requests


@dataclass
class TelegramConfig:
    bot_token: str
    chat_id: str


class TelegramClient:
    def __init__(self, config: TelegramConfig, timeout_seconds: int = 20):
        self.config = config
        self.timeout_seconds = timeout_seconds
        self.base_url = f"https://api.telegram.org/bot{config.bot_token}"

    def send_approval_request(self, text: str, request_id: str) -> int:
        payload = {
            "chat_id": self.config.chat_id,
            "text": text,
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "✅ Approve", "callback_data": f"approve:{request_id}"},
                        {"text": "❌ Reject", "callback_data": f"reject:{request_id}"},
                    ]
                ]
            },
        }
        response = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return int(data["result"]["message_id"])

    def wait_for_decision(self, request_id: str, start_offset: int = 0) -> bool | None:
        deadline = time.time() + self.timeout_seconds
        offset = start_offset

        while time.time() < deadline:
            response = requests.get(
                f"{self.base_url}/getUpdates",
                params={"timeout": 5, "offset": offset + 1},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            for update in data.get("result", []):
                offset = max(offset, int(update.get("update_id", 0)))
                cb = update.get("callback_query")
                if not cb:
                    continue
                callback_data = cb.get("data", "")
                decision = parse_callback_decision(callback_data, request_id)
                if decision is not None:
                    return decision
            time.sleep(0.2)
        return None


def parse_callback_decision(callback_data: str, request_id: str) -> bool | None:
    if callback_data == f"approve:{request_id}":
        return True
    if callback_data == f"reject:{request_id}":
        return False
    return None
