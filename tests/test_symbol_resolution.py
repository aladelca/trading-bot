from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient


class DummyResp:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_resolve_symbol_id_exact_match(monkeypatch):
    q = QuestradeClient(refresh_token="x")

    monkeypatch.setattr(
        "src.broker.questrade.client.refresh_access_token",
        lambda _rt: type("T", (), {"access_token": "a", "api_server": "https://api/"})(),
    )

    def fake_get(url, *args, **kwargs):
        if url.endswith("/symbols/search"):
            return DummyResp({"symbols": [{"symbol": "SPY", "symbolId": 12345}]})
        if url.endswith("/accounts"):
            return DummyResp({"accounts": [{"number": "111"}]})
        return DummyResp({})

    monkeypatch.setattr("src.broker.questrade.client.requests.get", fake_get)
    sid = q.resolve_symbol_id("SPY")
    assert sid == 12345


def test_submit_order_blocks_when_symbol_id_missing(monkeypatch):
    q = QuestradeClient(refresh_token="x")

    monkeypatch.setattr(
        "src.broker.questrade.client.refresh_access_token",
        lambda _rt: type("T", (), {"access_token": "a", "api_server": "https://api/"})(),
    )

    def fake_get(url, *args, **kwargs):
        if url.endswith("/accounts"):
            return DummyResp({"accounts": [{"number": "111"}]})
        if url.endswith("/symbols/search"):
            return DummyResp({"symbols": []})
        return DummyResp({})

    monkeypatch.setattr("src.broker.questrade.client.requests.get", fake_get)

    out = q.submit_order(OrderRequest("SPY", "buy", 1), dry_run=False)
    assert out["status"] == "blocked"
    assert out["reason"] == "missing_symbol_id"
