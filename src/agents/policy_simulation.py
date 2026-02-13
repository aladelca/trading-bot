from __future__ import annotations

from src.agents.automation_policy import choose_auto_approve_tier, tier_allows_auto_approve
from src.agents.drift import detect_metric_drift, drift_severity, rollback_recommendation
from src.agents.review_learning import generate_learning_recommendations


def simulate_governance_policy(
    *,
    confidence: float,
    symbol: str,
    allowed_symbols: set[str],
    allowed_tiers: set[str],
    current_kpi: dict,
    baseline_kpi: dict,
) -> dict:
    tier = choose_auto_approve_tier(confidence)
    auto_approve = tier_allows_auto_approve(tier, symbol, allowed_symbols, allowed_tiers=allowed_tiers)

    alerts = detect_metric_drift(current_kpi, baseline_kpi)
    severity = drift_severity(alerts)
    rollback = rollback_recommendation(alerts)
    recs = generate_learning_recommendations(current_kpi)

    return {
        "auto_approve": auto_approve,
        "tier": tier,
        "symbol": symbol.upper(),
        "allowed_tiers": sorted({t.lower() for t in allowed_tiers}),
        "drift_alerts": alerts,
        "drift_severity": severity,
        "rollback_recommendation": rollback,
        "learning_recommendations": recs,
    }
