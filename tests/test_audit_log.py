from src.storage.audit_log import AuditLogger


def test_audit_log_writes_rows(tmp_path):
    db = tmp_path / "audit.db"
    audit = AuditLogger(str(db))
    audit.log("fill", {"symbol": "SPY", "qty": 1})
    assert audit.count() == 1
    assert audit.count("fill") == 1
