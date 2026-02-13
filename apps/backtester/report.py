from __future__ import annotations

import json
import sqlite3


def generate_kpi_report(db_path: str = "data/audit.db") -> dict:
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

    return {
        "events_total": len(rows),
        "approvals_total": approvals,
        "approvals_yes": approved,
        "approval_rate": round(approval_rate, 4),
        "fills_total": fills,
        "signals_rejected": rejected,
    }


if __name__ == "__main__":
    print(generate_kpi_report())
