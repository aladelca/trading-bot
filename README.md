# trading-bot

Human-in-the-loop scaffold for a news-driven **stocks/ETF** trading bot (Questrade-first), with Telegram approval before execution.

## Current status
- ✅ v1 scaffold (paper mode default)
- ✅ Risk gates + sizing
- ✅ Symbol whitelist enforcement
- ✅ Signal + approval + fill audit logging (SQLite)
- ✅ Signal placeholder from free news feed interface
- ✅ Telegram approval client wiring (inline approve/reject + polling)
- ✅ Questrade token/account integration primitives (live execution still disabled)
- ❌ No live trading enabled yet

## Why extended hours can help
- Capture post-earnings and macro reactions earlier.
- Potentially improve entry timing around overnight news.

## Extended-hours risks (important)
- Wider spreads and thinner liquidity.
- More slippage and false breakouts.
- Harder fills for larger position sizes.

## Free data/news options (start here)
- RSS/news feeds (issuer press releases, market news RSS)
- Yahoo Finance public headlines (scraped carefully, terms-aware)
- SEC company filings feed (for U.S.-listed assets)
- Stooq/Alpha Vantage free tiers for supplemental market data

## Grok API
Yes, you can use Grok API if you have access and key provisioning. Add an adapter under `src/signals/` for sentiment/event scoring while keeping risk rules deterministic.

## Setup (Python 3.11)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
pytest -q
python apps/orchestrator/main.py
```

## Credentials to add later
Update `.env`:
- `QUESTRADE_CLIENT_ID`
- `QUESTRADE_REFRESH_TOKEN`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## Questrade API coverage in bot
Current adapter now supports:
- Accounts: list accounts
- Balances: per-currency balances / buying power
- Positions: open positions by account
- Executions + activities: historical account events
- Quotes: real-time quote pulls from symbol IDs
- Candles: time-series candles by interval
- Orders: validated submit path with retry/idempotency

Fetch a strategy-ready broker snapshot (balances + positions + quotes):
```bash
python apps/backtester/questrade_snapshot.py --symbols SPY,QQQ,XEQT
```

## Safety
- Keep `PAPER_MODE=true` until you validate performance and reliability.
- Keep approval gate mandatory in early live phases.
- Live execution is blocked unless BOTH are explicitly set:
  - `LIVE_TRADING_ENABLED=true`
  - `LIVE_TRADING_CONFIRM=I_UNDERSTAND_LIVE_TRADING_RISK`
- Even with live enabled, keep `LIVE_ORDER_DRY_RUN=true` until final launch.

## KPI report
After running orchestrator cycles, generate KPI summary from audit DB:
```bash
python apps/backtester/report.py
```

## Advanced PnL report
Generate realized/unrealized PnL and save a snapshot:
```bash
python apps/backtester/pnl_report.py
```
Optional envs for normalization:
- `BASE_CURRENCY` (default `USD`)
- `FX_RATES_JSON` (example: `{"USD":1.0,"CAD":0.75}`)
- `TRADE_CURRENCY` for new ledger writes

## Weekly postmortem report
Generate weekly KPI + drift + learning recommendations:
```bash
python apps/backtester/weekly_postmortem.py
```

## Agentic supervisor cycle
Run the new supervised multi-agent pipeline skeleton:
```bash
python apps/orchestrator/agentic_main.py
```
Optional inter-agent CLI bridge controls:
- `AGENT_CLI_ENABLED=false`
- `AGENT_CLI_ALLOWED_COMMANDS=python`
- `AGENT_CLI_TIMEOUT_SECONDS=5`
- `AGENT_CLI_MAX_RETRIES=1`
- `AGENT_CLI_RETRY_BACKOFF_SECONDS=0.2`
- `AGENT_ALLOWED_ROUTES=signal:risk,risk:execution`

Comms observability:
- bridge events are stored in `comms_events` table in `AUDIT_DB_PATH`
- failed CLI deliveries are retried up to `AGENT_CLI_MAX_RETRIES` with backoff then tagged dead-letter
- replay dead letters manually:
  - `python apps/orchestrator/agent_cli_dlq_replay.py --limit 10`

Governance policy simulation sandbox:
```bash
python apps/backtester/policy_simulation.py \
  --confidence 0.93 \
  --symbol SPY \
  --allowed-symbols SPY,QQQ \
  --allowed-tiers tier-1,tier-2 \
  --current-kpi-json '{"approval_rate":0.42,"signals_rejected":14,"equity_pnl_total":3}' \
  --baseline-kpi-json '{"approval_rate":0.55,"signals_rejected":8,"equity_pnl_total":7}'
```

Governance threshold calibration from replay pack:
```bash
python apps/backtester/threshold_calibration.py \
  --replay-pack data/replay_packs/governance-sample.json \
  --candidates 0.85,0.88,0.90,0.92,0.95
```

Weekly governance calibration report artifact:
```bash
python apps/backtester/weekly_governance_calibration.py
```

Scheduled governance delivery manifest:
```bash
python apps/backtester/scheduled_governance_delivery.py
```
Install cron helper:
```bash
bash scripts/deploy/install_governance_calibration_cron.sh
```

Governance threshold tuning from paper KPIs:
```bash
python apps/backtester/threshold_tuning.py \
  --kpi-json '{"approval_rate":0.58,"equity_pnl_total":3.4,"signals_rejected":11}'
```

Governance recommendation approval workflow (human decision):
```bash
python apps/backtester/governance_approval_workflow.py \
  --recommendation-json '{"recommended_auto_approve_min_confidence":0.9,"recommended_allowed_tiers":["tier-1","tier-2"]}' \
  --decision change-set \
  --overrides-json '{"recommended_auto_approve_min_confidence":0.92}' \
  --decided-by adrian \
  --reason "keep risk tight"
