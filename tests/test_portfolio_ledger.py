from src.portfolio.ledger import PortfolioLedger


def test_portfolio_ledger_records_and_reports(tmp_path):
    ledger = PortfolioLedger(str(tmp_path / "portfolio.db"))
    ledger.record_trade("SPY", "buy", 2, 100.0, "filled", "paper")
    ledger.record_trade("QQQ", "sell", 1, 200.0, "dry-run", "live")

    m = ledger.metrics()
    assert m["trades_total"] == 2
    assert m["trades_buy"] == 1
    assert m["trades_sell"] == 1
    assert m["notional_total"] == 400.0
