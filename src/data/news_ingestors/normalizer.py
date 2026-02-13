from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class NormalizedNewsEvent:
    event_id: str
    symbol: str
    headline: str
    sentiment: str
    score: float
    price: float
    ts_utc: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_news_events(raw_events: list[dict], symbols: list[str]) -> list[dict]:
    whitelist = {s.upper() for s in symbols}
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []

    for item in raw_events:
        symbol = str(item.get("symbol", "")).upper().strip()
        headline = str(item.get("headline", "")).strip()
        if not symbol or not headline:
            continue
        if symbol not in whitelist:
            continue

        ts = str(item.get("ts_utc") or _utc_now_iso())
        dedup_key = (symbol, headline.lower())
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        score = float(item.get("score", 0.0))
        sentiment = str(item.get("sentiment", "neutral")).lower()
        price = float(item.get("price", 0.0))

        event_id = f"{symbol}:{abs(hash((headline.lower(), ts))) % 10_000_000}"
        out.append(
            {
                "event_id": event_id,
                "symbol": symbol,
                "headline": headline,
                "sentiment": sentiment,
                "score": score,
                "price": price,
                "ts_utc": ts,
            }
        )

    return out
