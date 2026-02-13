from src.data.news_ingestors.normalizer import normalize_news_events


def test_normalizer_dedups_and_filters_symbols():
    raw = [
        {"symbol": "SPY", "headline": "A", "score": 0.8, "sentiment": "positive", "price": 1},
        {"symbol": "SPY", "headline": "A", "score": 0.8, "sentiment": "positive", "price": 1},
        {"symbol": "IWM", "headline": "B", "score": 0.8, "sentiment": "positive", "price": 1},
    ]
    out = normalize_news_events(raw, symbols=["SPY", "QQQ"])
    assert len(out) == 1
    assert out[0]["symbol"] == "SPY"
    assert out[0]["event_id"].startswith("SPY:")
