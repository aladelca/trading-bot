from __future__ import annotations

from datetime import datetime, timedelta, timezone


def create_drift_ack(
    *,
    policy_id: str,
    severity: str,
    acknowledged_by: str,
    valid_for_minutes: int = 60,
) -> dict:
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=int(valid_for_minutes))
    return {
        "policy_id": policy_id,
        "severity": severity.lower(),
        "acknowledged_by": acknowledged_by,
        "acknowledged_utc": now.isoformat(),
        "expires_utc": expires.isoformat(),
        "status": "active",
    }


def evaluate_drift_ack(ack: dict, now_utc: datetime | None = None) -> dict:
    now = now_utc or datetime.now(timezone.utc)
    exp_raw = str(ack.get("expires_utc", "")).strip()
    try:
        exp = datetime.fromisoformat(exp_raw.replace("Z", "+00:00"))
    except ValueError:
        return {"ok": False, "reason": "invalid_expiry"}

    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)

    if now >= exp:
        return {"ok": False, "reason": "ack_expired", "expires_utc": exp.isoformat()}

    return {
        "ok": True,
        "reason": "ack_active",
        "expires_utc": exp.isoformat(),
        "minutes_remaining": round((exp - now).total_seconds() / 60.0, 2),
    }
