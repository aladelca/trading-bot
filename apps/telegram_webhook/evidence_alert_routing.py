from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def build_evidence_manifest(evidence_dir: str, out_dir: str) -> str:
    base = Path(evidence_dir)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    files = []
    if base.exists():
        for p in sorted(base.rglob("*")):
            if p.is_file():
                files.append({"path": str(p), "size_bytes": p.stat().st_size})

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = out / f"webhook-evidence-manifest-{ts}.json"
    payload = {
        "kind": "webhook_evidence_manifest",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_dir": str(base),
        "file_count": len(files),
        "files": files,
    }
    out_path.write_text(json.dumps(payload, sort_keys=True, indent=2))
    return str(out_path)


def build_incident_alert_manifest(incident_report_path: str, out_dir: str) -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = out / f"webhook-incident-alert-{ts}.json"

    payload = {
        "kind": "webhook_incident_alert",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "channel": os.getenv("WEBHOOK_ALERT_CHANNEL", "telegram"),
        "target": os.getenv("WEBHOOK_ALERT_TARGET", ""),
        "severity": os.getenv("WEBHOOK_ALERT_SEVERITY", "high"),
        "incident_report_path": incident_report_path,
        "status": "ready-for-routing",
        "dry_run": os.getenv("WEBHOOK_ALERT_DRY_RUN", "true").lower() in {"1", "true", "yes", "on"},
    }
    out_path.write_text(json.dumps(payload, sort_keys=True, indent=2))
    return str(out_path)
