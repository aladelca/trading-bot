# Change Impact

## Request Summary
- Request: Continue with webhook deployment hardening baseline (server/worker resilience improvements).
- Owner: Adrian
- Date: 2026-02-13

## Scope
- In scope:
  - Add queue-claim semantics (pending -> in_progress) in callback store.
  - Add retry/fail state tracking (`attempts`, `last_error`, `processing_state`).
  - Add webhook payload size guard and health endpoint.
  - Keep webhook ACK fast by enqueue-only server behavior.
  - Add tests for retry/fail transitions and processor error handling.
- Out of scope:
  - Public DNS/TLS final rollout.

## Risk
- Medium: callback handling state changes.
- Mitigation: idempotent keys, bounded retry logic, explicit state transitions.

## Test Plan
- Unit tests for callback state transitions and processor failure path.
- Full lint + test suite.

## Rollback Plan
- Revert PR merge commit.
