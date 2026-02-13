# Change Impact

## Request Summary
- Request: Implement TBOT-13 broker hardening matrix (error taxonomy, retries/backoff, idempotency keys).
- Owner: Adrian
- Date: 2026-02-13

## Scope
- In scope:
  - Define broker error classification (retryable/fatal/blocked).
  - Add retry policy with bounded exponential backoff.
  - Add idempotency key generation and propagation for live submit path.
  - Add tests for classification and retry behavior.
- Out of scope:
  - Broker-specific SLA tuning by market regime.

## Risk
- Medium: execution path behavior changes.
- Mitigation: bounded retries, safe defaults, tests.

## Test Plan
- Unit tests for taxonomy and retry policy.
- Integration-style tests for submit_order retry flow using mocked responses.
- Full lint + tests.

## Rollback Plan
- Revert PR merge commit.
