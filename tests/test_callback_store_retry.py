from src.webhook.callback_store import CallbackStore


def test_mark_failed_requeues_until_max_attempts(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    payload = {"update_id": 1, "callback_query": {"id": "cb1", "data": "approve:abc"}}
    store.upsert_event("k1", payload, 1, "cb1")

    claimed = store.claim_pending(limit=1)
    assert len(claimed) == 1

    store.mark_failed("k1", "boom", max_attempts=3)
    claimed_again = store.claim_pending(limit=1)
    assert len(claimed_again) == 1


def test_mark_failed_transitions_to_failed_at_limit(tmp_path):
    store = CallbackStore(str(tmp_path / "webhook.db"))
    payload = {"update_id": 1, "callback_query": {"id": "cb1", "data": "approve:abc"}}
    store.upsert_event("k2", payload, 1, "cb1")

    for _ in range(3):
        _ = store.claim_pending(limit=1)
        store.mark_failed("k2", "boom", max_attempts=3)

    assert store.claim_pending(limit=1) == []
