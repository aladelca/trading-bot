# Change Impact

## Request Summary
- Request: Complete TBOT-A13 scheduled governance calibration delivery (cron + channel routing baseline).
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add scheduled delivery runner that generates weekly calibration artifact and delivery manifest.
- Add cron install helper script for host scheduling.
- Add docs for channel routing envs and cron usage.
- Add tests for manifest generation.
- Update Jira/backlog/status for A13 completion and next workflow item.

## Risk
- Low: additive scheduling/delivery tooling; no live-order path change.

## Backward Compatibility
- Existing reporting paths remain unchanged.

## Security / Performance
- No outbound send by default; delivery is manifest-based and operator-controlled.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`
- `bash -n scripts/deploy/install_governance_calibration_cron.sh`

## Rollback Plan
- Revert PR merge commit.
