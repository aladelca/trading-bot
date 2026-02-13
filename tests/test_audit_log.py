from src.storage.audit_log import AuditLogger


def test_audit_log_writes_rows(tmp_path):
    db = tmp_path / "audit.db"
    audit = AuditLogger(str(db))
    audit.log("fill", {"symbol": "SPY", "qty": 1})
    assert audit.count() == 1
    assert audit.count("fill") == 1


def test_audit_log_writes_comms_rows(tmp_path):
    db = tmp_path / "audit.db"
    audit = AuditLogger(str(db))
    audit.log_comms(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        transport="session-bridge",
        status="ok",
        reason="",
        correlation_id="r1:signal->risk",
        payload={"x": 1},
    )
    assert audit.count_comms() == 1
    assert audit.count_comms("ok") == 1
