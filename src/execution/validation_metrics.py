from __future__ import annotations


def compute_validation_metrics(records: list[dict]) -> dict:
    total = len(records)
    blocked = 0
    warned = 0
    broker_errors = 0
    auto_reverted = 0

    for r in records:
        status = str(r.get("status", "")).lower()
        if status == "blocked" and r.get("rejection_source") == "pre_trade_validation":
            blocked += 1
        if r.get("validation_warning"):
            warned += 1
        if status == "error" and str(r.get("rejection_source", "")).startswith("broker_"):
            broker_errors += 1

        rollout = r.get("rollout") or (r.get("validation_warning") or {}).get("rollout") or {}
        if bool(rollout.get("auto_reverted")):
            auto_reverted += 1

    def pct(x: int) -> float:
        return round((x / total) if total else 0.0, 6)

    return {
        "records_total": total,
        "blocked_pretrade_total": blocked,
        "blocked_pretrade_rate": pct(blocked),
        "warning_report_only_total": warned,
        "warning_report_only_rate": pct(warned),
        "broker_error_total": broker_errors,
        "broker_error_rate": pct(broker_errors),
        "auto_reverted_total": auto_reverted,
        "auto_reverted_rate": pct(auto_reverted),
    }


def evaluate_validation_alerts(
    metrics: dict,
    *,
    max_blocked_rate: float = 0.25,
    max_broker_error_rate: float = 0.10,
    max_auto_reverted_rate: float = 0.05,
) -> list[str]:
    alerts: list[str] = []

    if float(metrics.get("blocked_pretrade_rate", 0.0)) > max_blocked_rate:
        alerts.append("blocked_pretrade_rate_above_threshold")
    if float(metrics.get("broker_error_rate", 0.0)) > max_broker_error_rate:
        alerts.append("broker_error_rate_above_threshold")
    if float(metrics.get("auto_reverted_rate", 0.0)) > max_auto_reverted_rate:
        alerts.append("auto_reverted_rate_above_threshold")

    return alerts
