from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient


def test_submit_order_blocked_by_validation_before_network():
    q = QuestradeClient(refresh_token="x")
    out = q.submit_order(OrderRequest("SPY", "buy", 1, order_type="stop", extended_hours=True), dry_run=False)
    assert out["status"] == "blocked"
    assert out["reason"] == "stop_not_allowed_in_extended_hours"
    assert out["rejection_source"] == "pre_trade_validation"


def test_submit_order_blocked_by_questrade_extended_hours_qty_cap_before_network():
    q = QuestradeClient(refresh_token="x")
    out = q.submit_order(OrderRequest("SPY", "buy", 6000, order_type="market", extended_hours=True), dry_run=False)
    assert out["status"] == "blocked"
    assert out["reason"] == "extended_hours_quantity_exceeds_questrade_cap"


def test_submit_order_report_only_mode_does_not_block(monkeypatch):
    monkeypatch.setenv("BROKER_VALIDATION_MODE", "report_only")
    q = QuestradeClient(refresh_token="x")
    out = q.submit_order(OrderRequest("SPY", "buy", 1, order_type="stop", extended_hours=True), dry_run=True)
    assert out["status"] == "dry-run"
    assert out["validation_warning"]["reason"] == "stop_not_allowed_in_extended_hours"
