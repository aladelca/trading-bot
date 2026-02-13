from __future__ import annotations

from datetime import datetime, timezone

OWNER_MATRIX = {
    "overdue_review": "governance-owner",
    "stale_pending": "risk-owner",
}


def build_reconciliation_tickets(reconciliation: dict, *, default_owner: str = "ops-owner") -> list[dict]:
    tickets: list[dict] = []
    recommendation_id = str(reconciliation.get("recommendation_id", ""))

    if bool(reconciliation.get("overdue_review")):
        tickets.append(
            {
                "kind": "governance_reconciliation_ticket",
                "type": "overdue_review",
                "owner": OWNER_MATRIX.get("overdue_review", default_owner),
                "recommendation_id": recommendation_id,
                "summary": f"Governance review overdue for {recommendation_id}",
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "severity": "medium",
            }
        )

    for row in reconciliation.get("stale_pending", []):
        version_tag = str(row.get("version_tag", ""))
        tickets.append(
            {
                "kind": "governance_reconciliation_ticket",
                "type": "stale_pending_cleanup",
                "owner": OWNER_MATRIX.get("stale_pending", default_owner),
                "recommendation_id": recommendation_id,
                "version_tag": version_tag,
                "summary": f"Stale pending governance decision requires cleanup: {version_tag}",
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "severity": "high",
            }
        )

    return tickets
