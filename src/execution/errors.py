from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BrokerErrorInfo:
    category: str  # retryable|fatal|blocked
    reason: str


def classify_broker_error(status_code: int, message: str = "") -> BrokerErrorInfo:
    msg = message.lower()

    if status_code in {408, 429, 500, 502, 503, 504}:
        return BrokerErrorInfo(category="retryable", reason=f"http_{status_code}")

    if status_code in {401, 403}:
        return BrokerErrorInfo(category="blocked", reason=f"auth_{status_code}")

    if status_code in {400, 404, 422}:
        # Could be invalid payload/symbol/account
        return BrokerErrorInfo(category="fatal", reason=f"request_{status_code}")

    if "timeout" in msg or "temporarily unavailable" in msg:
        return BrokerErrorInfo(category="retryable", reason="message_retryable")

    return BrokerErrorInfo(category="fatal", reason="unknown")
