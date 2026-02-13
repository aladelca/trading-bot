# Change Impact

## Request Summary
- Request: Proceed with TBOT-A7 by adding practical CLI transport for agent-to-agent communication.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Extend `AgentSessionBridge` with `cli` transport path.
- Enforce command allow-list and timeout controls for CLI execution.
- Add env-driven settings for enabling CLI transport and command policy.
- Add tests for allow-list pass/fail and execution behavior.
- Update board/status docs for TBOT-A7 progression.

## Risk
- Medium: shell execution can be sensitive.
- Mitigation: disabled by default, explicit allow-list, no shell mode, timeout-bound execution.

## Backward Compatibility
- Existing session-bridge behavior remains intact.

## Security / Performance
- Security: command execution restricted by `AGENT_CLI_ALLOWED_COMMANDS`.
- Performance: bounded with configurable timeout.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`
- Unit tests for CLI transport success, blocked command, and disabled mode.

## Rollback Plan
- Revert PR merge commit.
