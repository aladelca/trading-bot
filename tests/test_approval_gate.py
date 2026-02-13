from src.signals.models import TradeSignal
from src.telegram.approval import ApprovalGate


def test_approval_gate_bypass_when_not_required():
    gate = ApprovalGate(required=False)
    signal = TradeSignal("SPY", "buy", 0.9, 500, 495, 510, "test")
    assert gate.request(signal) is True
