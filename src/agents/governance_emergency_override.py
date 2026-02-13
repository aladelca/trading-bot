from __future__ import annotations

from datetime import datetime, timedelta, timezone


def create_emergency_override(
    *,
    policy_id: str,
    approved_by: str,
    reason: str,
    severity: str = "critical",
    override_minutes: int = 30,
    changes: dict | None = None,
) -> dict:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=int(override_minutes))
    return {
        "kind": "governance_emergency_override",
        "policy_id": policy_id,
        "severity": severity.lower(),
        "approved_by": approved_by,
        "reason": reason,
        "changes": changes or {},
        "created_utc": now.isoformat(),
        "expires_utc": expires.isoformat(),
        "status": "active",
    }


def evaluate_emergency_override(override: dict, now_utc: datetime | None = None) -> dict:
    now = now_utc or datetime.now(timezone.utc)
    exp_raw = str(override.get("expires_utc", "")).strip()
    if not exp_raw:
        return {"ok": False, "reason": "missing_expiry"}

    try:
        expires = datetime.fromisoformat(exp_raw.replace("Z", "+00:00"))
    except ValueError:
        return {"ok": False, "reason": "invalid_expiry"}

    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if now >= expires:
        return {
            "ok": False,
            "reason": "override_expired",
            "expires_utc": expires.isoformat(),
            "enforcement": "disable_override_and_require_new_approval",
        }

    return {
        "ok": True,
        "reason": "override_active",
        "expires_utc": expires.isoformat(),
        "minutes_remaining": round((expires - now).total_seconds() / 60.0, 2),
    }
