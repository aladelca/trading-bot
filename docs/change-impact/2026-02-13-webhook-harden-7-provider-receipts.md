# Change Impact

## Request Summary
- Request: Complete WEBHOOK-HARDEN-7 delivery connector integration to provider + signed delivery receipts.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Extend alert delivery connector with provider integration abstraction.
- Generate delivery receipts for sent alerts.
- Sign receipts with HMAC SHA-256 when signing key is configured.
- Extend runner CLI with provider and signing-key options.
- Add tests for signed receipt generation and failure dead-letter behavior.
- Update status docs/backlog and queue next follow-up.

## Risk
- Low/Medium: operational delivery metadata path only.

## Backward Compatibility
- Additive; prior behavior preserved with local/default provider.

## Security / Performance
- Signed receipts improve delivery audit integrity.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
