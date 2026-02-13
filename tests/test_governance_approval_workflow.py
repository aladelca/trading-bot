from src.agents.governance_approval import apply_decision, build_recommendation_package


def test_accept_recommendation_package():
    pkg = build_recommendation_package({"recommended_auto_approve_min_confidence": 0.9})
    out = apply_decision(pkg, "accept", decided_by="adrian")
    assert out["status"] == "approved"
    assert out["final_recommendation"]["recommended_auto_approve_min_confidence"] == 0.9


def test_reject_recommendation_package():
    pkg = build_recommendation_package({"recommended_allowed_tiers": ["tier-1"]})
    out = apply_decision(pkg, "reject", decided_by="adrian", reason="too restrictive")
    assert out["status"] == "rejected"
    assert out["decision"]["reason"] == "too restrictive"


def test_change_set_recommendation_package():
    pkg = build_recommendation_package({"recommended_auto_approve_min_confidence": 0.94})
    out = apply_decision(
        pkg,
        "change-set",
        decided_by="adrian",
        overrides={"recommended_auto_approve_min_confidence": 0.91},
    )
    assert out["status"] == "approved-with-changes"
    assert out["final_recommendation"]["recommended_auto_approve_min_confidence"] == 0.91
