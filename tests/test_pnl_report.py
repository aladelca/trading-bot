from apps.backtester.pnl_report import generate_pnl_report
from src.portfolio.ledger import PortfolioLedger


def test_generate_pnl_report(tmp_path):
    db = str(tmp_path / "portfolio.db")
    ledger = PortfolioLedger(db)
    ledger.record_trade("QQQ", "buy", 2, 200.0, "filled", "paper")

    report = generate_pnl_report(db_path=db, mark_prices={"QQQ": 210.0})
    assert report["realized_pnl_total"] == 0.0
    assert report["unrealized_pnl_total"] == 20.0
