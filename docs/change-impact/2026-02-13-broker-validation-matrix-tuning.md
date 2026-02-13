# Change Impact

## Request Summary
- Request: Continue with broker validation matrix tuning by order type/session.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add pre-submit validation matrix for order type + session constraints.
- Enforce quantity and symbol checks before broker submit.
- Integrate validation into live submit path with explicit blocked reasons.
- Add tests for matrix behavior.

## Risk
- Medium: can block orders unexpectedly if misconfigured.
- Mitigation: deterministic rules + tests + clear reasons.

## Test Plan
- Unit tests for valid/invalid order combinations.
- Integration-style test for blocked submit response.
- Full lint + tests.

## Rollback Plan
- Revert PR merge commit.
