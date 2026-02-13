from src.broker.questrade.client import QuestradeClient


class DummyResp:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def _patch_token(monkeypatch):
    monkeypatch.setattr(
        "src.broker.questrade.client.refresh_access_token",
        lambda _rt: type("T", (), {"access_token": "a", "api_server": "https://api/"})(),
    )


def test_get_balances_positions_and_snapshot(monkeypatch):
    q = QuestradeClient(refresh_token="x")
    _patch_token(monkeypatch)

    def fake_get(url, *args, **kwargs):
        if url.endswith("/accounts"):
            return DummyResp({"accounts": [{"number": "111"}]})
        if url.endswith("/accounts/111/balances"):
            return DummyResp({"perCurrencyBalances": [{"currency": "USD", "buyingPower": 2500.0}]})
        if url.endswith("/accounts/111/positions"):
            return DummyResp({"positions": [{"symbol": "SPY", "openQuantity": 10}]})
        if url.endswith("/symbols/search"):
            prefix = kwargs.get("params", {}).get("prefix")
            sid = 100 if prefix == "SPY" else 200
            return DummyResp({"symbols": [{"symbol": prefix, "symbolId": sid}]})
        if url.endswith("/markets/quotes"):
            return DummyResp({"quotes": [{"symbol": "SPY", "lastTradePrice": 600.0}]})
        return DummyResp({})

    monkeypatch.setattr("src.broker.questrade.client.requests.get", fake_get)

    balances = q.get_balances()
    positions = q.get_positions()
    snapshot = q.get_account_market_snapshot(symbols=["SPY"])

    assert balances["perCurrencyBalances"][0]["buyingPower"] == 2500.0
    assert positions[0]["symbol"] == "SPY"
    assert snapshot["quotes"][0]["symbol"] == "SPY"


def test_get_candles_uses_symbol_id(monkeypatch):
    q = QuestradeClient(refresh_token="x")
    _patch_token(monkeypatch)

    def fake_get(url, *args, **kwargs):
        if url.endswith("/symbols/search"):
            return DummyResp({"symbols": [{"symbol": "SPY", "symbolId": 12345}]})
        if url.endswith("/markets/candles/12345"):
            params = kwargs.get("params", {})
            assert params.get("interval") == "OneMinute"
            return DummyResp({"candles": [{"start": "2026-02-13T10:00:00-05:00", "close": 599.5}]})
        return DummyResp({})

    monkeypatch.setattr("src.broker.questrade.client.requests.get", fake_get)
    candles = q.get_candles("SPY", "2026-02-13T10:00:00-05:00", "2026-02-13T10:05:00-05:00")
    assert candles[0]["close"] == 599.5
