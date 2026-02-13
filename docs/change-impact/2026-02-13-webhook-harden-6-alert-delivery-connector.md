# Change Impact

## Request Summary
- Request: Complete WEBHOOK-HARDEN-6 alert delivery connector + retry policy for routing manifests.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add manifest delivery connector with bounded retries.
- Add dead-letter output for exhausted delivery attempts.
- Add CLI tool to process pending alert manifests from delivery directory.
- Add tests for retry success and dead-letter outcomes.
- Update board/status docs for WEBHOOK-HARDEN-6 completion.

## Risk
- Low/Medium: operational artifact processing only.

## Backward Compatibility
- Existing evidence/alert manifest generation remains unchanged.

## Security / Performance
- No external provider calls by default; connector remains dry-run/file-based unless endpoint configured.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
