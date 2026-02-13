from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.storage.audit_log import AuditLogger


def _parse_ts(value: str) -> datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        pass
    try:
        # sqlite CURRENT_TIMESTAMP format
        return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def evaluate_reconciliation(
    versions: list[dict],
    *,
    cadence_days: int = 7,
    stale_pending_hours: int = 72,
    now_utc: datetime | None = None,
) -> dict:
    now = now_utc or datetime.now(timezone.utc)
    parsed: list[dict] = []
    for v in versions:
        ts = _parse_ts(v.get("created_at", ""))
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        parsed.append({**v, "_created": ts})

    if not parsed:
        return {
            "ok": False,
            "reason": "no_versions",
            "overdue_review": True,
            "stale_pending": [],
            "cleanup_plan": [],
        }

    parsed.sort(key=lambda x: x["_created"])
    latest = parsed[-1]
    overdue_cutoff = now - timedelta(days=int(cadence_days))
    overdue_review = latest["_created"] < overdue_cutoff

    stale_cutoff = now - timedelta(hours=int(stale_pending_hours))
    stale_pending = [
        {
            "id": r.get("id"),
            "version_tag": r.get("version_tag"),
            "status": r.get("status"),
            "created_at": r.get("created_at"),
        }
        for r in parsed
        if str(r.get("status", "")).startswith("pending") and r["_created"] < stale_cutoff
    ]

    cleanup_plan = [
        {
            "action": "mark_stale_and_require_revalidation",
            "version_tag": row["version_tag"],
            "id": row["id"],
        }
        for row in stale_pending
    ]

    return {
        "ok": True,
        "reason": "ok",
        "latest_version_tag": latest.get("version_tag"),
        "latest_created_at": latest.get("created_at"),
        "overdue_review": overdue_review,
        "cadence_days": int(cadence_days),
        "stale_pending": stale_pending,
        "cleanup_plan": cleanup_plan,
    }


def run_reconciliation(
    audit: AuditLogger,
    *,
    recommendation_id: str,
    cadence_days: int = 7,
    stale_pending_hours: int = 72,
) -> dict:
    versions = audit.list_governance_versions(recommendation_id=recommendation_id)
    out = evaluate_reconciliation(
        versions,
        cadence_days=cadence_days,
        stale_pending_hours=stale_pending_hours,
    )
    out["recommendation_id"] = recommendation_id
    out["versions_checked"] = len(versions)
    return out
