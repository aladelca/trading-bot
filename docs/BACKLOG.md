# Product Backlog (Prioritized)

## P1 (High)
1. **TBOT-A6** - Agent communication bridge design (CLI/session protocol + security model)
2. **TBOT-A7** - Agent communication bridge implementation (routing, auth allow-list, correlation IDs)
3. **TBOT-A5** - Governance threshold tuning from live paper metrics
4. **BROKER-VALID-2** - Broker-specific edge-case matrix expansion
5. **WEBHOOK-HARDEN-3** - VPS execution and DNS/webhook cutover validation

## P2 (Medium)
6. **TBOT-A8** - Agent communication observability (delivery audit + retry/dead-letter policy)
7. Multi-currency PnL live FX feed + cross-rate validation
8. Weekly postmortem scheduler + distribution channel integration
9. Policy simulation sandbox for approval/risk changes

## Completed Recently
- **WEBHOOK-HARDEN-2** - Production rollout assets
  - Nginx production TLS template
  - systemd service units for server + worker
  - TLS bootstrap and webhook healthcheck scripts
  - host rollout checklist in deployment guide
- **TBOT-A2/A3/A4** - Governance hardening baseline
  - Structured learning recommendations
  - Tier-aware auto-approve escalation controls
  - Drift severity + rollback profile recommendations
- **PNL-FX-1** - Multi-currency PnL normalization baseline
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
