# Trading Bot Runbooks

## 1) Daily preflight (paper or micro-live)
1. Verify `.env` values are set as intended.
2. Confirm `PAPER_MODE=true` unless explicitly running micro-live.
3. Confirm guardrails:
   - `LIVE_TRADING_ENABLED=true` only when intended.
   - `LIVE_TRADING_CONFIRM=I_UNDERSTAND_LIVE_TRADING_RISK`.
   - `LIVE_ORDER_DRY_RUN=true` for safe validation.
4. Run checks:
   - `ruff check .`
   - `PYTHONPATH=. pytest -q`

## 2) Start cycle
- Run orchestrator:
  - `python apps/orchestrator/main.py`
- Review audit entries in `data/audit.db`.
- Review portfolio ledger in `data/portfolio.db`.

## 3) KPI review (daily/weekly)
- Generate KPI report:
  - `python apps/backtester/report.py`
- Track trends:
  - approval rate
  - signal rejection reasons
  - trade notional

## 4) Incident handling
### A) Unexpected live-routing attempt
- Set `LIVE_TRADING_ENABLED=false`
- Keep `LIVE_ORDER_DRY_RUN=true`
- Re-run and verify blocked status.

### B) Broker auth failures
- Validate refresh token and account access.
- Rotate token if needed.
- Keep in paper mode until resolved.

### C) Approval anomalies
- Verify Telegram bot token/chat id.
- Confirm callback updates and offset progression.
- In webhook mode, verify worker is consuming pending callback queue.

## Webhook deployment baseline
- Start services scaffold:
  - `docker compose -f infra/docker/docker-compose.webhook.yml up -d`
- Ensure certificate files are present in `infra/nginx/certs/`.
- Validate webhook path and secret header handling.

## 5) Rollback drill
- Revert latest merge commit if runtime regression appears.
- Re-run full test suite.
- Resume from last known good commit.
