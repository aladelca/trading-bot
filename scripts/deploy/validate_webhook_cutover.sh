#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${WEBHOOK_PUBLIC_DOMAIN:-}"
HEALTH_PATH="${WEBHOOK_HEALTH_PATH:-/health}"

if [[ -z "$DOMAIN" ]]; then
  echo "WEBHOOK_PUBLIC_DOMAIN is required"
  exit 1
fi

echo "[1/5] systemd status"
sudo systemctl is-active tradingbot-webhook-server >/dev/null
sudo systemctl is-active tradingbot-webhook-worker >/dev/null

echo "[2/5] local health endpoint"
curl -fsS "http://127.0.0.1:8080${HEALTH_PATH}" >/dev/null

echo "[3/5] public TLS health endpoint"
curl -fsS "https://${DOMAIN}${HEALTH_PATH}" >/dev/null

echo "[4/5] webhook db queue depth"
python - << 'PY'
import os, sqlite3
p = os.getenv('WEBHOOK_DB_PATH', 'data/webhook.db')
conn = sqlite3.connect(p)
try:
    row = conn.execute("SELECT COUNT(*) FROM callbacks WHERE processing_state='pending'").fetchone()
    pending = int(row[0]) if row else 0
except sqlite3.OperationalError:
    pending = 0
print(f"pending_callbacks={pending}")
PY

echo "[5/5] nginx config check"
sudo nginx -t >/dev/null

echo "WEBHOOK cutover validation OK"
