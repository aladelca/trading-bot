# Webhook Deployment Hardening Guide

## Objective
Harden Telegram webhook operations for production deployment with TLS, reverse proxy, supervised processes, and repeatable health checks.

## Components
1. HTTP webhook server (`apps/telegram_webhook/server.py`)
2. Worker processor (`apps/telegram_webhook/worker.py`)
3. Callback store (`data/webhook.db`)
4. Reverse proxy template (`infra/nginx/telegram_webhook.prod.conf`)
5. systemd units (`infra/systemd/tradingbot-webhook-*.service`)

## Security controls
- Secret-token verification (`X-Telegram-Bot-Api-Secret-Token`)
- Payload size limit (`WEBHOOK_MAX_BODY_BYTES`)
- Health endpoint (`GET /health`)
- Queue-style processing to keep webhook ACK fast
- TLS + HSTS at reverse proxy

## Host rollout checklist (WEBHOOK-HARDEN-2)
1. **Prepare host paths**
   - Repo at `/opt/trading-bot`
   - Python venv at `/opt/trading-bot/.venv`
   - Env file at `/opt/trading-bot/.env`
2. **Configure domain/env**
   - Set `WEBHOOK_PUBLIC_DOMAIN`
   - Set `CERTBOT_EMAIL`
   - Set `TELEGRAM_WEBHOOK_SECRET`
3. **Provision TLS cert**
   - `source /opt/trading-bot/.env`
   - `bash scripts/deploy/bootstrap_tls.sh`
4. **Install Nginx config**
   - Copy `infra/nginx/telegram_webhook.prod.conf` to `/etc/nginx/sites-available/tradingbot-webhook.conf`
   - Replace `__DOMAIN__` with your domain
   - Enable site + `nginx -t` + reload
5. **Install systemd services**
   - Copy both unit files from `infra/systemd/` to `/etc/systemd/system/`
   - `sudo systemctl daemon-reload`
   - `sudo systemctl enable --now tradingbot-webhook-server tradingbot-webhook-worker`
6. **Telegram webhook registration**
   - Register webhook URL: `https://<domain>/telegram/webhook`
   - Include secret token matching `TELEGRAM_WEBHOOK_SECRET`
7. **Post-deploy validation**
   - `bash scripts/deploy/healthcheck_webhook.sh`
   - `bash scripts/deploy/validate_webhook_cutover.sh`
   - `bash scripts/deploy/capture_webhook_evidence.sh`
   - `python apps/telegram_webhook/incident_report.py`
   - Check worker logs: queue drains, no retry spikes
   - Apply go/no-go criteria from `docs/webhook-cutover-checklist.md`

## Operational checks
- Webhook health: `GET /health`
- Queue is draining (`processing_state='pending'` decreases)
- worker/server systemd services stay `active (running)`

## Failure behavior
- Duplicate callback events are ignored (idempotent key)
- Processing errors are retried up to max attempts then marked `failed`
- Keep live order guardrails active while webhook changes are deployed

## Rollback
- Disable webhook services:
  - `sudo systemctl stop tradingbot-webhook-worker tradingbot-webhook-server`
- Restore previous Nginx config and reload
- Repoint Telegram webhook to prior endpoint (or clear webhook)
