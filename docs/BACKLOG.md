# Product Backlog (Prioritized)

## P1 (High)
1. **TBOT-A15** - Governance recommendation application guardrails + rollback template
2. **TBOT-A16** - Governance recommendation audit and versioning ledger
3. **BROKER-VALID-4** - Validation mode drift monitoring + hard-fail auto-revert policy
4. **WEBHOOK-HARDEN-5** - Automated evidence upload + incident alert routing

## P2 (Medium)
6. **TBOT-A8** - Agent communication observability (delivery audit + retry/dead-letter policy)
7. Multi-currency PnL live FX feed + cross-rate validation
8. Weekly postmortem scheduler + distribution channel integration
9. Policy simulation sandbox for approval/risk changes

## Completed Recently
- **WEBHOOK-HARDEN-4** - Host evidence + incident automation baseline
  - Evidence capture script (`scripts/deploy/capture_webhook_evidence.sh`)
  - Incident report generator (`apps/telegram_webhook/incident_report.py`)
  - Cutover checklist acceptance criteria updated with evidence + incident outputs
- **BROKER-VALID-3** - Validation rollout toggles + rejection telemetry baseline
  - Added `BROKER_VALIDATION_MODE` (`enforce|report_only`)
  - Added pre-trade rejection source metadata
  - Added broker-side rejection telemetry payloads for API/transport failures
- **TBOT-A14** - Governance recommendation approval workflow baseline
  - Human decision states: accept / reject / change-set
  - Workflow CLI for explicit decision artifacts
  - Unit tests for approval path variants
- **TBOT-A13** - Scheduled governance calibration delivery baseline
  - Scheduled delivery manifest generator (`apps/backtester/scheduled_governance_delivery.py`)
  - Cron install helper (`scripts/deploy/install_governance_calibration_cron.sh`)
  - Delivery routing envs and manifest tests
- **WEBHOOK-HARDEN-3** - VPS cutover validation baseline
  - Host-side cutover validation script (`scripts/deploy/validate_webhook_cutover.sh`)
  - Go/no-go acceptance checklist (`docs/webhook-cutover-checklist.md`)
  - Runbook/deployment integration for cutover gating
- **BROKER-VALID-2** - Broker-specific edge-case matrix expansion baseline
  - Added side/symbol sanitation and hard quantity caps
  - Added Questrade extended-hours edge rules with explicit block reasons
  - Added validation coverage in matrix and submit-path tests
- **TBOT-A5** - Governance threshold tuning baseline from paper KPIs
  - Heuristic tuning recommendations for min confidence and allowed tiers
  - CLI runner for KPI-driven recommendation generation
  - Unit tests for conservative/opportunistic profiles
- **TBOT-A12** - Weekly governance calibration automation baseline
  - Weekly markdown report generator (`apps/backtester/weekly_governance_calibration.py`)
  - Includes KPI snapshot + threshold ranking artifact
  - Test coverage for artifact generation flow
- **TBOT-A11** - Governance threshold calibration baseline
  - Replay-pack evaluator for candidate confidence thresholds
  - CLI calibration runner (`apps/backtester/threshold_calibration.py`)
  - Sample replay pack + tests for ranking outcomes
- **TBOT-A10** - Governance policy simulation sandbox baseline
  - What-if simulator for approval tier policy and drift severity outcomes
  - CLI runner for scenario inputs (`apps/backtester/policy_simulation.py`)
  - Unit tests for policy decisions and drift/recommendation outputs
- **TBOT-A9** - Agent communication delivery guarantees baseline
  - Retry backoff control for CLI transport
  - Dead-letter query helpers in audit storage
  - DLQ replay tool (`apps/orchestrator/agent_cli_dlq_replay.py`)
- **TBOT-A8** - Agent communication observability baseline
  - Persisted comms audit events (`comms_events`) in audit DB
  - CLI retry policy with dead-letter tagging on exhausted attempts
  - Comms observability tests (ok/blocked/error counts)
- **TBOT-A7** - Agent communication bridge implementation baseline
  - Route allow-list enforcement and correlation IDs
  - CLI transport support with explicit command allow-list and timeout
  - Manual CLI bridge runner (`apps/orchestrator/agent_cli_bridge.py`)
- **TBOT-A6** - Agent communication bridge design baseline
  - Extended stage envelope contract with source/target/transport/correlation
  - Defined Sprint-3 comms track and protocol expectations
- **WEBHOOK-HARDEN-2** - Production rollout assets
  - Nginx production TLS template
  - systemd service units for server + worker
  - TLS bootstrap and webhook healthcheck scripts
  - host rollout checklist in deployment guide
- **TBOT-A2/A3/A4** - Governance hardening baseline
  - Structured learning recommendations
  - Tier-aware auto-approve escalation controls
  - Drift severity + rollback profile recommendations
- **PNL-FX-1** - Multi-currency PnL normalization baseline
- **TBOT-15** - Weekly postmortem automation baseline
- **WEBHOOK-HARDEN-1** - Deployment hardening baseline
  - Nginx reverse-proxy template
  - Docker compose scaffold (server + worker + nginx)
  - Async webhook worker polling queue
- **TBOT-14** - Advanced PnL engine baseline
- **TBOT-13** - Broker hardening matrix baseline
- **TBOT-12** - Production-style Telegram webhook baseline

## Definition of Ready (ticket)
- Clear objective
- Acceptance criteria
- Risks and rollback note
- Test strategy

## Definition of Done (ticket)
- Code merged
- Tests green
- Docs updated
- Ops impact documented
