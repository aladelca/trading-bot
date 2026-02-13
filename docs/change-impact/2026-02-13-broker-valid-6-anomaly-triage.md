# Change Impact

## Request Summary
- Request: Complete BROKER-VALID-6 broker validation anomaly triage playbook + remediation matrix.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add anomaly triage evaluator using validation alert outputs and metrics context.
- Add remediation matrix with severity, owner, and runbook actions.
- Add CLI helper to generate triage reports from records JSON.
- Add tests for high-severity and informational triage outcomes.
- Update Jira/backlog/implementation docs and queue next follow-up.

## Risk
- Low: additive reporting and operational guidance only.

## Backward Compatibility
- Fully additive.

## Security / Performance
- Improves operational safety by mapping anomalies to deterministic remediation actions.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
