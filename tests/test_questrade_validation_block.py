from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient


def test_submit_order_blocked_by_validation_before_network():
    q = QuestradeClient(refresh_token="x")
    out = q.submit_order(OrderRequest("SPY", "buy", 1, order_type="stop", extended_hours=True), dry_run=False)
    assert out["status"] == "blocked"
    assert out["reason"] == "stop_not_allowed_in_extended_hours"
