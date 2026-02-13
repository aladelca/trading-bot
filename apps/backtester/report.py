from __future__ import annotations

import json
import sqlite3

from src.portfolio.pnl import compute_positions_and_pnl


def _ledger_metrics(portfolio_db_path: str) -> dict:
    conn = sqlite3.connect(portfolio_db_path)
    try:
        row = conn.execute("SELECT COUNT(*), COALESCE(SUM(quantity * price), 0) FROM trades").fetchone()
    except sqlite3.OperationalError:
        return {"trades_total": 0, "notional_total": 0.0}
    if not row:
        return {"trades_total": 0, "notional_total": 0.0}
    return {"trades_total": int(row[0]), "notional_total": round(float(row[1]), 4)}


def generate_kpi_report(db_path: str = "data/audit.db", portfolio_db_path: str = "data/portfolio.db") -> dict:
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT kind, payload_json FROM events ORDER BY id ASC").fetchall()

    approvals = 0
    approved = 0
    fills = 0
    rejected = 0

    for kind, payload_json in rows:
        payload = json.loads(payload_json)
        if kind == "approval":
            approvals += 1
            if payload.get("approved"):
                approved += 1
        elif kind == "fill":
            fills += 1
        elif kind == "signal_rejected":
            rejected += 1

    approval_rate = (approved / approvals) if approvals else 0.0
    ledger = _ledger_metrics(portfolio_db_path)
    pnl = compute_positions_and_pnl(db_path=portfolio_db_path)

    return {
        "events_total": len(rows),
        "approvals_total": approvals,
        "approvals_yes": approved,
        "approval_rate": round(approval_rate, 4),
        "fills_total": fills,
        "signals_rejected": rejected,
        "ledger_trades_total": ledger["trades_total"],
        "ledger_notional_total": ledger["notional_total"],
        "realized_pnl_total": pnl["realized_pnl_total"],
        "unrealized_pnl_total": pnl["unrealized_pnl_total"],
        "equity_pnl_total": pnl["equity_pnl_total"],
    }


if __name__ == "__main__":
    print(generate_kpi_report())
