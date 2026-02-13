# Change Impact

## Request Summary
- Request: Complete TBOT-A15 governance recommendation application guardrails + rollback template.
- Owner: Adrian
- Date: 2026-02-13

## Scope
- Add guardrail evaluator before applying governance recommendation decisions.
- Enforce mandatory fields and safe ranges for confidence/tier settings.
- Add rollback plan template generator from approved recommendation packages.
- Add tests for guardrail pass/fail and rollback template output.
- Update Jira/backlog/status docs to mark A15 completion.

## Risk
- Medium: guardrails gate recommendation application behavior.
- Mitigation: strict validation, explicit failure reasons, additive tooling only.

## Backward Compatibility
- Existing recommendation approval workflow remains intact.

## Security / Performance
- Prevents unsafe policy application ranges.

## Test Plan
- `ruff check .`
- `PYTHONPATH=. pytest -q`

## Rollback Plan
- Revert PR merge commit.
