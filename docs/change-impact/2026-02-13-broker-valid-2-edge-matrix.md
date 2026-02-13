# Change Impact

## Request Summary
- Request: Execute BROKER-VALID-2 broker-specific edge-case matrix expansion.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Extend order validation matrix with side/symbol sanitation and quantity caps.
- Add Questrade-specific edge constraints for extended-hours submits.
- Ensure submit path blocks invalid requests before network.
- Add tests for new matrix paths.
- Update Jira/backlog/status docs for BROKER-VALID-2 completion baseline.

## Risk
- Medium: stricter validation may block previously accepted orders.
- Mitigation: deterministic rules + explicit test coverage + clear reasons.

## Backward Compatibility
- Existing valid market/limit flows remain unchanged.

## Security / Performance
- Security: prevents malformed order payload classes from leaving process.
- Performance: negligible; pure local validation checks.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
