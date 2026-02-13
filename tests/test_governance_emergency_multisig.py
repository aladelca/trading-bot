from datetime import datetime, timezone

from src.agents.governance_emergency_multisig import (
    create_emergency_override_multisig,
    evaluate_emergency_override_multisig,
)


def test_multisig_override_active():
    override = create_emergency_override_multisig(
        policy_id="p1",
        incident_id="inc-77",
        reason="critical incident",
        approvers=["adrian", "risk-lead"],
        min_approvals=2,
        override_minutes=60,
    )
    out = evaluate_emergency_override_multisig(override)
    assert out["ok"] is True
    assert out["reason"] == "override_multisig_active"


def test_multisig_override_rejects_missing_incident():
    override = create_emergency_override_multisig(
        policy_id="p1",
        incident_id="",
        reason="critical incident",
        approvers=["adrian", "risk-lead"],
        min_approvals=2,
    )
    out = evaluate_emergency_override_multisig(override)
    assert out["ok"] is False
    assert out["reason"] == "missing_incident_id"


def test_multisig_override_rejects_insufficient_approvals():
    override = create_emergency_override_multisig(
        policy_id="p1",
        incident_id="inc-88",
        reason="critical incident",
        approvers=["adrian"],
        min_approvals=2,
    )
    out = evaluate_emergency_override_multisig(override)
    assert out["ok"] is False
    assert out["reason"] == "insufficient_approvals"


def test_multisig_override_expired():
    override = create_emergency_override_multisig(
        policy_id="p1",
        incident_id="inc-99",
        reason="critical incident",
        approvers=["adrian", "risk-lead"],
        min_approvals=2,
        override_minutes=1,
    )
    out = evaluate_emergency_override_multisig(
        override,
        now_utc=datetime(2100, 1, 1, tzinfo=timezone.utc),
    )
    assert out["ok"] is False
    assert out["reason"] == "override_expired"
