from src.execution.validation_remediation import build_remediation_hooks, execute_remediation_hooks


def test_build_remediation_hooks_from_triage_findings():
    triage = {
        "findings": [
            {"alert": "broker_error_rate_above_threshold", "owner": "broker-integration", "severity": "high"},
            {"alert": "blocked_pretrade_rate_above_threshold", "owner": "risk", "severity": "medium"},
        ]
    }
    hooks = build_remediation_hooks(triage)
    assert len(hooks) == 2
    assert hooks[0]["hook"].startswith("runbook.")


def test_execute_remediation_hooks_dry_run_and_execute_modes():
    hooks = [{"hook": "runbook.validation.inspect_pretrade_blocks", "alert": "blocked_pretrade_rate_above_threshold"}]
    dry = execute_remediation_hooks(hooks, dry_run=True)
    live = execute_remediation_hooks(hooks, dry_run=False)
    assert dry[0]["status"] == "planned"
    assert dry[0]["executed"] is False
    assert live[0]["status"] == "executed"
    assert live[0]["executed"] is True
