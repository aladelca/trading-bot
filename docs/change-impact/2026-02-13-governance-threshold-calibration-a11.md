# Change Impact

## Request Summary
- Request: Implement TBOT-A11 governance threshold calibration with scenario replay packs.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add calibration module that evaluates candidate confidence thresholds against replay scenarios.
- Add CLI runner to calibrate and output recommended threshold candidates.
- Add sample replay pack JSON for deterministic local calibration.
- Add tests for calibration scoring and recommendation ordering.
- Update board/status docs to reflect TBOT-A11 baseline completion.

## Risk
- Low/Medium: additive tooling; no direct order-execution behavior changes.

## Backward Compatibility
- Existing simulation/runtime paths remain unchanged.

## Security / Performance
- No external calls; local JSON processing only.
- Computationally lightweight over small replay packs.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`
- Unit tests for threshold calibration behavior.

## Rollback Plan
- Revert PR merge commit.
