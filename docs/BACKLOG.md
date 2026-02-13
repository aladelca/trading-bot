# Product Backlog (Prioritized)

## P1 (High)
1. **TBOT-A5** - Governance threshold tuning from live paper metrics
2. **WEBHOOK-HARDEN-2** - Production webhook rollout finalization (real cert provisioning + domain + supervised host process)
3. **BROKER-VALID-2** - Broker-specific edge-case matrix expansion

## P2 (Medium)
4. Multi-currency PnL live FX feed + cross-rate validation
5. Weekly postmortem scheduler + distribution channel integration
6. Policy simulation sandbox for approval/risk changes

## Completed Recently
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
