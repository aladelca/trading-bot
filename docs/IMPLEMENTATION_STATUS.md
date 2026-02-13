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

## Partially Implemented
- 🟡 Questrade live order path: request wiring exists, but symbolId resolution is still placeholder.
- 🟡 Portfolio/monitoring metrics: core event counters available, advanced realized/unrealized PnL not finalized.

## Not Yet Implemented
- ⬜ Production webhook service for Telegram callbacks (currently polling-based).
- ⬜ Full micro-live operations playbook (runbooks/weekly postmortem templates).
- ⬜ Automated controlled-automation policy (Phase D auto-approve subset rules).

## Recommendation to reach “v1 operational”
1. Implement symbolId lookup + validated order mapping per asset.
2. Add portfolio ledger and realized/unrealized PnL tracker.
3. Add operator runbook (`docs/runbooks.md`) with incident handling and rollback drills.
4. Run 2-4 weeks paper with KPI snapshots before enabling non-dry-run live mode.
