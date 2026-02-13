import json
from pathlib import Path

from apps.backtester.scheduled_governance_delivery import run_scheduled_governance_delivery
from src.storage.audit_log import AuditLogger


def test_scheduled_governance_delivery_creates_manifest(tmp_path, monkeypatch):
    pack = tmp_path / "pack.json"
    pack.write_text(
        """
        [
          {"confidence": 0.95, "pnl_outcome": 1.0, "approved": true},
          {"confidence": 0.88, "pnl_outcome": 0.2, "approved": true},
          {"confidence": 0.84, "pnl_outcome": -0.4, "approved": false}
        ]
        """
    )
    monkeypatch.setenv("GOV_DELIVERY_CHANNEL", "telegram")
    monkeypatch.setenv("GOV_DELIVERY_TARGET", "12345")

    audit_db = str(tmp_path / "audit.db")
    portfolio_db = str(tmp_path / "portfolio.db")
    audit = AuditLogger(audit_db)
    audit.log("approval", {"approved": True})

    manifest = run_scheduled_governance_delivery(
        replay_pack_path=str(pack),
        audit_db=audit_db,
        portfolio_db=portfolio_db,
        out_dir=str(tmp_path / "reports"),
        delivery_dir=str(tmp_path / "delivery"),
    )

    data = json.loads(Path(manifest).read_text())
    assert data["kind"] == "weekly_governance_calibration_delivery"
    assert data["status"] == "ready-for-delivery"
    assert Path(data["report_path"]).exists()
    assert data["target"] == "12345"
