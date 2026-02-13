# Change Impact

## Request Summary
- Request: Complete TBOT-A18 governance policy drift acknowledgements + expiry controls.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add governance drift acknowledgement model with expiry checks.
- Add CLI helper to create/evaluate acknowledgement payloads.
- Add tests for valid and expired acknowledgements.
- Update board/status docs for A18 completion and next follow-up.

## Risk
- Low: additive governance process tooling.

## Backward Compatibility
- No runtime execution changes.

## Security / Performance
- Ensures stale acknowledgements cannot be treated as valid indefinitely.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
