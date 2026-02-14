# Change Impact

## Request Summary
- Request: Complete WEBHOOK-HARDEN-8 provider ack verification and receipt tamper validation pipeline.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add receipt verification helpers (signature check + provider ack validation).
- Add tamper-detection pipeline for saved receipt artifacts.
- Add CLI utility for validating receipt directory integrity.
- Add tests for valid receipts, signature mismatch, and missing provider ack metadata.
- Update docs/status and queue next follow-up.

## Risk
- Low: additive integrity checks for delivery receipts.

## Backward Compatibility
- Additive only.

## Security / Performance
- Improves webhook operations integrity by validating receipt authenticity and provider metadata completeness.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
