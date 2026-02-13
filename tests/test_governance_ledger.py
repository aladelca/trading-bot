from src.agents.governance_ledger import list_governance_versions, record_governance_version
from src.storage.audit_log import AuditLogger


def test_governance_version_record_and_list(tmp_path):
    audit = AuditLogger(str(tmp_path / "audit.db"))

    record_governance_version(
        audit,
        recommendation_id="rec-1",
        version_tag="v1",
        status="approved",
        decided_by="adrian",
        payload={"min_conf": 0.9},
    )
    record_governance_version(
        audit,
        recommendation_id="rec-1",
        version_tag="v2",
        status="approved-with-changes",
        decided_by="adrian",
        payload={"min_conf": 0.92},
    )

    rows = list_governance_versions(audit, recommendation_id="rec-1")
    assert len(rows) == 2
    assert rows[0]["version_tag"] == "v1"
    assert rows[1]["version_tag"] == "v2"
