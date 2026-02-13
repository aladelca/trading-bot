from datetime import datetime, timezone

from src.execution.validation_rollout import resolve_validation_mode


def test_report_only_auto_reverts_after_window():
    out = resolve_validation_mode(
        configured_mode="report_only",
        report_only_since_utc="2026-02-13T00:00:00+00:00",
        report_only_max_minutes=60,
        auto_revert_enabled=True,
        now_utc=datetime(2026, 2, 13, 2, 0, tzinfo=timezone.utc),
    )
    assert out["effective_mode"] == "enforce"
    assert out["auto_reverted"] is True


def test_report_only_stays_when_within_window():
    out = resolve_validation_mode(
        configured_mode="report_only",
        report_only_since_utc="2026-02-13T00:00:00+00:00",
        report_only_max_minutes=180,
        auto_revert_enabled=True,
        now_utc=datetime(2026, 2, 13, 1, 0, tzinfo=timezone.utc),
    )
    assert out["effective_mode"] == "report_only"
    assert out["auto_reverted"] is False
