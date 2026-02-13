import json
import sqlite3
from pathlib import Path

from apps.telegram_webhook.evidence_alert_pipeline import run_evidence_alert_pipeline


def test_evidence_alert_pipeline_outputs_manifests(tmp_path, monkeypatch):
    # prepare webhook db with no failures (still should produce report)
    db = tmp_path / "webhook.db"
    sqlite3.connect(db).close()

    evidence_root = tmp_path / "evidence"
    snap = evidence_root / "snap1"
    snap.mkdir(parents=True)
    (snap / "health-local.json").write_text('{"ok": true}')

    monkeypatch.setenv("WEBHOOK_ALERT_CHANNEL", "telegram")
    monkeypatch.setenv("WEBHOOK_ALERT_TARGET", "123")
    monkeypatch.setenv("WEBHOOK_ALERT_DRY_RUN", "true")

    out = run_evidence_alert_pipeline(
        webhook_db=str(db),
        evidence_dir=str(evidence_root),
        out_dir=str(tmp_path / "delivery"),
    )

    e = json.loads(Path(out["evidence_manifest"]).read_text())
    a = json.loads(Path(out["alert_manifest"]).read_text())

    assert e["kind"] == "webhook_evidence_manifest"
    assert e["file_count"] >= 1
    assert a["kind"] == "webhook_incident_alert"
    assert a["target"] == "123"
    assert a["status"] == "ready-for-routing"
