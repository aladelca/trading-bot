from src.portfolio.ledger import PortfolioLedger
from src.portfolio.pnl import compute_positions_and_pnl


def test_multicurrency_normalization_cad_to_usd(tmp_path):
    db = str(tmp_path / "portfolio.db")
    ledger = PortfolioLedger(db)

    # CAD trade converted to USD base at fx 0.75
    ledger.record_trade("SHOP", "buy", 2, 100.0, "filled", "paper", currency="CAD")

    out = compute_positions_and_pnl(
        db_path=db,
        mark_prices={"SHOP": 110.0},
        fx_rates={"CAD": 0.75, "USD": 1.0},
        base_currency="USD",
    )
    sym = out["symbols"]["SHOP"]

    assert sym["avg_cost_base"] == 75.0
    assert sym["mark_price_base"] == 82.5
    assert sym["unrealized_pnl_base"] == 15.0
