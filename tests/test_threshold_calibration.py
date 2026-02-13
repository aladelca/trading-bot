from src.agents.threshold_calibration import ReplayScenario, calibrate_thresholds, evaluate_threshold


def test_evaluate_threshold_returns_selection_stats():
    scenarios = [
        ReplayScenario(confidence=0.96, pnl_outcome=1.0, approved=True),
        ReplayScenario(confidence=0.88, pnl_outcome=-0.2, approved=False),
    ]
    out = evaluate_threshold(scenarios, 0.90)
    assert out["selected"] == 1
    assert out["approval_rate"] == 1.0


def test_calibrate_thresholds_ranks_candidates():
    scenarios = [
        ReplayScenario(confidence=0.96, pnl_outcome=1.2, approved=True),
        ReplayScenario(confidence=0.92, pnl_outcome=0.6, approved=True),
        ReplayScenario(confidence=0.86, pnl_outcome=-0.5, approved=False),
    ]
    out = calibrate_thresholds(scenarios, [0.85, 0.90, 0.95])
    assert out["best"] is not None
    assert out["ranked"][0]["score"] >= out["ranked"][1]["score"]
