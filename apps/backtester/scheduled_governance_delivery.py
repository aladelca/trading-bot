from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from apps.backtester.weekly_governance_calibration import generate_weekly_governance_calibration_report


def run_scheduled_governance_delivery(
    replay_pack_path: str = "data/replay_packs/governance-sample.json",
    audit_db: str = "data/audit.db",
    portfolio_db: str = "data/portfolio.db",
    out_dir: str = "apps/backtester/reports",
    delivery_dir: str = "apps/backtester/reports/delivery",
) -> str:
    report_path = generate_weekly_governance_calibration_report(
        replay_pack_path=replay_pack_path,
        audit_db=audit_db,
        portfolio_db=portfolio_db,
        out_dir=out_dir,
    )

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    manifest_path = Path(delivery_dir) / f"governance-delivery-{ts}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "kind": "weekly_governance_calibration_delivery",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "report_path": report_path,
        "channel": os.getenv("GOV_DELIVERY_CHANNEL", "telegram"),
        "target": os.getenv("GOV_DELIVERY_TARGET", ""),
        "summary": "Weekly governance calibration report generated",
        "status": "ready-for-delivery",
    }

    manifest_path.write_text(json.dumps(payload, sort_keys=True, indent=2))
    return str(manifest_path)


if __name__ == "__main__":
    print(run_scheduled_governance_delivery())
