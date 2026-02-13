# Governance Change Deployment Checklist (TBOT-A17)

## Preconditions
- Recommendation package is approved (`approved` or `approved-with-changes`).
- Guardrail evaluator returns `ok=true`.
- Rollback template generated and reviewed.

## Mandatory Sign-off Matrix
- `risk_owner_approved`
- `ops_owner_approved`
- `rollback_plan_attached`
- `kpi_snapshot_attached`
- `dry_run_validation_passed`

## Release Steps
1. Capture current policy values and store as rollback baseline.
2. Apply approved governance config changes in controlled environment.
3. Validate dry-run behavior and policy metrics.
4. Obtain final risk+ops sign-off.
5. Promote to scheduled/live policy context.

## Abort Conditions
- Any missing mandatory gate.
- Drift severity `high` without explicit override.
- Missing rollback artifact.

## Post-Deployment Verification
- Re-run KPI report and drift detector.
- Confirm no unexpected increase in rejected/failed governance actions.
- Attach verification summary to governance ledger entry.
