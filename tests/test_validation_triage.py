from src.execution.validation_triage import build_validation_anomaly_triage


def test_validation_triage_high_severity_path():
    records = [
        {"status": "error", "rejection_source": "broker_api"},
        {"status": "error", "rejection_source": "broker_transport"},
        {"status": "submitted"},
        {"status": "blocked", "rejection_source": "pre_trade_validation", "rollout": {"auto_reverted": True}},
    ]

    out = build_validation_anomaly_triage(
        records,
        max_blocked_rate=0.2,
        max_broker_error_rate=0.2,
        max_auto_reverted_rate=0.01,
    )

    assert out["status"] == "alert"
    assert out["overall_severity"] == "high"
    assert any(f["owner"] == "broker-integration" for f in out["findings"])


def test_validation_triage_ok_path():
    records = [{"status": "submitted"}, {"status": "submitted"}]
    out = build_validation_anomaly_triage(records)
    assert out["status"] == "ok"
    assert out["findings"] == []
