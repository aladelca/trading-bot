from src.agents.governance_autoticket import build_reconciliation_tickets


def test_build_reconciliation_tickets_for_overdue_and_stale():
    reconciliation = {
        "recommendation_id": "rec-1",
        "overdue_review": True,
        "stale_pending": [{"version_tag": "v3"}, {"version_tag": "v4"}],
    }
    out = build_reconciliation_tickets(reconciliation)
    assert len(out) == 3
    assert out[0]["type"] == "overdue_review"
    assert out[0]["owner"] == "governance-owner"
    stale = [x for x in out if x["type"] == "stale_pending_cleanup"]
    assert len(stale) == 2
    assert all(x["owner"] == "risk-owner" for x in stale)


def test_build_reconciliation_tickets_no_findings():
    reconciliation = {
        "recommendation_id": "rec-1",
        "overdue_review": False,
        "stale_pending": [],
    }
    out = build_reconciliation_tickets(reconciliation)
    assert out == []
