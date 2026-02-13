from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from apps.backtester.report import generate_kpi_report
from src.agents.threshold_calibration import ReplayScenario, calibrate_thresholds


def generate_weekly_governance_calibration_report(
    replay_pack_path: str = "data/replay_packs/governance-sample.json",
    audit_db: str = "data/audit.db",
    portfolio_db: str = "data/portfolio.db",
    candidates: list[float] | None = None,
    out_dir: str = "apps/backtester/reports",
) -> str:
    candidates = candidates or [0.85, 0.88, 0.90, 0.92, 0.95]
    scenarios_raw = json.loads(Path(replay_pack_path).read_text())
    scenarios = [
        ReplayScenario(
            confidence=float(x["confidence"]),
            pnl_outcome=float(x["pnl_outcome"]),
            approved=bool(x["approved"]),
        )
        for x in scenarios_raw
    ]

    calibration = calibrate_thresholds(scenarios, candidates)
    kpi = generate_kpi_report(db_path=audit_db, portfolio_db_path=portfolio_db)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = Path(out_dir) / f"weekly-governance-calibration-{ts}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    best = calibration.get("best") or {}
    lines = [
        "# Weekly Governance Calibration",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        "",
        "## KPI Snapshot",
        *(f"- {k}: {v}" for k, v in kpi.items()),
        "",
        "## Threshold Calibration Best Candidate",
        f"- threshold: {best.get('threshold')}",
        f"- score: {best.get('score')}",
        f"- selected: {best.get('selected')}",
        f"- approval_rate: {best.get('approval_rate')}",
        f"- avg_pnl: {best.get('avg_pnl')}",
        "",
        "## Full Candidate Ranking",
    ]

    for row in calibration.get("ranked", []):
        lines.append(
            f"- threshold={row['threshold']} score={row['score']} selected={row['selected']} approval_rate={row['approval_rate']} avg_pnl={row['avg_pnl']}"
        )

    out_path.write_text("\n".join(lines))
    return str(out_path)


if __name__ == "__main__":
    print(generate_weekly_governance_calibration_report())
