from __future__ import annotations

from datetime import datetime, timedelta, timezone


def create_emergency_override_multisig(
    *,
    policy_id: str,
    incident_id: str,
    reason: str,
    approvers: list[str],
    min_approvals: int = 2,
    severity: str = "critical",
    override_minutes: int = 30,
    changes: dict | None = None,
) -> dict:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=int(override_minutes))
    return {
        "kind": "governance_emergency_override_multisig",
        "policy_id": policy_id,
        "incident_id": incident_id,
        "reason": reason,
        "severity": severity.lower(),
        "approvers": approvers,
        "min_approvals": int(min_approvals),
        "changes": changes or {},
        "created_utc": now.isoformat(),
        "expires_utc": expires.isoformat(),
        "status": "pending-multisig",
    }


def evaluate_emergency_override_multisig(override: dict, now_utc: datetime | None = None) -> dict:
    now = now_utc or datetime.now(timezone.utc)

    incident_id = str(override.get("incident_id", "")).strip()
    if not incident_id:
        return {"ok": False, "reason": "missing_incident_id"}

    approvers = [str(a).strip().lower() for a in (override.get("approvers") or []) if str(a).strip()]
    min_approvals = int(override.get("min_approvals", 2))
    uniq = sorted(set(approvers))

    if len(uniq) != len(approvers):
        return {"ok": False, "reason": "duplicate_approvers"}

    if min_approvals < 2:
        return {"ok": False, "reason": "min_approvals_too_low", "value": min_approvals}

    if len(uniq) < min_approvals:
        return {
            "ok": False,
            "reason": "insufficient_approvals",
            "have": len(uniq),
            "need": min_approvals,
        }

    exp_raw = str(override.get("expires_utc", "")).strip()
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
            "enforcement": "disable_override_and_require_new_multisig",
        }

    return {
        "ok": True,
        "reason": "override_multisig_active",
        "incident_id": incident_id,
        "approvers": uniq,
        "expires_utc": expires.isoformat(),
        "minutes_remaining": round((expires - now).total_seconds() / 60.0, 2),
    }
