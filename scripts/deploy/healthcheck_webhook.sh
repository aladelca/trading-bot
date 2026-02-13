#!/usr/bin/env bash
set -euo pipefail

HOST="${WEBHOOK_HEALTH_HOST:-https://127.0.0.1}"
PATH_HEALTH="${WEBHOOK_HEALTH_PATH:-/health}"

curl -fsS "$HOST$PATH_HEALTH" >/dev/null

echo "webhook healthcheck ok: $HOST$PATH_HEALTH"
