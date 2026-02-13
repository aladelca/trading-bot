# Product Backlog (Prioritized)

## P0 (Critical)
1. **TBOT-12** - Production Telegram webhook
   - Acceptance:
     - Secret-validated webhook endpoint
     - Callback idempotency by update_id/callback_query.id
     - <3s ACK and async processing
2. **TBOT-13** - Broker hardening matrix
   - Acceptance:
     - Retryable vs non-retryable taxonomy
     - Backoff + max attempts
     - Idempotency key propagation
3. **TBOT-14** - Advanced PnL engine
   - Acceptance:
     - Realized and unrealized PnL by symbol
     - Position avg cost + mark-to-market snapshots

## P1 (High)
4. **TBOT-11** - Agentic supervisor pipeline completion
   - Acceptance:
     - Stage contracts enforced
     - Circuit-breaker integration
     - End-to-end trace IDs across agents
5. **TBOT-15** - Weekly postmortem automation
   - Acceptance:
     - Scheduled KPI summary and anomaly list

## P2 (Medium)
6. **TBOT-A2** - Review/Learning agent recommendations
7. **TBOT-A3** - Controlled automation escalation rules
8. **TBOT-A4** - Drift detection and rollback policy

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
