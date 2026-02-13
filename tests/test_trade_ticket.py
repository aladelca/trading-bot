from src.broker.base import OrderRequest
from src.execution.trade_ticket import build_trade_ticket


def test_build_trade_ticket():
    ticket = build_trade_ticket(
        OrderRequest("xeqt", "BUY", 5, order_type="limit", extended_hours=True),
        strategy_id="strat-1",
        rationale="mean reversion entry",
    )
    assert ticket["kind"] == "manual_trade_ticket"
    assert ticket["symbol"] == "XEQT"
    assert ticket["side"] == "buy"
    assert ticket["execution_mode"] == "manual_in_questrade"
