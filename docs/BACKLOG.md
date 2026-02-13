# Product Backlog (Prioritized)

## P1 (High)
1. **BROKER-VALID-6** - Broker validation anomaly triage playbook + remediation matrix
2. **WEBHOOK-HARDEN-7** - Delivery connector integration to provider + signed delivery receipts
3. **TBOT-A21** - Governance emergency override multi-signature approvals + incident linkage
4. **TBOT-A22** - Governance reconciliation drift auto-ticketing + owner assignment

## P2 (Medium)
6. **TBOT-A8** - Agent communication observability (delivery audit + retry/dead-letter policy)
7. Multi-currency PnL live FX feed + cross-rate validation
8. Weekly postmortem scheduler + distribution channel integration
9. Policy simulation sandbox for approval/risk changes

## Completed Recently
- **TBOT-A20** - Governance reconciliation review cadence + stale decision cleanup baseline
  - Reconciliation evaluator for policy review cadence compliance
  - Stale pending decision detection with cleanup-plan artifacts
  - CLI helper + tests for overdue and stale detection behavior
- **BROKER-API-1** - Questrade API capability expansion baseline
  - Added wrappers for balances, positions, executions, activities, quotes, candles
  - Added account+market snapshot helper CLI for strategy inputs
  - Added endpoint behavior tests for expanded API surface
- **TBOT-A19** - Governance emergency override protocol + expiry enforcement baseline
  - Emergency override artifact generator with explicit operator/severity/reason fields
  - Expiry evaluator with strict disable-on-expiry enforcement signal
  - CLI helper + tests for active/expired/invalid override lifecycle paths
- **WEBHOOK-HARDEN-6** - Alert delivery connector + retry policy baseline
  - Delivery connector for incident alert manifests
  - Retry + dead-letter handling for exhausted attempts
  - CLI runner + tests for sent/dead-letter outcomes
- **BROKER-VALID-5** - Validation rollout metrics dashboard + alert thresholds baseline
  - Metrics aggregator for pre-trade blocks, warnings, broker errors, auto-reverts
  - Threshold alert evaluator and dashboard CLI
  - Unit tests for metrics and alert triggers
- **TBOT-A18** - Governance drift acknowledgement + expiry controls baseline
  - Drift acknowledgement payload generator
  - Expiry evaluator with active/expired outcomes
  - CLI helper + tests for ack lifecycle checks
- **TBOT-A17** - Governance deployment checklist + sign-off matrix baseline
  - Mandatory deployment gates and abort conditions documented
  - Sign-off matrix evaluator CLI
  - Unit tests for ready/block outcomes
- **WEBHOOK-HARDEN-5** - Automated evidence upload + incident alert routing baseline
  - Evidence manifest generator from captured snapshots
  - Incident alert routing manifest generator (channel/target/severity)
  - Unified evidence-alert pipeline + tests
- **BROKER-VALID-4** - Validation mode drift monitor + hard-fail auto-revert baseline
  - Added report-only expiry controls with fail-safe revert to enforce mode
  - Added rollout metadata in validation warning/block responses
  - Added tests for drift window behavior and auto-revert enforcement
- **TBOT-A16** - Governance recommendation audit/versioning ledger baseline
  - Added governance_versions ledger table in audit DB
  - Added version record/list helpers and CLI
  - Added tests for version history ordering
- **TBOT-A15** - Governance recommendation application guardrails baseline
  - Guardrail evaluator for approved recommendation packages
  - Rollback template generator for prior-policy restoration
  - CLI helper and tests for apply/rollback artifacts
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
