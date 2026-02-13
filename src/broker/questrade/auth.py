from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass
class QuestradeToken:
    access_token: str
    api_server: str
    expires_in: int


def refresh_access_token(refresh_token: str) -> QuestradeToken:
    response = requests.get(
        "https://login.questrade.com/oauth2/token",
        params={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    return QuestradeToken(
        access_token=payload["access_token"],
        api_server=payload["api_server"],
        expires_in=int(payload.get("expires_in", 0)),
    )
