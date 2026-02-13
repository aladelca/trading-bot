from __future__ import annotations

from datetime import datetime, timezone


def evaluate_application_guardrails(approved_package: dict) -> dict:
    status = str(approved_package.get("status", "")).lower()
    if not status.startswith("approved"):
        return {"ok": False, "reason": "package_not_approved"}

    final = approved_package.get("final_recommendation") or {}

    min_conf = final.get("recommended_auto_approve_min_confidence")
    tiers = final.get("recommended_allowed_tiers")

    if min_conf is None or tiers is None:
        return {"ok": False, "reason": "missing_required_fields"}

    min_conf = float(min_conf)
    if min_conf < 0.80 or min_conf > 0.99:
        return {"ok": False, "reason": "min_confidence_out_of_range", "value": min_conf}

    normalized_tiers = [str(t).lower() for t in tiers]
    allowed = {"tier-1", "tier-2", "tier-3"}
    if any(t not in allowed for t in normalized_tiers):
        return {"ok": False, "reason": "invalid_tier_values", "tiers": normalized_tiers}

    if "tier-3" in normalized_tiers and min_conf > 0.92:
        return {
            "ok": False,
            "reason": "inconsistent_tier_confidence_policy",
            "detail": "tier-3 enabled but min confidence too strict",
        }

    return {
        "ok": True,
        "reason": "ok",
        "normalized": {
            "recommended_auto_approve_min_confidence": round(min_conf, 4),
            "recommended_allowed_tiers": sorted(set(normalized_tiers)),
        },
    }


def build_rollback_template(approved_package: dict, previous_policy: dict | None = None) -> dict:
    previous_policy = previous_policy or {}
    return {
        "kind": "governance_rollback_plan",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "recommendation_id": approved_package.get("id"),
        "current_policy_candidate": approved_package.get("final_recommendation") or {},
        "rollback_to": previous_policy,
        "steps": [
            "Set AUTO_APPROVE_ENABLED=false if incident severity is high.",
            "Restore AUTO_APPROVE_MIN_CONFIDENCE and AUTO_APPROVE_ALLOWED_TIERS from rollback_to.",
            "Keep LIVE_ORDER_DRY_RUN=true until post-rollback validation passes.",
            "Run KPI and drift checks before re-enabling prior automation posture.",
        ],
    }
