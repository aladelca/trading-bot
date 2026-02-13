from src.agents.drift import detect_metric_drift, drift_severity, rollback_recommendation


def test_drift_detection_and_rollback():
    curr = {"approval_rate": 0.3, "equity_pnl_total": -20, "signals_rejected": 30}
    base = {"approval_rate": 0.6, "equity_pnl_total": 10, "signals_rejected": 10}
    alerts = detect_metric_drift(curr, base)
    assert len(alerts) >= 2
    sev = drift_severity(alerts)
    assert sev in {"medium", "high"}
    rb = rollback_recommendation(alerts)
    assert "rollback" in rb.lower()
