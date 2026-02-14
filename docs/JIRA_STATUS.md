# Trading Bot - Jira Style Status

_Last updated: 2026-02-13_

## Epic TBOT-EPIC-1: Core v1 Trading Pipeline
- Status: **IN PROGRESS**
- Progress: 100%

### Done
- TBOT-1 Scaffold + config baseline ✅
- TBOT-2 Risk engine + sizing ✅
- TBOT-3 Telegram approval flow (polling) ✅
- TBOT-4 Audit store + decision persistence ✅
- TBOT-5 Live guardrails + dry-run routing ✅
- TBOT-6 News normalization + dedup + relevance filter ✅
- TBOT-7 KPI reporting baseline ✅
- TBOT-8 SymbolId resolution baseline ✅
- TBOT-9 Portfolio ledger baseline ✅
- TBOT-10 Ops runbook baseline ✅
- TBOT-11 Agentic supervisor architecture and contracts ✅
- TBOT-12 Telegram production webhook + idempotent callback store ✅
- TBOT-13 Broker retry matrix and error taxonomy hardening ✅
- TBOT-14 Advanced realized/unrealized PnL engine ✅

### Done
- TBOT-15 Weekly postmortem automation ✅

### Done
- WEBHOOK-HARDEN-1 Deployment hardening baseline (TLS/reverse-proxy/worker scaffold) ✅
- WEBHOOK-HARDEN-2 Production rollout assets (TLS bootstrap script, systemd units, prod Nginx template, rollout guide) ✅
- WEBHOOK-HARDEN-3 VPS cutover validation baseline (go/no-go checklist + validation script) ✅
- WEBHOOK-HARDEN-4 Host evidence capture + post-cutover incident automation baseline ✅
- WEBHOOK-HARDEN-5 Automated evidence upload + incident alert routing baseline ✅
- WEBHOOK-HARDEN-6 Alert delivery connector + retry policy baseline ✅
- WEBHOOK-HARDEN-7 Provider delivery integration + signed receipt baseline ✅
- WEBHOOK-HARDEN-8 Provider ack verification + receipt tamper validation baseline ✅
- PNL-FX-1 Multi-currency PnL normalization baseline ✅
- BROKER-VALID-2 Broker-specific edge-case validation matrix expansion ✅
- BROKER-VALID-3 Validation rollout toggles + broker rejection telemetry baseline ✅
- BROKER-VALID-4 Validation mode drift monitoring + hard-fail auto-revert policy ✅
- BROKER-VALID-5 Validation rollout metrics dashboard + alert thresholds ✅
- BROKER-VALID-6 Broker validation anomaly triage playbook + remediation matrix ✅
- BROKER-VALID-7 Validation anomaly auto-remediation runbook execution hooks ✅
- BROKER-API-1 Questrade API capability expansion (balances/positions/quotes/candles snapshot support) ✅
- BROKER-ACCESS-1 Questrade retail read-only safety mode + manual trade tickets ✅

## Epic TBOT-EPIC-2: Agentic Autonomy with Governance
- Status: **IN PROGRESS**
- Progress: 100%

### Done
- TBOT-A1 Multi-agent contracts and supervisor skeleton ✅
- TBOT-A2 Learning/review agent reports ✅
- TBOT-A3 Controlled auto-approve policy escalation matrix ✅
- TBOT-A4 Drift detection and rollback recommendations ✅

### To Do
- TBOT-A23 Governance override quorum policy templates + role-based signer matrix
- TBOT-A24 Governance stale-ticket SLA tracking + escalation routing

### Done
- TBOT-A6 Agent communication bridge design (CLI/session protocol + envelope contract) ✅
- TBOT-A7 Agent communication bridge implementation (auth allow-list + routing + CLI transport) ✅
- TBOT-A8 Agent communication observability (delivery audit + retry/dead-letter policy) ✅
- TBOT-A9 Agent communication delivery guarantees hardening (backoff tuning + DLQ replay tooling) ✅
- TBOT-A10 Governance policy simulation sandbox (what-if approvals/risk) ✅
- TBOT-A11 Governance threshold calibration with scenario replay packs ✅
- TBOT-A12 Weekly governance calibration automation + report artifacting ✅
- TBOT-A13 Scheduled governance calibration delivery (cron + channel delivery) ✅
- TBOT-A14 Governance recommendation approval workflow (human accept/reject/change-set) ✅
- TBOT-A15 Governance recommendation application guardrails + rollback template ✅
- TBOT-A16 Governance recommendation audit and versioning ledger ✅
- TBOT-A17 Governance change deployment checklist + sign-off matrix ✅
- TBOT-A18 Governance policy drift acknowledgements + expiry controls ✅
- TBOT-A19 Governance emergency override protocol + expiry enforcement ✅
- TBOT-A20 Governance policy reconciliation review cadence + stale decision cleanup ✅
- TBOT-A21 Governance emergency override multi-signature approvals + incident linkage ✅
- TBOT-A22 Governance reconciliation drift auto-ticketing + owner assignment ✅
- TBOT-A5 Governance threshold tuning using 2-4 week paper metrics ✅
