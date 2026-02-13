from __future__ import annotations


def detect_metric_drift(current: dict, baseline: dict) -> list[str]:
    alerts: list[str] = []

    curr_approval = float(current.get("approval_rate", 0.0))
    base_approval = float(baseline.get("approval_rate", curr_approval))
    if curr_approval < base_approval - 0.15:
        alerts.append("Approval rate drifted down significantly.")

    curr_pnl = float(current.get("equity_pnl_total", 0.0))
    base_pnl = float(baseline.get("equity_pnl_total", curr_pnl))
    if curr_pnl < base_pnl - abs(base_pnl * 0.2 + 1.0):
        alerts.append("Equity PnL deteriorated versus baseline.")

    curr_rej = int(current.get("signals_rejected", 0))
    base_rej = int(baseline.get("signals_rejected", curr_rej))
    if curr_rej > base_rej * 1.5 + 5:
        alerts.append("Signal rejection volume increased materially.")

    return alerts


def drift_severity(alerts: list[str]) -> str:
    if not alerts:
        return "none"
    if len(alerts) == 1:
        return "low"
    if len(alerts) == 2:
        return "medium"
    return "high"


def rollback_recommendation(alerts: list[str]) -> str:
    severity = drift_severity(alerts)
    if severity == "none":
        return "No rollback needed. Continue monitoring."
    if severity == "low":
        return "Recommend cautious rollback review and temporary risk reduction."
    if severity == "medium":
        return "Recommend rollback to last known stable config and keep paper-mode active."
    return "Immediate rollback recommended; disable live mode and enforce manual approvals only."
