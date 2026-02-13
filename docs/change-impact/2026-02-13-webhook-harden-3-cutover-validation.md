# Change Impact

## Request Summary
- Request: Complete WEBHOOK-HARDEN-3 with VPS cutover validation assets.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add executable cutover checklist for DNS/TLS/systemd/webhook registration verification.
- Add host-ready validation script to check service health, TLS endpoint, and queue state.
- Extend deployment/runbook docs with explicit go/no-go acceptance criteria.
- Update Jira/backlog/status docs to mark WEBHOOK-HARDEN-3 baseline complete.

## Risk
- Low/Medium: operational scripts/docs only; host execution still controlled manually.

## Backward Compatibility
- No trading/runtime logic changes.

## Security / Performance
- Reinforces secure cutover gates and rollback path.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`
- Shell sanity check scripts (`bash -n`).

## Rollback Plan
- Revert PR merge commit.
