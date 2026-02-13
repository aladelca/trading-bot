from src.execution.validation_metrics import compute_validation_metrics, evaluate_validation_alerts


def test_compute_validation_metrics_counts_and_rates():
    records = [
        {"status": "blocked", "rejection_source": "pre_trade_validation", "rollout": {"auto_reverted": True}},
        {"status": "error", "rejection_source": "broker_api"},
        {"status": "dry-run", "validation_warning": {"reason": "x", "rollout": {"auto_reverted": False}}},
        {"status": "submitted"},
    ]
    out = compute_validation_metrics(records)
    assert out["records_total"] == 4
    assert out["blocked_pretrade_total"] == 1
    assert out["broker_error_total"] == 1
    assert out["warning_report_only_total"] == 1
    assert out["auto_reverted_total"] == 1


def test_evaluate_validation_alerts_triggers_thresholds():
    metrics = {
        "blocked_pretrade_rate": 0.5,
        "broker_error_rate": 0.2,
        "auto_reverted_rate": 0.1,
    }
    alerts = evaluate_validation_alerts(metrics)
    assert "blocked_pretrade_rate_above_threshold" in alerts
    assert "broker_error_rate_above_threshold" in alerts
    assert "auto_reverted_rate_above_threshold" in alerts
