

def position_size_from_risk(equity: float, risk_per_trade: float, entry: float, stop: float) -> int:
    risk_dollars = equity * risk_per_trade
    risk_per_share = abs(entry - stop)
    if risk_per_share <= 0:
        return 0
    qty = int(risk_dollars / risk_per_share)
    return max(qty, 0)
