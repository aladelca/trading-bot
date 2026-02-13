from __future__ import annotations

import argparse
import json
import os

from src.agents.governance_reconciliation import run_reconciliation
from src.storage.audit_log import AuditLogger


def main() -> None:
    p = argparse.ArgumentParser(description="Governance reconciliation cadence + stale decision cleanup")
    p.add_argument("--recommendation-id", required=True)
    p.add_argument("--cadence-days", type=int, default=7)
    p.add_argument("--stale-pending-hours", type=int, default=72)
    args = p.parse_args()

    audit = AuditLogger(os.getenv("AUDIT_DB_PATH", "data/audit.db"))
    out = run_reconciliation(
        audit,
        recommendation_id=args.recommendation_id,
        cadence_days=args.cadence_days,
        stale_pending_hours=args.stale_pending_hours,
    )
    print(json.dumps(out))


if __name__ == "__main__":
    main()
