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

## Plan tracking
- Implementation status vs plan: `docs/IMPLEMENTATION_STATUS.md`

## Portfolio ledger
Executed/paper/dry-run trade intents are recorded in `data/portfolio.db` for lightweight metrics.

## Controlled automation (optional)
You can enable strict auto-approval for high-confidence symbols only:
- `AUTO_APPROVE_ENABLED=true`
- `AUTO_APPROVE_MIN_CONFIDENCE=0.90`
- `AUTO_APPROVE_SYMBOLS=SPY,QQQ`

Default is disabled (`false`).