```

Governance apply guardrails + rollback template:
```bash
python apps/backtester/governance_apply_guardrails.py \
  --approved-package-json '{"id":"r1","status":"approved","final_recommendation":{"recommended_auto_approve_min_confidence":0.9,"recommended_allowed_tiers":["tier-1","tier-2"]}}' \
  --previous-policy-json '{"AUTO_APPROVE_MIN_CONFIDENCE":0.92,"AUTO_APPROVE_ALLOWED_TIERS":"tier-1,tier-2"}'
```

Governance recommendation versioning ledger:
```bash
python apps/backtester/governance_versioning.py \
  --recommendation-id rec-1 \
  --version-tag v1 \
  --status approved \
  --decided-by adrian \
  --payload-json '{"recommended_auto_approve_min_confidence":0.9}'
```

Governance deployment sign-off matrix:
```bash
python apps/backtester/governance_signoff.py \
  --signoff-json '{"risk_owner_approved":true,"ops_owner_approved":true,"rollback_plan_attached":true,"kpi_snapshot_attached":true,"dry_run_validation_passed":true}'
```
See: `docs/governance-deployment-checklist.md`

Governance drift acknowledgement + expiry evaluation:
```bash
python apps/backtester/governance_drift_ack.py \
  --policy-id auto-approve-policy \
  --severity high \
  --acknowledged-by adrian \
  --valid-minutes 120
```

Governance emergency override protocol:
```bash
python apps/backtester/governance_emergency_override.py \
  --policy-id auto-approve-policy \
  --approved-by adrian \
  --reason "incident-mitigation" \
  --override-minutes 30 \
  --changes-json '{"AUTO_APPROVE_ENABLED": false}'
```

Manual CLI bridge invocation example:
```bash
python apps/orchestrator/agent_cli_bridge.py \
  --request-id demo-1 \
  --source-agent signal \
  --target-agent risk \
  --command "python -c \"print('hello-risk')\""
```

## Telegram webhook mode
Run production-style webhook receiver (with secret-token validation):
```bash
python apps/telegram_webhook/server.py
```
Run worker for async callback processing queue:
```bash
python apps/telegram_webhook/worker.py
```
Set env vars: `TELEGRAM_WEBHOOK_SECRET`, `WEBHOOK_HOST`, `WEBHOOK_PORT`, `WEBHOOK_PATH`, `WEBHOOK_DB_PATH`, `WEBHOOK_MAX_BODY_BYTES`, `WEBHOOK_WORKER_POLL_SECONDS`, `WEBHOOK_WORKER_BATCH_SIZE`.

Health check:
- `GET /health` returns webhook service status.

For deployment scaffold, see:
- `infra/docker/docker-compose.webhook.yml`
- `infra/nginx/telegram_webhook.conf`
- `infra/nginx/telegram_webhook.prod.conf`
- `infra/systemd/tradingbot-webhook-server.service`
- `infra/systemd/tradingbot-webhook-worker.service`
- `docs/deployment-webhook-hardening.md`
- `docs/webhook-cutover-checklist.md`
- `scripts/deploy/validate_webhook_cutover.sh`
- `scripts/deploy/capture_webhook_evidence.sh`
- `apps/telegram_webhook/incident_report.py`
- `apps/telegram_webhook/evidence_alert_pipeline.py`

Generate evidence + alert routing manifests:
```bash
python apps/telegram_webhook/evidence_alert_pipeline.py
```
Deliver pending alert manifests with retry policy:
```bash
python apps/telegram_webhook/alert_delivery_runner.py \
  --delivery-dir apps/telegram_webhook/reports/delivery \
  --max-attempts 3 \
  --backoff-seconds 0.2
```

## Plan tracking
- Implementation status vs plan: `docs/IMPLEMENTATION_STATUS.md`
- Jira-style status board: `docs/JIRA_STATUS.md`
- Backlog tickets: `docs/BACKLOG.md`

## Portfolio ledger
Executed/paper/dry-run trade intents are recorded in `data/portfolio.db` for lightweight metrics.

## Controlled automation (optional)
You can enable strict auto-approval for high-confidence symbols only:
- `AUTO_APPROVE_ENABLED=true`
- `AUTO_APPROVE_MIN_CONFIDENCE=0.90`
- `AUTO_APPROVE_SYMBOLS=SPY,QQQ`
- `AUTO_APPROVE_ALLOWED_TIERS=tier-1,tier-2`

Default is disabled (`false`).

## Broker order validation matrix (baseline)
Before live submit, the bot validates:
- symbol format and allowed symbol chars
- side is `buy|sell`
- quantity > 0 and global quantity cap
- allowed order types (`market|limit|stop`)
- session rule: `stop` orders blocked in extended hours
- broker-specific edge rules (Questrade extended-hours restrictions)

Rollout toggle:
- `BROKER_VALIDATION_MODE=enforce` (default)
- `BROKER_VALIDATION_MODE=report_only` (attach warning telemetry but do not block)
- `BROKER_VALIDATION_AUTO_REVERT=true` (force fail-safe revert to enforce)
- `BROKER_VALIDATION_REPORT_ONLY_SINCE_UTC=<ISO-8601 UTC>`
- `BROKER_VALIDATION_REPORT_ONLY_MAX_MINUTES=<int>`

Validation rollout metrics dashboard:
```bash
python apps/backtester/broker_validation_dashboard.py \
  --records-json '[{"status":"blocked","rejection_source":"pre_trade_validation"},{"status":"error","rejection_source":"broker_api"}]'
```
