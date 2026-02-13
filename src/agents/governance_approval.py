from __future__ import annotations

from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_recommendation_package(recommendation: dict, source: str = "threshold_tuning") -> dict:
    return {
        "id": recommendation.get("id") or f"gov-rec-{int(datetime.now(timezone.utc).timestamp())}",
        "source": source,
        "created_utc": _now(),
        "status": "pending-approval",
        "recommendation": recommendation,
        "decision": None,
    }


def apply_decision(
    package: dict,
    decision: str,
    decided_by: str,
    overrides: dict | None = None,
    reason: str = "",
) -> dict:
    d = decision.strip().lower()
    if d not in {"accept", "reject", "change-set"}:
        raise ValueError("invalid_decision")

    out = dict(package)
    recommendation = dict(out.get("recommendation", {}))

    if d == "accept":
        final_recommendation = recommendation
        status = "approved"
    elif d == "reject":
        final_recommendation = recommendation
        status = "rejected"
    else:
        final_recommendation = {**recommendation, **(overrides or {})}
        status = "approved-with-changes"

    out["status"] = status
    out["final_recommendation"] = final_recommendation
    out["decision"] = {
        "decision": d,
        "decided_by": decided_by,
        "reason": reason,
        "overrides": overrides or {},
        "decided_utc": _now(),
    }
    return out
