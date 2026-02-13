from __future__ import annotations

from src.data.news_ingestors.normalizer import normalize_news_events


RAW_FEED_SAMPLE = [
    {
        "symbol": "SPY",
        "headline": "Macro headline placeholder",
        "sentiment": "positive",
        "score": 0.72,
        "price": 500,
    },
    {
        "symbol": "SPY",
        "headline": "Macro headline placeholder",  # duplicate
        "sentiment": "positive",
        "score": 0.72,
        "price": 500,
    },
    {
        "symbol": "QQQ",
        "headline": "Tech earnings momentum",
        "sentiment": "positive",
        "score": 0.69,
        "price": 430,
    },
]


def fetch_free_news_events(symbols: list[str]) -> list[dict]:
    """Fetch free-news sample and return normalized, deduped, whitelist-relevant events."""
    return normalize_news_events(RAW_FEED_SAMPLE, symbols=symbols)
