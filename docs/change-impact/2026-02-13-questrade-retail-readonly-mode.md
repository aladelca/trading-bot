# Change Impact

## Request Summary
- Request: Treat Questrade integration as normal retail client mode (read-only API for bot execution).
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add account-mode control for Questrade (`retail_read_only|partner_trading`).
- Block live order submission when account mode is retail read-only.
- Add recommendation trade ticket artifact helper for manual execution.
- Add CLI helper to emit trade tickets.
- Add tests for retail block and ticket generation.
- Update docs/status/backlog.

## Risk
- Low: safer default, fail-closed for live submission.

## Backward Compatibility
- Additive; partner mode can preserve prior submit behavior.

## Security / Performance
- Reduces execution risk by preventing unsupported live API trade attempts.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
