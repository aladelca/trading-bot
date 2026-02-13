from src.signals.models import TradeSignal
from src.telegram.approval import ApprovalGate


def test_approval_gate_bypass_when_not_required():
    gate = ApprovalGate(required=False)
    signal = TradeSignal("SPY", "buy", 0.9, 500, 495, 510, "test")
    assert gate.request(signal) is True


def test_approval_gate_fails_closed_without_telegram(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    gate = ApprovalGate(required=True)
    signal = TradeSignal("SPY", "buy", 0.9, 500, 495, 510, "test")
    assert gate.request(signal) is False
