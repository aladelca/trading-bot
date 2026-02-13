from src.signals.models import TradeSignal
from src.telegram import approval as approval_module


class DummyTelegramClient:
    def __init__(self, *_args, **_kwargs):
        self.ids = []

    def send_approval_request(self, text: str, request_id: str) -> int:
        self.ids.append(request_id)
        return 1

    def wait_for_decision(self, request_id: str, start_offset: int = 0):
        return True, start_offset


def test_request_id_is_unique_per_call(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "x")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "y")
    monkeypatch.setattr(approval_module, "TelegramClient", DummyTelegramClient)

    gate = approval_module.ApprovalGate(required=True)
    s = TradeSignal("SPY", "buy", 0.9, 500, 495, 510, "test")

    gate.request(s)
    gate.request(s)

    assert len(gate.client.ids) == 2
    assert gate.client.ids[0] != gate.client.ids[1]
