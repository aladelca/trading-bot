import pytest

from src.execution.guardrails import LiveExecutionBlocked, assert_live_execution_allowed


def test_live_execution_blocked_by_default(monkeypatch):
    monkeypatch.delenv("LIVE_TRADING_ENABLED", raising=False)
    monkeypatch.delenv("LIVE_TRADING_CONFIRM", raising=False)
    with pytest.raises(LiveExecutionBlocked):
        assert_live_execution_allowed()


def test_live_execution_allowed_with_explicit_flags(monkeypatch):
    monkeypatch.setenv("LIVE_TRADING_ENABLED", "true")
    monkeypatch.setenv("LIVE_TRADING_CONFIRM", "I_UNDERSTAND_LIVE_TRADING_RISK")
    assert_live_execution_allowed()
