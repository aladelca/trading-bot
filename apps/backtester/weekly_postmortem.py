from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from apps.backtester.report import generate_kpi_report
from src.agents.drift import detect_metric_drift, rollback_recommendation
from src.agents.review_learning import generate_learning_recommendations


def generate_weekly_postmortem(
    audit_db: str = "data/audit.db",
    portfolio_db: str = "data/portfolio.db",
    baseline: dict | None = None,
    out_dir: str = "apps/backtester/reports",
) -> str:
    baseline = baseline or {}
    kpi = generate_kpi_report(db_path=audit_db, portfolio_db_path=portfolio_db)
    recs = generate_learning_recommendations(kpi)
    drift_alerts = detect_metric_drift(kpi, baseline)
    rollback = rollback_recommendation(drift_alerts)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = Path(out_dir) / f"weekly-postmortem-{ts}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Weekly Postmortem",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        "",
        "## KPI Snapshot",
        *(f"- {k}: {v}" for k, v in kpi.items()),
        "",
        "## Learning Recommendations",
        *(f"- {r}" for r in recs),
        "",
        "## Drift Alerts",
    ]

    if drift_alerts:
        lines.extend(f"- {a}" for a in drift_alerts)
    else:
        lines.append("- None")

    lines.extend(["", "## Rollback Recommendation", f"- {rollback}", ""])
    out_path.write_text("\n".join(lines))
    return str(out_path)


if __name__ == "__main__":
    print(generate_weekly_postmortem())
