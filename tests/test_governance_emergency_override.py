from datetime import datetime, timezone

from src.agents.governance_emergency_override import (
    create_emergency_override,
    evaluate_emergency_override,
)


def test_emergency_override_active():
    override = create_emergency_override(
        policy_id="p1",
        approved_by="adrian",
        reason="incident-mitigation",
        override_minutes=45,
    )
    out = evaluate_emergency_override(override)
    assert out["ok"] is True
    assert out["reason"] == "override_active"


def test_emergency_override_expired():
    override = create_emergency_override(
        policy_id="p1",
        approved_by="adrian",
        reason="incident-mitigation",
        override_minutes=1,
    )
    out = evaluate_emergency_override(
        override,
        now_utc=datetime(2100, 1, 1, tzinfo=timezone.utc),
    )
    assert out["ok"] is False
    assert out["reason"] == "override_expired"


def test_emergency_override_invalid_expiry():
    out = evaluate_emergency_override({"expires_utc": "bad-timestamp"})
    assert out["ok"] is False
    assert out["reason"] == "invalid_expiry"
