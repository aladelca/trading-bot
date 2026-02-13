# Change Impact

## Request Summary
- Request: Proceed with agent communication capability so assistant can communicate with a new agent via CLI/session bridge; reflect activities on board.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add agent communication bridge skeleton with route allow-list and correlation IDs.
- Extend stage envelope contract with source/target/transport/correlation metadata.
- Integrate a baseline handoff in supervisor flow.
- Add tests for comms bridge + updated envelope contract.
- Update Jira/backlog/status to reflect TBOT-A6 done and TBOT-A7 in progress.

## Risk
- Medium: affects agent orchestration contracts.
- Mitigation: preserve backwards compatibility via defaults and add unit tests.

## Backward Compatibility
- Existing envelope builders remain compatible due to defaults.

## Security/Performance
- Adds explicit route allow-list at communication layer for least privilege.
- No external I/O introduced in this baseline.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
