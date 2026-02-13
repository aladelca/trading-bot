from src.execution.errors import classify_broker_error


def test_classify_retryable_http():
    info = classify_broker_error(503, "service unavailable")
    assert info.category == "retryable"


def test_classify_blocked_auth():
    info = classify_broker_error(401, "unauthorized")
    assert info.category == "blocked"


def test_classify_fatal_payload():
    info = classify_broker_error(400, "bad request")
    assert info.category == "fatal"
