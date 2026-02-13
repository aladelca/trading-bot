# Change Impact

## Request Summary
- Request: Complete BROKER-VALID-5 broker validation rollout metrics dashboard + alert thresholds.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add metrics aggregator for broker validation/rejection outcomes.
- Add threshold-based alert evaluator for rejection rates and mode-drift signals.
- Add CLI dashboard runner for JSON records input.
- Add tests for metric calculations and alert triggers.
- Update Jira/backlog/status docs to mark BROKER-VALID-5 completion.

## Risk
- Low: analytics-only tooling; no order path mutation.

## Backward Compatibility
- Fully additive.

## Security / Performance
- Improves visibility into validation rollout quality.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
