from src.storage.audit_log import AuditLogger


def test_save_and_get_decision(tmp_path):
    audit = AuditLogger(str(tmp_path / "audit.db"))
    audit.save_decision("req-1", True, "telegram")
    assert audit.get_decision("req-1") is True
    audit.save_decision("req-1", False, "telegram")
    assert audit.get_decision("req-1") is False
