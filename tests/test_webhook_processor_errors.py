from src.webhook.callback_store import CallbackStore
from src.webhook.telegram_processor import enqueue_telegram_update, process_pending_once


def test_processor_handles_malformed_callback_query_as_ignored(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    update = {"update_id": 7, "callback_query": "bad"}
    enqueue_telegram_update(update, store)

    out = process_pending_once(store, limit=10)
    assert out[0]["status"] == "ignored"

    # no pending events left
    claimed = store.claim_pending(limit=10)
    assert claimed == []
