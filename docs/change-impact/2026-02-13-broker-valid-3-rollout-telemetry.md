# Change Impact

## Request Summary
- Request: Complete BROKER-VALID-3 with rollout toggles and broker-side rejection telemetry.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add validation rollout mode toggle (`enforce|report_only`).
- Add structured telemetry fields for pre-trade and broker-side rejections.
- Preserve fail-safe default (enforce).
- Add tests for report-only behavior and telemetry output.
- Update board/status docs to mark BROKER-VALID-3 complete.

## Risk
- Medium: report-only mode could allow orders that validation would block.
- Mitigation: default remains `enforce`; explicit warnings emitted in output.

## Backward Compatibility
- Existing behavior preserved under default mode.

## Security / Performance
- Better observability for rejection causes; no meaningful performance cost.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
