# Change Impact

## Request Summary
- Request: Continue implementation by closing two major v1 gaps: Questrade symbolId resolution and portfolio ledger tracking.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- In scope:
  - Add symbol lookup (`symbolId`) before non-dry-run live order submission.
  - Block live order submission if symbolId cannot be resolved.
  - Add portfolio ledger storage and trade metrics.
  - Integrate ledger recording in orchestrator execution path.
  - Extend KPI report with ledger metrics.
- Out of scope:
  - Full PnL mark-to-market and unrealized PnL engine.
  - Webhook deployment.

## Risk
- Medium: touches live order path and persistence behavior.
- Mitigation: safe blocking behavior + tests + dry-run default.

## Test Plan
- Unit tests for symbolId resolution and blocked live submit path.
- Unit tests for ledger write/stats.
- Full lint + test suite.

## Rollback Plan
- Revert PR merge commit.
