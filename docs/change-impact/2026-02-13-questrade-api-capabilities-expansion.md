# Change Impact

## Request Summary
- Request: Review available Questrade APIs and update bot adapter coverage accordingly.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Expand Questrade client capabilities beyond order submit path.
- Add account operations wrappers: balances, positions, executions, activities.
- Add market-data wrappers: quotes and candles.
- Add consolidated account+market snapshot helper for strategy inputs.
- Add CLI utility to fetch a live snapshot from Questrade.
- Add tests for new capability endpoints and data assembly.

## Risk
- Medium: broker integration surface increases, but changes are additive and read-heavy.

## Backward Compatibility
- Backward compatible. Existing order flow and method signatures remain unchanged.

## Security / Performance
- No secret leakage changes; uses existing bearer token path.
- Helps strategy layer rely on broker-native balances/prices/positions instead of ad-hoc assumptions.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
