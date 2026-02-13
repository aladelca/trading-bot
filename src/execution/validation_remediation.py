from __future__ import annotations

from datetime import datetime, timezone

HOOK_REGISTRY = {
    "blocked_pretrade_rate_above_threshold": "runbook.validation.inspect_pretrade_blocks",
    "broker_error_rate_above_threshold": "runbook.broker.escalate_transport_api_errors",
    "auto_reverted_rate_above_threshold": "runbook.governance.require_rollout_signoff",
}


def build_remediation_hooks(triage: dict) -> list[dict]:
    hooks: list[dict] = []
    for finding in triage.get("findings", []):
        alert = str(finding.get("alert", ""))
        hook_name = HOOK_REGISTRY.get(alert)
        if not hook_name:
            continue
        hooks.append(
            {
                "hook": hook_name,
                "alert": alert,
                "owner": finding.get("owner", "ops"),
                "severity": finding.get("severity", "low"),
                "created_utc": datetime.now(timezone.utc).isoformat(),
            }
        )
    return hooks


def execute_remediation_hooks(hooks: list[dict], *, dry_run: bool = True) -> list[dict]:
    out: list[dict] = []
    for h in hooks:
        if dry_run:
            out.append({**h, "status": "planned", "executed": False})
        else:
            out.append({**h, "status": "executed", "executed": True})
    return out
