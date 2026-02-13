# Change Impact

## Request Summary
- Request: Proceed with TBOT-A9 delivery guarantees hardening for agent communications.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add retry backoff for CLI transport attempts.
- Add dead-letter replay tooling for failed comms deliveries.
- Extend audit storage helpers to query dead-letter comms safely.
- Add tests for backoff/dlq query/replay behavior.
- Update board/status docs for TBOT-A9 completion baseline.

## Risk
- Medium: changes delivery behavior in comms bridge.
- Mitigation: bounded retries, explicit dead-letter filtering, deterministic tests.

## Backward Compatibility
- Existing comms APIs remain compatible.

## Security / Performance
- Security: no widening of command permissions.
- Performance: small sleep intervals on retries; configurable.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
