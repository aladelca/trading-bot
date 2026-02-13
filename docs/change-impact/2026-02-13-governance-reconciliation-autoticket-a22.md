# Change Impact

## Request Summary
- Request: Complete TBOT-A22 governance reconciliation drift auto-ticketing + owner assignment.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add auto-ticket generation for governance reconciliation findings.
- Add owner assignment matrix for overdue review and stale pending cleanup.
- Add CLI helper to generate ticket artifacts from reconciliation result.
- Add tests for overdue/stale ticket generation and owner mapping.
- Update docs/status tracking and queue next follow-up.

## Risk
- Low: additive governance reporting automation.

## Backward Compatibility
- Fully additive.

## Security / Performance
- Improves accountability with deterministic owner routing for governance hygiene findings.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
