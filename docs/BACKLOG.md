# Product Backlog (Prioritized)

## P1 (High)
1. **TBOT-A2** - Review/Learning agent recommendations hardening
2. **TBOT-A3** - Controlled automation escalation policy hardening
3. **TBOT-A4** - Drift detection tuning + rollback policy automation

## P2 (Medium)
4. Webhook deployment finalization (real cert provisioning + domain + supervised process on host)
5. Broker validation matrix tuning by order type/session
6. Multi-currency PnL normalization

## Completed Recently
- **TBOT-15** - Weekly postmortem automation baseline
- **WEBHOOK-HARDEN-1** - Deployment hardening baseline
  - Nginx reverse-proxy template
  - Docker compose scaffold (server + worker + nginx)
  - Async webhook worker polling queue
- **TBOT-14** - Advanced PnL engine baseline
- **TBOT-13** - Broker hardening matrix baseline
- **TBOT-12** - Production-style Telegram webhook baseline

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
