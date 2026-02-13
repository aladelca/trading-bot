# Human-in-the-Loop News-Driven Trading Agent — Implementation Plan

## 1) Goal
Build a trading agent that:
1. Ingests market-moving news,
2. Generates trade proposals,
3. Requires Telegram approval before execution,
4. Enforces strict risk limits,
5. Logs all decisions for auditability and iteration.

### Success criteria (first 8 weeks)
- No hard risk-limit breaches (daily/weekly drawdown rules always enforced).
- Stable execution pipeline (no duplicate or orphan orders).
- Positive expectancy in paper trading and micro-live testing.

---

## 2) Broker Choice for Canada (Questrade vs Alternatives)

### Can we use Questrade API?
Yes, likely yes for v1, especially for a Canada-first setup.

### Caveats to validate early
- Supported order types needed by strategy (market/limit/stop/bracket behavior).
- API rate limits and reliability.
- Auth/token refresh behavior under long-running sessions.
- Market data latency/coverage for selected assets.

### Recommendation
Implement a **broker abstraction layer** from day one:
- Start with `QuestradeAdapter`.
- Keep the door open for `IBKRAdapter` if scaling needs outgrow Questrade.

---

## 3) Architecture (v1)

## Core components
1. **News Ingestion Service**
   - Pulls from trusted sources.
   - Normalizes timestamps to UTC.
   - Deduplicates and tags by symbol relevance.

2. **Signal Engine**
   - Scores sentiment + event impact.
   - Applies transparent rule-based logic.
   - Emits trade candidate with expiry.

3. **Risk Engine (hard gate)**
   - Position sizing by risk budget.
   - Enforces max daily/weekly drawdown.
   - Enforces max concurrent positions and max trades/day.

4. **Approval Bot (Telegram)**
   - Sends trade card with Approve/Reject/Modify.
   - Includes time-to-expiry.
   - Rejects stale proposals.

5. **Execution Engine**
   - Routes validated orders to broker API.
   - Handles fills/partials/cancel.
   - Uses idempotency keys to prevent duplicates.

6. **Portfolio & Monitoring**
   - Tracks equity, exposure, realized/unrealized PnL.
   - Emits alerts for risk events.

7. **Audit Store**
   - Logs full chain: signal → approval → order → outcome.
   - Supports weekly review and debugging.

---

## 4) Suggested Repository Structure

```text
trading-bot/
  apps/
    orchestrator/
    telegram-bot/
    backtester/
  src/
    data/
      news_ingestors/
      market_data/
    signals/
      sentiment/
      event_impact/
      strategy_rules/
    risk/
      position_sizing.py
      hard_limits.py
    broker/
      base.py
      questrade/
      ibkr/              # optional, future-ready
    execution/
      order_router.py
      fill_handler.py
    portfolio/
    analytics/
  config/
    settings.yaml
    risk_policy.yaml
    assets_whitelist.yaml
  infra/
    docker/
    migrations/
  tests/
  docs/
    architecture.md
    runbooks.md
```

---

## 5) Risk Policy (Mandatory Defaults)

- Risk per trade: **0.5%–1.0%** of account equity.
- Daily max drawdown: **2%** (kill switch).
- Weekly max drawdown: **5%** (pause + manual review).
- Max concurrent positions: **2–4**.
- Max trades/day: configurable hard cap (e.g., 3–6).
- Whitelist-only symbols (start with 2–4 liquid assets).
- No averaging down/martingale unless explicitly designed and tested.
- API keys with minimum permissions only (no withdrawals where applicable).

---

## 6) Trading Logic v1 (Simple and Auditable)

### Strategy template
- Event-driven trigger from high-impact fresh news.
- Momentum confirmation from market data.
- Volatility-aware stop placement.
- Position sizing from stop distance and risk budget.
- Predefined take-profit and/or time-based exit.
- Signal expiry if stale.

### Why this approach
- Transparent and debuggable.
- Lower overfitting risk than complex ML-first setups.
- Easier to enforce strict risk controls.

---

## 7) Approval Flow (Human-in-the-Loop)

1. Signal engine creates candidate trade.
2. Risk engine validates candidate.
3. Telegram bot sends proposal:
   - Symbol, side, size, entry, stop, target,
   - Rationale summary,
   - Confidence score,
   - Expiry timer.
4. User action:
   - **Approve** → execute,
   - **Reject** → discard,
   - **Modify** → resubmit through risk checks.
