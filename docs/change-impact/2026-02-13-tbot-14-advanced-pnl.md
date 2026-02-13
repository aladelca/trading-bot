# Change Impact

## Request Summary
- Request: Implement TBOT-14 advanced PnL baseline (realized/unrealized, avg cost, mark-to-market snapshots).
- Owner: Adrian
- Date: 2026-02-13

## Scope
- In scope:
  - Add portfolio PnL engine on top of trade ledger.
  - Compute per-symbol position, avg cost, realized PnL.
  - Compute unrealized PnL from mark prices.
  - Add snapshot persistence for equity/PnL time series.
  - Expose PnL summary in KPI report path.
- Out of scope:
  - Broker-native fills reconciliation.
  - Corporate actions and multi-currency FX normalization.

## Risk
- Medium: financial math correctness.
- Mitigation: deterministic formulas + targeted tests.

## Test Plan
- Unit tests for long/short transitions and realized/unrealized outputs.
- Snapshot persistence test.
- Full lint + tests.

## Rollback Plan
- Revert PR merge commit.
