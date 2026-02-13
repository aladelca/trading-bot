# Change Impact

## Request Summary
- Request: Continue implementation with Telegram callback acknowledgement and safer live-order path with dry-run support.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- In scope:
  - Telegram callback acknowledgement (`answerCallbackQuery`).
  - Track/update Telegram offset through polling function.
  - Add Questrade order submission method guarded by explicit dry-run behavior.
  - Route live execution through guarded broker method.
  - Add tests for callback ack + live dry-run branch.
- Out of scope:
  - Public webhook deployment.
  - Enabling real live trading by default.

## Risk
- Medium: touches approval + execution path.
- Mitigation: fail-safe defaults, tests, and live guardrails remain mandatory.

## Test Plan
- Unit tests for Telegram ack and live dry-run execution.
- Full lint + test suite.

## Rollback Plan
- Revert PR merge commit.
