from src.agents.review_learning import generate_learning_recommendations


def test_learning_agent_flags_negative_pnl():
    recs = generate_learning_recommendations({"approval_rate": 0.3, "signals_rejected": 25, "equity_pnl_total": -10})
    assert len(recs) >= 2
    assert any("Negative equity PnL" in r["recommendation"] for r in recs)
    assert all("priority" in r and "topic" in r for r in recs)
