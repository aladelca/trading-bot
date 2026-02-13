from src.broker.base import OrderRequest
from src.execution.validation import validate_order_matrix


def test_validation_accepts_market_regular_or_extended():
    ok = validate_order_matrix(OrderRequest("SPY", "buy", 1, order_type="market", extended_hours=True))
    assert ok.ok is True


def test_validation_rejects_stop_in_extended_hours():
    bad = validate_order_matrix(OrderRequest("SPY", "buy", 1, order_type="stop", extended_hours=True))
    assert bad.ok is False
    assert bad.reason == "stop_not_allowed_in_extended_hours"


def test_validation_rejects_invalid_quantity():
    bad = validate_order_matrix(OrderRequest("SPY", "buy", 0, order_type="market", extended_hours=False))
    assert bad.ok is False
    assert bad.reason == "invalid_quantity"
