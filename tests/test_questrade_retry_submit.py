from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient


def test_submit_order_retries_retryable_errors(monkeypatch):
    q = QuestradeClient(refresh_token="x")

    monkeypatch.setattr(
        "src.broker.questrade.client.refresh_access_token",
        lambda _rt: type("T", (), {"access_token": "a", "api_server": "https://api/"})(),
    )
    monkeypatch.setattr(q, "get_accounts", lambda: [{"number": "111"}])
    monkeypatch.setattr(q, "resolve_symbol_id", lambda _s: 123)

    calls = {"n": 0}

    def fake_submit_once(token, account_id, payload, idem_key):
        calls["n"] += 1
        if calls["n"] < 3:
            return {"status": "error", "error_category": "retryable", "reason": "http_503"}
        return {"status": "submitted", "broker": "questrade", "response": {"ok": True}}

    monkeypatch.setattr(q, "_submit_once", fake_submit_once)
    monkeypatch.setattr("src.execution.retry.time.sleep", lambda _s: None)

    out = q.submit_order(OrderRequest("SPY", "buy", 1), dry_run=False, request_id="req-1")
    assert out["status"] == "submitted"
    assert out["attempt"] == 3
    assert "idempotency_key" in out
