from src.telegram.client import TelegramClient, TelegramConfig


def test_wait_for_decision_acknowledges_callback(monkeypatch):
    calls = {"ack": 0}

    class DummyResp:
        def __init__(self, payload):
            self._payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self._payload

    def fake_get(*_args, **_kwargs):
        return DummyResp(
            {
                "result": [
                    {
                        "update_id": 10,
                        "callback_query": {"id": "cb-1", "data": "approve:abc"},
                    }
                ]
            }
        )

    def fake_post(url, *args, **kwargs):
        if url.endswith("/answerCallbackQuery"):
            calls["ack"] += 1
        return DummyResp({"ok": True, "result": {"message_id": 1}})

    monkeypatch.setattr("src.telegram.client.requests.get", fake_get)
    monkeypatch.setattr("src.telegram.client.requests.post", fake_post)

    c = TelegramClient(TelegramConfig("t", "c"), timeout_seconds=1)
    decision, offset = c.wait_for_decision("abc", start_offset=0)
    assert decision is True
    assert offset == 10
    assert calls["ack"] == 1
