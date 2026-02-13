# Change Impact

## Request Summary
- Request: Continue with TBOT-A8 by adding observability for agent communication bridge (delivery audit + retry/dead-letter policy).
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add comms audit storage for bridge events.
- Add bounded retry policy for CLI delivery failures.
- Add dead-letter logging when retries are exhausted.
- Wire supervisor bridge with audit logger.
- Add tests for audit logging and dead-letter behavior.
- Update board/status docs to reflect TBOT-A8 baseline completion.

## Risk
- Medium: affects orchestration observability paths.
- Mitigation: additive schema changes, deterministic retry bounds, unit tests.

## Backward Compatibility
- Existing event/decision audit tables remain unchanged.

## Security / Performance
- Security: better traceability of inter-agent messages.
- Performance: small additional SQLite writes for comms events.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
