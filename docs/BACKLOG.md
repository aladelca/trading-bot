# Product Backlog (Prioritized)

## P0 (Critical)
1. **TBOT-14** - Advanced PnL engine
   - Acceptance:
     - Realized and unrealized PnL by symbol
     - Position avg cost + mark-to-market snapshots

## P1 (High)
3. **TBOT-11** - Agentic supervisor pipeline completion
   - Acceptance:
     - Stage contracts enforced
     - Circuit-breaker integration
     - End-to-end trace IDs across agents
4. **TBOT-15** - Weekly postmortem automation
   - Acceptance:
     - Scheduled KPI summary and anomaly list

## P2 (Medium)
5. **TBOT-A2** - Review/Learning agent recommendations
6. **TBOT-A3** - Controlled automation escalation rules
7. **TBOT-A4** - Drift detection and rollback policy

## Completed Recently
- **TBOT-13** - Broker hardening matrix baseline
  - Retryable/fatal/blocked taxonomy
  - Bounded retry with backoff
  - Idempotency key propagation for live submit
- **TBOT-12** - Production-style Telegram webhook baseline
  - Secret-token validation
  - Callback idempotency by update_id/callback_query.id
  - Webhook callback persistence in SQLite

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
