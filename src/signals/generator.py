from src.signals.models import TradeSignal


def generate_signal_from_news_event(event: dict) -> TradeSignal | None:
    score = float(event.get("score", 0))
    if score < 0.65:
        return None
    symbol = event.get("symbol", "SPY")
    side = "buy" if event.get("sentiment", "positive") == "positive" else "sell"
    entry = float(event.get("price", 500))
    stop = entry * (0.99 if side == "buy" else 1.01)
    tp = entry * (1.02 if side == "buy" else 0.98)
    return TradeSignal(symbol, side, score, entry, stop, tp, event.get("headline", "news-event"))
