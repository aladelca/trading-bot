from src.webhook.callback_store import CallbackStore
from src.webhook.telegram_processor import process_telegram_update


def test_process_update_and_ignore_duplicate(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    update = {"update_id": 99, "callback_query": {"id": "cb-99", "data": "approve:req123"}}

    first = process_telegram_update(update, store)
    second = process_telegram_update(update, store)

    assert first["status"] == "processed"
    assert first["decision"] is True
    assert second["status"] == "duplicate"


def test_process_update_ignores_invalid_data(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    update = {"update_id": 1, "callback_query": {"id": "cb-1", "data": "invalid-data"}}
    out = process_telegram_update(update, store)
    assert out["status"] == "ignored"
