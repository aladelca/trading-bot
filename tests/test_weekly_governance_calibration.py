from pathlib import Path

from apps.backtester.weekly_governance_calibration import generate_weekly_governance_calibration_report
from src.storage.audit_log import AuditLogger


def test_generate_weekly_governance_calibration_report(tmp_path):
    audit_db = str(tmp_path / "audit.db")
    portfolio_db = str(tmp_path / "portfolio.db")
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

    audit = AuditLogger(audit_db)
    audit.log("approval", {"approved": True})

    out = generate_weekly_governance_calibration_report(
        replay_pack_path=str(pack),
        audit_db=audit_db,
        portfolio_db=portfolio_db,
        candidates=[0.85, 0.9],
        out_dir=str(tmp_path),
    )
    text = Path(out).read_text()
    assert "Weekly Governance Calibration" in text
    assert "threshold:" in text
