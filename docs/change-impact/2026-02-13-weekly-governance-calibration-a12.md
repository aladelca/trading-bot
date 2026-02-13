# Change Impact

## Request Summary
- Request: Complete TBOT-A12 weekly governance calibration automation and report artifacting.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add weekly governance calibration report generator.
- Generate markdown artifact with KPI snapshot + threshold ranking.
- Add tests for report generation.
- Update Jira/backlog/status docs to reflect A12 completion and next follow-up.

## Risk
- Low: additive reporting tooling only.

## Backward Compatibility
- No runtime behavior changes in order execution path.

## Security / Performance
- No external network actions; local file/db reads only.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
