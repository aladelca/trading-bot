from src.agents.policy_simulation import simulate_governance_policy


def test_policy_simulation_manual_when_tier_not_allowed():
    out = simulate_governance_policy(
        confidence=0.86,
        symbol="SPY",
        allowed_symbols={"SPY"},
        allowed_tiers={"tier-1", "tier-2"},
        current_kpi={"approval_rate": 0.5, "signals_rejected": 10, "equity_pnl_total": 5},
        baseline_kpi={"approval_rate": 0.6, "signals_rejected": 8, "equity_pnl_total": 8},
    )
    assert out["tier"] == "tier-3"
    assert out["auto_approve"] is False


def test_policy_simulation_detects_drift_and_recommendations():
    out = simulate_governance_policy(
        confidence=0.96,
        symbol="QQQ",
        allowed_symbols={"SPY", "QQQ"},
        allowed_tiers={"tier-1", "tier-2"},
        current_kpi={"approval_rate": 0.3, "signals_rejected": 30, "equity_pnl_total": -10},
        baseline_kpi={"approval_rate": 0.6, "signals_rejected": 10, "equity_pnl_total": 10},
    )
    assert out["auto_approve"] is True
    assert out["drift_severity"] in {"medium", "high"}
    assert len(out["learning_recommendations"]) >= 2
