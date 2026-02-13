from __future__ import annotations

from src.storage.audit_log import AuditLogger


def record_governance_version(
    audit: AuditLogger,
    *,
    recommendation_id: str,
    version_tag: str,
    status: str,
    decided_by: str,
    payload: dict,
) -> None:
    audit.log_governance_version(
        recommendation_id=recommendation_id,
        version_tag=version_tag,
        status=status,
        decided_by=decided_by,
        payload=payload,
    )


def list_governance_versions(audit: AuditLogger, recommendation_id: str) -> list[dict]:
    return audit.list_governance_versions(recommendation_id=recommendation_id)
