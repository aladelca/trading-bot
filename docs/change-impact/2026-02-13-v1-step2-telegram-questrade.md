# Change Impact

## Request Summary
- Request: Continue implementation with Telegram approval flow wiring and Questrade auth/account integration primitives.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- In scope:
  - Telegram client for approval requests with inline buttons.
  - Approval gate integration with timeout-based decision polling.
  - Questrade auth/token refresh and account/balance retrieval helpers.
  - Questrade order payload builder for future live routing.
  - Unit tests for Telegram decision parsing and Questrade token handling.
- Out of scope:
  - Public webhook endpoint deployment.
  - Live order execution against brokerage account.

## Affected Components
- `src/telegram/*`, `src/broker/questrade/*`, `src/config/settings.py`, `README.md`, `tests/*`

## Impact Analysis
- Functional impact:
  - Moves approval and broker integration from stubs toward operational adapters.
- Backward compatibility:
  - Keeps paper mode default; no forced live behavior.
- Security impact:
  - Uses env vars for secrets; no credentials in code.
- Performance impact:
  - Small HTTP overhead only when approvals are requested.
- Operational impact:
  - Enables realistic end-to-end testing with credentials later.

## Risk Assessment
- Risk level: Medium
- Main risks:
  - Telegram polling can miss updates if offsets are mishandled.
  - Token refresh failures if Questrade credentials are invalid.
- Mitigations:
  - Explicit update offset handling.
  - Graceful fallback behavior and tests.

## Test Plan
- Unit tests for:
  - Telegram callback parsing and approval decisions.
  - Questrade token response handling.
  - Approval gate fallback logic when Telegram is unavailable.

## Rollback Plan
- Revert PR merge commit.

## Sign-off
- Ready for implementation: Yes
