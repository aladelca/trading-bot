from __future__ import annotations

from src.execution.validation_metrics import compute_validation_metrics, evaluate_validation_alerts


REMEDIATION_MATRIX = {
    "blocked_pretrade_rate_above_threshold": {
        "severity": "medium",
        "owner": "risk",
        "actions": [
            "Inspect top validation reasons by count.",
            "Confirm symbol/session rules against broker policy.",
            "Adjust strategy order templates if reject reasons are expected.",
        ],
    },
    "broker_error_rate_above_threshold": {
        "severity": "high",
        "owner": "broker-integration",
        "actions": [
            "Check broker API status and recent transport failures.",
            "Switch execution posture to conservative routing.",
            "Escalate if retryable errors persist beyond SLA window.",
        ],
    },
    "auto_reverted_rate_above_threshold": {
        "severity": "high",
        "owner": "governance",
        "actions": [
            "Review report_only rollout windows and expiry policy.",
            "Require explicit sign-off before re-entering report_only mode.",
            "Document drift root cause and mitigation in change log.",
        ],
    },
}


def build_validation_anomaly_triage(
    records: list[dict],
    *,
    max_blocked_rate: float = 0.25,
    max_broker_error_rate: float = 0.10,
    max_auto_reverted_rate: float = 0.05,
) -> dict:
    metrics = compute_validation_metrics(records)
    alerts = evaluate_validation_alerts(
        metrics,
        max_blocked_rate=max_blocked_rate,
        max_broker_error_rate=max_broker_error_rate,
        max_auto_reverted_rate=max_auto_reverted_rate,
    )

    findings: list[dict] = []
    for alert in alerts:
        rem = REMEDIATION_MATRIX.get(alert, {"severity": "low", "owner": "ops", "actions": []})
        findings.append(
            {
                "alert": alert,
                "severity": rem["severity"],
                "owner": rem["owner"],
                "actions": rem["actions"],
            }
        )

    severity_rank = {"low": 0, "medium": 1, "high": 2}
    overall = "ok"
    if findings:
        highest = max(findings, key=lambda x: severity_rank.get(x["severity"], 0))
        overall = highest["severity"]

    return {
        "status": "alert" if findings else "ok",
        "overall_severity": overall,
        "metrics": metrics,
        "alerts": alerts,
        "findings": findings,
    }
