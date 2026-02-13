import requests

from src.broker.questrade.client import QuestradeClient


class _Resp:
    def __init__(self, code: int, text: str = "bad"):
        self.status_code = code
        self.text = text


def test_submit_once_broker_rejection_has_telemetry(monkeypatch):
    q = QuestradeClient(refresh_token="x")
    q.token = type("T", (), {"access_token": "a", "api_server": "https://api/"})()
    monkeypatch.setattr("src.broker.questrade.client.requests.post", lambda *a, **k: _Resp(400, "invalid order"))

    out = q._submit_once(q.token, "111", {"x": 1}, "idem-1")
    assert out["status"] == "error"
    assert out["rejection_source"] == "broker_api"
    assert out["telemetry"]["phase"] == "submit"


def test_submit_once_transport_rejection_has_telemetry(monkeypatch):
    q = QuestradeClient(refresh_token="x")
    q.token = type("T", (), {"access_token": "a", "api_server": "https://api/"})()

    def _boom(*_a, **_k):
        raise requests.RequestException("net down")

    monkeypatch.setattr("src.broker.questrade.client.requests.post", _boom)

    out = q._submit_once(q.token, "111", {"x": 1}, "idem-1")
    assert out["status"] == "error"
    assert out["rejection_source"] == "broker_transport"
    assert out["telemetry"]["http_status"] == 503
