# Implementation Status vs Plan

Updated: 2026-02-13

## Completed
- ✅ Repo scaffold + configs (`apps/`, `src/`, `config/`, tests)
- ✅ Broker abstraction and Questrade adapter baseline
- ✅ Risk engine hard limits + position sizing
- ✅ Telegram approval workflow (inline approve/reject + polling)
- ✅ Callback acknowledgement (`answerCallbackQuery`)
- ✅ Audit store for events + approval decisions (SQLite)
- ✅ Execution router with paper/live split
- ✅ Live guardrails requiring explicit env confirmation
- ✅ Live dry-run default route (`LIVE_ORDER_DRY_RUN=true`)
- ✅ News normalization + dedup + whitelist relevance filtering
- ✅ Rule-based signal generator
- ✅ Paper execution path
- ✅ KPI report utility from audit DB (`apps/backtester/report.py`)
- ✅ End-to-end run path tests and integration checks
- ✅ Agentic contracts + supervisor skeleton (`src/agents/*`)
- ✅ Telegram webhook baseline with idempotent callback persistence (`apps/telegram_webhook/server.py`, `src/webhook/*`)
- ✅ Webhook server/worker queue hardening baseline (health endpoint, payload size guard, retry/fail states)
- ✅ Webhook production rollout assets (prod Nginx TLS template, systemd units, TLS bootstrap + healthcheck scripts, deployment checklist)
- ✅ Webhook VPS cutover validation baseline (go/no-go checklist + host validation script)
- ✅ Webhook host evidence/incident baseline (evidence snapshot script + incident report generator)
- ✅ Broker hardening baseline (error taxonomy + retry/backoff + idempotency key propagation)
- ✅ Broker validation edge-matrix baseline v2 (symbol/side hygiene + quantity caps + Questrade extended-hours constraints)
- ✅ Broker validation rollout/telemetry baseline v3 (`BROKER_VALIDATION_MODE` + rejection source telemetry)
- ✅ Broker validation drift-control baseline v4 (report-only expiry + hard-fail auto-revert)
- ✅ Advanced PnL baseline (realized/unrealized + avg cost + snapshot persistence)
- ✅ Multi-currency PnL normalization baseline (base-currency conversion with FX map)
- ✅ Weekly postmortem automation baseline (`apps/backtester/weekly_postmortem.py`)
- ✅ Governance baselines: structured learning recommendations + drift detection severity + rollback guidance + tier escalation controls
- ✅ Agent communication design baseline (envelope contract + bridge route policy scaffold)
- ✅ Agent communication implementation baseline (CLI transport, command allow-list, timeout controls, manual bridge runner)
- ✅ Agent communication observability baseline (audit table + retry/dead-letter policy + coverage tests)
- ✅ Agent communication delivery guarantees baseline (retry backoff + dead-letter query/replay tooling)
- ✅ Governance policy simulation sandbox baseline (what-if approvals/risk with CLI scenario runner)
- ✅ Governance threshold calibration baseline (replay-pack candidate ranking + calibration CLI)
- ✅ Weekly governance calibration artifact baseline (weekly report generator with KPI snapshot + candidate ranking)
- ✅ Scheduled governance calibration delivery baseline (manifest generation + cron helper + routing envs)
- ✅ Governance recommendation approval workflow baseline (accept/reject/change-set with explicit decision artifacts)
- ✅ Governance recommendation apply guardrails baseline (safety checks + rollback template generation)
- ✅ Governance recommendation audit/versioning ledger baseline (versioned governance decisions in audit DB)
- ✅ Governance threshold tuning baseline from paper KPI metrics (recommended min confidence + allowed tiers)

## Partially Implemented
- 🟡 Questrade live order path: symbolId + retry/idempotency + baseline order/session validation matrix implemented; SLA tuning and broker-specific edge-case matrix remain.
- 🟡 Portfolio/monitoring metrics: ledger + realized/unrealized + FX normalization implemented; live FX source integration remains.

## Not Yet Implemented
- ⬜ Production webhook host execution (apply templates on target VPS, DNS cutover, Telegram webhook registration validation).
- ⬜ Full micro-live weekly postmortem template automation (basic runbook now exists in docs/runbooks.md).
- ⬜ Advanced controlled-automation policy orchestration (basic env-driven auto-approve rules now implemented).

## Recommendation to reach “v1 operational”
1. Complete broker validation matrix + error/SLA policy tuning by order type/session.
2. Add realized/unrealized PnL tracker on top of current ledger.
3. Add public deployment hardening for webhook (TLS, reverse proxy, queue workers).
4. Run 2-4 weeks paper with KPI snapshots before enabling non-dry-run live mode.
