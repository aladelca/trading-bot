from src.webhook.callback_store import CallbackStore


def test_callback_store_upsert_idempotent(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    payload = {"update_id": 1, "callback_query": {"id": "cb1", "data": "approve:abc"}}

    first = store.upsert_event("k1", payload, 1, "cb1")
    second = store.upsert_event("k1", payload, 1, "cb1")

    assert first is True
    assert second is False

    pending = store.list_pending(limit=10)
    assert len(pending) == 1

    store.mark_processed("k1", request_id="abc", decision="approve")
    assert store.list_pending(limit=10) == []
