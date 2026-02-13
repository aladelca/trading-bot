from src.execution.retry import RetryPolicy, with_retry


def test_with_retry_retries_until_success():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] < 3:
            return {"status": "error", "error_category": "retryable"}
        return {"status": "submitted"}

    out = with_retry(
        fn,
        should_retry=lambda r: r.get("status") == "error" and r.get("error_category") == "retryable",
        policy=RetryPolicy(max_attempts=3, base_delay_seconds=0.0, backoff_multiplier=1.0),
    )
    assert out["status"] == "submitted"
    assert out["attempt"] == 3
