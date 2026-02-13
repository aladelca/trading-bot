from dataclasses import dataclass


@dataclass
class TradeSignal:
    symbol: str
    side: str
    confidence: float
    entry: float
    stop: float
    take_profit: float
    rationale: str
