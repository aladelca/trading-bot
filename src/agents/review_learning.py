from __future__ import annotations


def generate_learning_recommendations(kpi: dict) -> list[str]:
    recs: list[str] = []

    approval_rate = float(kpi.get("approval_rate", 0.0))
    rejection_count = int(kpi.get("signals_rejected", 0))
    equity_pnl = float(kpi.get("equity_pnl_total", 0.0))

    if rejection_count > 20:
        recs.append("High rejection volume: tighten pre-signal filters to reduce low-quality proposals.")

    if approval_rate < 0.4:
        recs.append("Low approval rate: improve signal rationale quality and confidence calibration.")

    if equity_pnl < 0:
        recs.append("Negative equity PnL: reduce risk_per_trade and narrow tradable symbols.")

    if not recs:
        recs.append("System stable: continue paper monitoring and collect longer horizon metrics.")

    return recs
