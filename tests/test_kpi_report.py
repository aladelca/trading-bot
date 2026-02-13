from apps.backtester.report import generate_kpi_report
from src.storage.audit_log import AuditLogger


def test_kpi_report_counts(tmp_path):
    db = tmp_path / "audit.db"
    audit = AuditLogger(str(db))
    audit.log("approval", {"approved": True})
    audit.log("approval", {"approved": False})
    audit.log("fill", {"symbol": "SPY"})
    audit.log("signal_rejected", {"reason": "x"})

    report = generate_kpi_report(str(db))
    assert report["events_total"] == 4
    assert report["approvals_total"] == 2
    assert report["approvals_yes"] == 1
    assert report["fills_total"] == 1
    assert report["signals_rejected"] == 1