5. If no response by expiry → auto-cancel.

---

## 8) Data, Logging, and Metrics

## Store per trade
- Source event/news IDs,
- Signal features and score,
- Risk checks + reasons,
- Approval metadata,
- Broker request/response IDs,
- Fill details,
- Final PnL and exit reason.

## Weekly KPI review
- Win rate,
- Profit factor,
- Max drawdown,
- Expectancy,
- Average hold time,
- Slippage vs assumption.

---

## 9) Phased Rollout

### Phase A — Design & Setup (3–5 days)
- Finalize broker adapter requirements.
- Define risk policy + asset whitelist.
- Implement skeleton architecture and configs.

### Phase B — Paper Trading (2–4 weeks)
- Run full pipeline with simulated execution.
- Tune only risk and execution reliability first.
- Avoid frequent strategy parameter changes.

### Phase C — Micro Live (2–4 weeks)
- Deploy with small capital and strict approval gating.
- Keep kill-switch thresholds conservative.
- Conduct weekly postmortems.

### Phase D — Controlled Automation
- Auto-approve only a narrow subset of high-confidence setups.
- Maintain manual override and hard risk controls.

---

## 10) Security & Operational Controls

- Secrets in env/vault; never commit tokens.
- Least-privilege API credentials.
- 2FA on GitHub and broker accounts.
- Strict idempotency and retry policies.
- Health checks and alerting for service outages.
- Immutable audit logs.

---

## 11) Implementation Backlog (First 2 Sprints)

## Sprint 1
- [ ] Repo scaffolding + config files.
- [ ] Broker interface (`BrokerClient`) + stub Questrade adapter.
- [ ] Risk engine with hard-limit checks.
- [ ] Telegram proposal workflow (Approve/Reject/Expiry).
- [ ] Event and trade log schema.

## Sprint 2
- [ ] News ingestion + dedup + relevance tagging.
- [ ] Rule-based signal generator.
- [ ] Paper execution simulator.
- [ ] KPI dashboard script/report.
- [ ] End-to-end integration tests.

## Sprint 3 (Agentic Governance + Comms)
- [ ] TBOT-A5 threshold tuning with 2-4 week paper metrics.
- [ ] TBOT-A6 agent communication bridge design (CLI/session protocol).
- [ ] TBOT-A7 agent communication bridge implementation + auth/allow-list.
- [ ] TBOT-A8 comms observability (delivery audit, retries, dead-letter handling).

---

## 12) Definition of Done (v1)

- End-to-end trade proposal and approval flow works reliably.
- All executed trades pass risk engine checks.
- No duplicate order submissions under retry scenarios.
- Full audit trail available for every signal and trade.
- Paper-trading metrics produced weekly and reviewed.

---

## 13) Agentic Architecture (Proposed)

Introduce a supervised multi-agent topology:

1. **Market-Intel Agent**
   - Ingests and normalizes news + market context.
2. **Signal Agent**
   - Converts events into structured trade hypotheses.
3. **Risk Agent**
   - Enforces hard limits, whitelists, and sizing policy.
4. **Approval Agent**
   - Runs human-in-the-loop decision workflow (Telegram/webhook).
5. **Execution Agent**
   - Routes paper/live orders with guardrails and retries.
6. **Portfolio Agent**
   - Updates ledger, positions, and PnL metrics.
7. **Supervisor Agent**
   - Orchestrates sequence, circuit-breakers, and incident posture.
8. **Review/Learning Agent**
   - Produces periodic improvement recommendations (non-autonomous apply).
9. **Agent Communication Bridge (CLI/Session Bus)**
   - Provides explicit inter-agent communication channel (CLI/session-based messaging).
   - Supports request/response envelopes, correlation IDs, and delivery status.
   - Enforces allow-lists, auth context, and full audit logging of agent-to-agent instructions.

### Agent handoff contract (minimum)
Each stage produces a typed envelope:
- `request_id`
- `source_agent`
- `target_agent`
- `transport` (`internal|cli|session-bridge`)
- `stage`
- `status` (`ok|blocked|error`)
- `payload`
- `reason` (if blocked/error)
- `timestamp_utc`
- `correlation_id`

---

## 14) Final Recommendation

This is **technically feasible** and a good fit for phased delivery.
Use Questrade first if it matches your account and instrument needs, but preserve broker portability with a clean adapter design.
Focus on **capital protection + process reliability** before optimization.
