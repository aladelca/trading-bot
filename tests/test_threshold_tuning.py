from src.agents.threshold_tuning import recommend_governance_thresholds


def test_threshold_tuning_conservative_mode():
    out = recommend_governance_thresholds(
        {"approval_rate": 0.4, "equity_pnl_total": -2.0, "signals_rejected": 25}
    )
    assert out["posture"] == "conservative"
    assert out["recommended_auto_approve_min_confidence"] == 0.94
    assert out["recommended_allowed_tiers"] == ["tier-1"]


def test_threshold_tuning_opportunistic_mode():
    out = recommend_governance_thresholds(
        {"approval_rate": 0.72, "equity_pnl_total": 8.0, "signals_rejected": 6}
    )
    assert out["posture"] == "opportunistic"
    assert out["recommended_auto_approve_min_confidence"] == 0.88
    assert "tier-3" in out["recommended_allowed_tiers"]
