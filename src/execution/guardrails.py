from __future__ import annotations

import os


class LiveExecutionBlocked(Exception):
    pass


def assert_live_execution_allowed() -> None:
    enabled = os.getenv("LIVE_TRADING_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
    confirm = os.getenv("LIVE_TRADING_CONFIRM", "")

    if not enabled:
        raise LiveExecutionBlocked("LIVE_TRADING_ENABLED is false")

    if confirm != "I_UNDERSTAND_LIVE_TRADING_RISK":
        raise LiveExecutionBlocked("LIVE_TRADING_CONFIRM missing or invalid")
