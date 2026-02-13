from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient


def test_submit_order_blocked_by_validation_before_network():
    q = QuestradeClient(refresh_token="x")
    out = q.submit_order(OrderRequest("SPY", "buy", 1, order_type="stop", extended_hours=True), dry_run=False)
    assert out["status"] == "blocked"
    assert out["reason"] == "stop_not_allowed_in_extended_hours"


def test_submit_order_blocked_by_questrade_extended_hours_qty_cap_before_network():
    q = QuestradeClient(refresh_token="x")
    out = q.submit_order(OrderRequest("SPY", "buy", 6000, order_type="market", extended_hours=True), dry_run=False)
    assert out["status"] == "blocked"
    assert out["reason"] == "extended_hours_quantity_exceeds_questrade_cap"
