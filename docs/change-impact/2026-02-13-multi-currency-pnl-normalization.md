# Change Impact

## Request Summary
- Request: Implement multi-currency PnL normalization baseline.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add currency field to portfolio ledger trades.
- Normalize realized/unrealized PnL to configurable base currency using FX rates.
- Extend PnL report to accept base currency + FX map.
- Add tests for mixed-currency normalization.

## Risk
- Medium: currency conversion assumptions can misstate PnL if rates are stale.
- Mitigation: explicit fx_rates input and deterministic fallback behavior.

## Test Plan
- Unit tests for mixed USD/CAD PnL normalization.
- Backward-compatibility tests for default currency behavior.
- Full lint + tests.

## Rollback Plan
- Revert PR merge commit.
