from __future__ import annotations

from datetime import datetime, timezone


ISO_SUFFIX = "Z"


def _parse_iso_utc(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v:
        return None
    if v.endswith(ISO_SUFFIX):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def resolve_validation_mode(
    *,
    configured_mode: str,
    report_only_since_utc: str,
    report_only_max_minutes: int,
    auto_revert_enabled: bool,
    now_utc: datetime | None = None,
) -> dict:
    mode = (configured_mode or "enforce").strip().lower()
    now = now_utc or datetime.now(timezone.utc)

    if mode != "report_only":
        return {
            "configured_mode": mode,
            "effective_mode": mode,
            "auto_reverted": False,
            "reason": "configured_non_report_only",
        }

    start = _parse_iso_utc(report_only_since_utc)
    if start is None:
        if auto_revert_enabled:
            return {
                "configured_mode": mode,
                "effective_mode": "enforce",
                "auto_reverted": True,
                "reason": "invalid_or_missing_report_only_since",
            }
        return {
            "configured_mode": mode,
            "effective_mode": "report_only",
            "auto_reverted": False,
            "reason": "missing_report_only_since_no_auto_revert",
        }

    elapsed_min = (now - start).total_seconds() / 60.0
    if auto_revert_enabled and report_only_max_minutes > 0 and elapsed_min >= report_only_max_minutes:
        return {
            "configured_mode": mode,
            "effective_mode": "enforce",
            "auto_reverted": True,
            "reason": "report_only_window_expired",
            "elapsed_minutes": round(elapsed_min, 2),
        }

    return {
        "configured_mode": mode,
        "effective_mode": "report_only",
        "auto_reverted": False,
        "reason": "report_only_within_window",
        "elapsed_minutes": round(elapsed_min, 2),
    }
