# Change Impact

## Request Summary
- Request: Harden TBOT-A2/A3/A4 governance components and update ticketing accordingly.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- In scope:
  - Upgrade learning recommendations to structured, prioritized output.
  - Add stricter escalation matrix controls for auto-approval tiers.
  - Add drift severity scoring + actionable rollback profile.
  - Wire governance outputs into weekly postmortem.
  - Add tests and Jira/backlog updates.
- Out of scope:
  - Autonomous config mutation in live mode.

## Risk
- Medium: policy logic can affect approval path.
- Mitigation: explicit env gates, deterministic behavior, tests.

## Test Plan
- Unit tests for policy tier gating and drift severity.
- Postmortem generation tests with governance sections.
- Full lint + test suite.

## Rollback Plan
- Revert PR merge commit.
