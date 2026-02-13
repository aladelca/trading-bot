# Webhook Deployment Hardening Guide

## Objective
Harden Telegram webhook operations for production-style deployment.

## Components
1. HTTP webhook server (`apps/telegram_webhook/server.py`)
2. Worker processor (`apps/telegram_webhook/worker.py`)
3. Callback store (`data/webhook.db`)

## Security controls
- Secret-token verification (`X-Telegram-Bot-Api-Secret-Token`)
- Payload size limit (`WEBHOOK_MAX_BODY_BYTES`)
- Health endpoint (`GET /health`)
- Queue-style processing to keep webhook ACK fast

## Recommended deployment topology
- Reverse proxy (Nginx/Caddy) with TLS termination
- Internal app bind (localhost/private network)
- Process manager (systemd/supervisor) for:
  - webhook server
  - webhook worker

## Operational checks
- Webhook health: `GET /health`
- Queue is draining (worker logs show processed events)
- No build-up of `processing_state='pending'` rows

## Failure behavior
- Duplicate callback events are ignored (idempotent key)
- Processing errors are retried up to max attempts then marked `failed`
- Keep live order guardrails active while webhook changes are deployed
