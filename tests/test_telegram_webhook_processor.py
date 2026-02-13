from src.webhook.callback_store import CallbackStore
from src.webhook.telegram_processor import enqueue_telegram_update, process_pending_once


def test_enqueue_then_process_and_ignore_duplicate(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    update = {"update_id": 99, "callback_query": {"id": "cb-99", "data": "approve:req123"}}

    first = enqueue_telegram_update(update, store)
    second = enqueue_telegram_update(update, store)

    assert first["status"] == "queued"
    assert second["status"] == "duplicate"

    processed = process_pending_once(store)
    assert len(processed) == 1
    assert processed[0]["status"] == "processed"
    assert processed[0]["decision"] is True


def test_process_update_ignores_invalid_data(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    update = {"update_id": 1, "callback_query": {"id": "cb-1", "data": "invalid-data"}}
    enqueue_telegram_update(update, store)
    out = process_pending_once(store)
    assert out[0]["status"] == "ignored"
