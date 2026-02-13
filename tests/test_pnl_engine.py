from src.portfolio.ledger import PortfolioLedger
from src.portfolio.pnl import compute_positions_and_pnl


def test_pnl_realized_and_unrealized(tmp_path):
    db = str(tmp_path / "portfolio.db")
    ledger = PortfolioLedger(db)

    # long 10 @100, sell 4 @110 => realized +40, remaining 6 @100
    ledger.record_trade("SPY", "buy", 10, 100.0, "filled", "paper")
    ledger.record_trade("SPY", "sell", 4, 110.0, "filled", "paper")

    out = compute_positions_and_pnl(db_path=db, mark_prices={"SPY": 105.0})
    sym = out["symbols"]["SPY"]

    assert sym["qty"] == 6
    assert sym["avg_cost"] == 100.0
    assert sym["realized_pnl"] == 40.0
    assert sym["unrealized_pnl"] == 30.0
    assert out["equity_pnl_total"] == 70.0
