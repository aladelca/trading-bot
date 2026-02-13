from src.agents.governance_apply import build_rollback_template, evaluate_application_guardrails


def test_guardrails_accept_valid_package():
    pkg = {
        "id": "r1",
        "status": "approved",
        "final_recommendation": {
            "recommended_auto_approve_min_confidence": 0.9,
            "recommended_allowed_tiers": ["tier-1", "tier-2"],
        },
    }
    out = evaluate_application_guardrails(pkg)
    assert out["ok"] is True


def test_guardrails_reject_out_of_range_confidence():
    pkg = {
        "status": "approved",
        "final_recommendation": {
            "recommended_auto_approve_min_confidence": 0.5,
            "recommended_allowed_tiers": ["tier-1"],
        },
    }
    out = evaluate_application_guardrails(pkg)
    assert out["ok"] is False
    assert out["reason"] == "min_confidence_out_of_range"


def test_rollback_template_contains_steps():
    pkg = {"id": "r2", "final_recommendation": {"recommended_auto_approve_min_confidence": 0.9}}
    out = build_rollback_template(pkg, previous_policy={"AUTO_APPROVE_MIN_CONFIDENCE": 0.92})
    assert out["kind"] == "governance_rollback_plan"
    assert len(out["steps"]) >= 3
