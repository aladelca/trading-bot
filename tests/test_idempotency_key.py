from src.broker.base import OrderRequest
from src.execution.idempotency import build_order_idempotency_key


def test_idempotency_key_is_stable_for_same_input():
    o = OrderRequest("SPY", "buy", 2)
    k1 = build_order_idempotency_key(o, "req1")
    k2 = build_order_idempotency_key(o, "req1")
    assert k1 == k2


def test_idempotency_key_changes_with_request_id():
    o = OrderRequest("SPY", "buy", 2)
    k1 = build_order_idempotency_key(o, "req1")
    k2 = build_order_idempotency_key(o, "req2")
    assert k1 != k2
