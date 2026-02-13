from src.broker.questrade.auth import refresh_access_token


class DummyResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "access_token": "token-1",
            "api_server": "https://api01.iq.questrade.com/",
            "expires_in": 1800,
        }


def test_refresh_access_token_parses_response(monkeypatch):
    def fake_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr("src.broker.questrade.auth.requests.get", fake_get)
    token = refresh_access_token("refresh-token")
    assert token.access_token == "token-1"
    assert token.api_server.startswith("https://")
    assert token.expires_in == 1800
