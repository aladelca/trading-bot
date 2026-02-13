from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient


def test_submit_order_blocked_in_retail_mode(monkeypatch):
    q = QuestradeClient(refresh_token="x")
    monkeypatch.setenv("QUESTRADE_ACCOUNT_MODE", "retail_read_only")

    out = q.submit_order(OrderRequest("SPY", "buy", 1), dry_run=False)
    assert out["status"] == "blocked"
    assert out["reason"] == "questrade_retail_read_only"


def test_submit_order_allows_partner_mode_path(monkeypatch):
    q = QuestradeClient(refresh_token="x")
    monkeypatch.setenv("QUESTRADE_ACCOUNT_MODE", "partner_trading")

    monkeypatch.setattr(
        "src.broker.questrade.client.refresh_access_token",
        lambda _rt: type("T", (), {"access_token": "a", "api_server": "https://api/"})(),
    )
    monkeypatch.setattr(q, "get_accounts", lambda: [{"number": "111"}])
    monkeypatch.setattr(q, "resolve_symbol_id", lambda _s: 123)
    monkeypatch.setattr(q, "_submit_once", lambda *_a, **_k: {"status": "submitted", "broker": "questrade"})

    out = q.submit_order(OrderRequest("SPY", "buy", 1), dry_run=False, request_id="r1")
    assert out["status"] == "submitted"
