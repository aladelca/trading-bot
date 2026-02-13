from __future__ import annotations

import json
import os

from src.portfolio.pnl import compute_positions_and_pnl
from src.portfolio.snapshots import save_snapshot


def generate_pnl_report(
    db_path: str = "data/portfolio.db",
    mark_prices: dict[str, float] | None = None,
    fx_rates: dict[str, float] | None = None,
    base_currency: str = "USD",
) -> dict:
    report = compute_positions_and_pnl(
        db_path=db_path,
        mark_prices=mark_prices,
        fx_rates=fx_rates,
        base_currency=base_currency,
    )
    save_snapshot(report, db_path=db_path)
    return report


if __name__ == "__main__":
    fx_json = os.getenv("FX_RATES_JSON", "{}")
    try:
        fx_rates = json.loads(fx_json)
    except json.JSONDecodeError:
        fx_rates = {}

    print(
        generate_pnl_report(
            db_path=os.getenv("PORTFOLIO_DB_PATH", "data/portfolio.db"),
            fx_rates=fx_rates,
            base_currency=os.getenv("BASE_CURRENCY", "USD"),
        )
    )
