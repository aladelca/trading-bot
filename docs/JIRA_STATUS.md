# Trading Bot - Jira Style Status

_Last updated: 2026-02-13_

## Epic TBOT-EPIC-1: Core v1 Trading Pipeline
- Status: **IN PROGRESS**
- Progress: 98%

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
- PNL-FX-1 Multi-currency PnL normalization baseline ✅

## Epic TBOT-EPIC-2: Agentic Autonomy with Governance
- Status: **IN PROGRESS**
- Progress: 85%

### Done
- TBOT-A1 Multi-agent contracts and supervisor skeleton ✅
- TBOT-A2 Learning/review agent reports ✅
- TBOT-A3 Controlled auto-approve policy escalation matrix ✅
- TBOT-A4 Drift detection and rollback recommendations ✅

### To Do
- TBOT-A5 Governance threshold tuning using 2-4 week paper metrics
- TBOT-A6 Agent communication bridge design (CLI/session protocol + envelope contract)
- TBOT-A7 Agent communication bridge implementation (auth allow-list + routing)
- TBOT-A8 Agent communication observability (delivery audit + retry/dead-letter policy)
