# Change Impact

## Request Summary
- Request: Complete TBOT-A5 governance threshold tuning based on paper metrics.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add policy-tuning module that recommends confidence threshold and allowed tiers using KPI inputs.
- Add CLI runner for tuning from KPI JSON.
- Add tests for conservative/aggressive tuning outcomes.
- Update board/status/backlog and docs for A5 completion.

## Risk
- Medium: recommendations can influence future governance configs.
- Mitigation: recommendation-only output (no autonomous apply), conservative guardrails.

## Backward Compatibility
- No existing runtime behavior changes.

## Security / Performance
- Offline calculations only; no external calls.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
