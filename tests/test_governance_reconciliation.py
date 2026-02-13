from datetime import datetime, timezone

from src.agents.governance_reconciliation import evaluate_reconciliation


def test_reconciliation_overdue_and_stale_pending_detected():
    versions = [
        {
            "id": 1,
            "version_tag": "v1",
            "status": "pending-approval",
            "created_at": "2026-02-01 00:00:00",
        },
        {
            "id": 2,
            "version_tag": "v2",
            "status": "approved",
            "created_at": "2026-02-02 00:00:00",
        },
    ]

    out = evaluate_reconciliation(
        versions,
        cadence_days=7,
        stale_pending_hours=24,
        now_utc=datetime(2026, 2, 13, tzinfo=timezone.utc),
    )
    assert out["ok"] is True
    assert out["overdue_review"] is True
    assert len(out["stale_pending"]) == 1
    assert out["cleanup_plan"][0]["action"] == "mark_stale_and_require_revalidation"


def test_reconciliation_recent_version_not_overdue():
    versions = [
        {
            "id": 5,
            "version_tag": "v5",
            "status": "approved",
            "created_at": "2026-02-12T23:00:00+00:00",
        }
    ]
    out = evaluate_reconciliation(
        versions,
        cadence_days=7,
        stale_pending_hours=24,
        now_utc=datetime(2026, 2, 13, tzinfo=timezone.utc),
    )
    assert out["ok"] is True
    assert out["overdue_review"] is False
    assert out["stale_pending"] == []
