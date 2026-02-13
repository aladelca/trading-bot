from src.signals.models import TradeSignal
from src.telegram.approval import ApprovalGate


def test_approval_gate_bypass_when_not_required():
    gate = ApprovalGate(required=False)
    signal = TradeSignal("SPY", "buy", 0.9, 500, 495, 510, "test")
    assert gate.request(signal) is True


def test_approval_gate_fails_closed_without_telegram(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.setenv("AUTO_APPROVE_ENABLED", "false")
    gate = ApprovalGate(required=True)
    signal = TradeSignal("SPY", "buy", 0.9, 500, 495, 510, "test")
    assert gate.request(signal) is False


def test_approval_gate_policy_auto_approve(monkeypatch):
    monkeypatch.setenv("AUTO_APPROVE_ENABLED", "true")
    monkeypatch.setenv("AUTO_APPROVE_MIN_CONFIDENCE", "0.85")
    monkeypatch.setenv("AUTO_APPROVE_SYMBOLS", "SPY,QQQ")
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    gate = ApprovalGate(required=True)
    signal = TradeSignal("SPY", "buy", 0.9, 500, 495, 510, "test")
    approved, source, _rid = gate.request_with_meta(signal)
    assert approved is True
    assert source.startswith("policy-auto:")
