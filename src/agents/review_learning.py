from __future__ import annotations


def generate_learning_recommendations(kpi: dict) -> list[dict]:
    recs: list[dict] = []

    approval_rate = float(kpi.get("approval_rate", 0.0))
    rejection_count = int(kpi.get("signals_rejected", 0))
    equity_pnl = float(kpi.get("equity_pnl_total", 0.0))

    if rejection_count > 20:
        recs.append(
            {
                "priority": "medium",
                "topic": "signal-quality",
                "recommendation": "High rejection volume: tighten pre-signal filters to reduce low-quality proposals.",
            }
        )

    if approval_rate < 0.4:
        recs.append(
            {
                "priority": "high",
                "topic": "approval-calibration",
                "recommendation": "Low approval rate: improve signal rationale quality and confidence calibration.",
            }
        )

    if equity_pnl < 0:
        recs.append(
            {
                "priority": "high",
                "topic": "risk-control",
                "recommendation": "Negative equity PnL: reduce risk_per_trade and narrow tradable symbols.",
            }
        )

    if not recs:
        recs.append(
            {
                "priority": "low",
                "topic": "stability",
                "recommendation": "System stable: continue paper monitoring and collect longer horizon metrics.",
            }
        )

    return recs
