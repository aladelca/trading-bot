from datetime import datetime, timezone

from src.agents.governance_drift_ack import create_drift_ack, evaluate_drift_ack


def test_drift_ack_active():
    ack = create_drift_ack(policy_id="p1", severity="high", acknowledged_by="adrian", valid_for_minutes=60)
    out = evaluate_drift_ack(ack)
    assert out["ok"] is True
    assert out["reason"] == "ack_active"


def test_drift_ack_expired():
    ack = create_drift_ack(policy_id="p1", severity="high", acknowledged_by="adrian", valid_for_minutes=1)
    out = evaluate_drift_ack(
        ack,
        now_utc=datetime(2100, 1, 1, tzinfo=timezone.utc),
    )
    assert out["ok"] is False
    assert out["reason"] == "ack_expired"
