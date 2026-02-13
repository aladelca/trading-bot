from __future__ import annotations

import json
from pathlib import Path

from apps.telegram_webhook.evidence_alert_routing import build_evidence_manifest, build_incident_alert_manifest
from apps.telegram_webhook.incident_report import generate_webhook_incident_report


def run_evidence_alert_pipeline(
    webhook_db: str = "data/webhook.db",
    evidence_dir: str = "/tmp/webhook-evidence",
    out_dir: str = "apps/telegram_webhook/reports/delivery",
) -> dict:
    incident = generate_webhook_incident_report(db_path=webhook_db)
    evidence_manifest = build_evidence_manifest(evidence_dir=evidence_dir, out_dir=out_dir)
    alert_manifest = build_incident_alert_manifest(incident_report_path=incident, out_dir=out_dir)

    summary = {
        "incident_report": incident,
        "evidence_manifest": evidence_manifest,
        "alert_manifest": alert_manifest,
    }
    summary_path = Path(out_dir) / "webhook-evidence-alert-latest.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, sort_keys=True, indent=2))
    summary["summary_path"] = str(summary_path)
    return summary


if __name__ == "__main__":
    print(json.dumps(run_evidence_alert_pipeline()))
