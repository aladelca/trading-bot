from __future__ import annotations

from src.portfolio.pnl import compute_positions_and_pnl
from src.portfolio.snapshots import save_snapshot


def generate_pnl_report(db_path: str = "data/portfolio.db", mark_prices: dict[str, float] | None = None) -> dict:
    report = compute_positions_and_pnl(db_path=db_path, mark_prices=mark_prices)
    save_snapshot(report, db_path=db_path)
    return report


if __name__ == "__main__":
    print(generate_pnl_report())
