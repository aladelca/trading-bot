# Change Impact

## Request Summary
- Request: Complete BROKER-VALID-4 validation mode drift monitoring + hard-fail auto-revert policy.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add validation rollout monitor that computes effective mode from drift controls.
- Auto-revert report-only mode to enforce when drift window expires.
- Fail-safe to enforce if report-only start timestamp is invalid/missing under strict settings.
- Add tests for drift expiration and fail-safe behavior.
- Update board/status docs for BROKER-VALID-4 completion.

## Risk
- Medium: may unexpectedly enforce validation if envs are misconfigured.
- Mitigation: explicit telemetry fields and deterministic fail-safe defaults.

## Backward Compatibility
- Existing `BROKER_VALIDATION_MODE=enforce` behavior unchanged.

## Security / Performance
- Strengthens safety posture by limiting prolonged report-only exposure.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
