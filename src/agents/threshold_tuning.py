from __future__ import annotations


def recommend_governance_thresholds(kpi: dict) -> dict:
    approval_rate = float(kpi.get("approval_rate", 0.0))
    equity_pnl = float(kpi.get("equity_pnl_total", 0.0))
    rejected = int(kpi.get("signals_rejected", 0))

    min_conf = 0.90
    allowed_tiers = {"tier-1", "tier-2"}
    posture = "balanced"

    # Conservative posture when quality deteriorates.
    if equity_pnl < 0 or approval_rate < 0.45 or rejected >= 20:
        min_conf = 0.94
        allowed_tiers = {"tier-1"}
        posture = "conservative"
    # Slightly relaxed posture with strong paper metrics.
    elif equity_pnl > 5 and approval_rate >= 0.65 and rejected < 10:
        min_conf = 0.88
        allowed_tiers = {"tier-1", "tier-2", "tier-3"}
        posture = "opportunistic"

    return {
        "recommended_auto_approve_min_confidence": round(min_conf, 4),
        "recommended_allowed_tiers": sorted(allowed_tiers),
        "posture": posture,
        "inputs": {
            "approval_rate": approval_rate,
            "equity_pnl_total": equity_pnl,
            "signals_rejected": rejected,
        },
    }
