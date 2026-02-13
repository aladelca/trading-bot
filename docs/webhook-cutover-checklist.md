# WEBHOOK-HARDEN-3 Cutover Checklist

## Preconditions
- Domain points to VPS A/AAAA records.
- `.env` on host configured (`WEBHOOK_PUBLIC_DOMAIN`, `TELEGRAM_WEBHOOK_SECRET`, `WEBHOOK_DB_PATH`).
- TLS certificate provisioned and Nginx config enabled.

## Go/No-Go checks
1. `sudo systemctl is-active tradingbot-webhook-server`
2. `sudo systemctl is-active tradingbot-webhook-worker`
3. `curl -fsS http://127.0.0.1:8080/health`
4. `curl -fsS https://<domain>/health`
5. `sudo nginx -t`
6. Pending callback queue is near-zero during idle periods.

## Telegram cutover
- Set webhook to `https://<domain>/telegram/webhook`
- Include `X-Telegram-Bot-Api-Secret-Token` value matching `TELEGRAM_WEBHOOK_SECRET`.
- Send a controlled test callback/update and verify it reaches worker processing.

## Acceptance criteria
- All checks pass twice (5 minutes apart).
- No callback retry spike after cutover.
- No `failed` callback accumulation.
- Health endpoints stable for >=15 minutes.

## Rollback
- Stop worker/server systemd services.
- Restore previous Nginx site and reload.
- Repoint or clear Telegram webhook.
- Keep live trading guardrails fail-closed during rollback window.
