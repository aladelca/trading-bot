#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${WEBHOOK_EVIDENCE_DIR:-/tmp/webhook-evidence}"
TS="$(date -u +%Y%m%d-%H%M%S)"
SNAP_DIR="$OUT_DIR/$TS"
mkdir -p "$SNAP_DIR"

DOMAIN="${WEBHOOK_PUBLIC_DOMAIN:-}"
HEALTH_PATH="${WEBHOOK_HEALTH_PATH:-/health}"
DB_PATH="${WEBHOOK_DB_PATH:-data/webhook.db}"

echo "capturing evidence in $SNAP_DIR"

sudo systemctl status tradingbot-webhook-server --no-pager > "$SNAP_DIR/systemd-server.txt" || true
sudo systemctl status tradingbot-webhook-worker --no-pager > "$SNAP_DIR/systemd-worker.txt" || true
sudo nginx -t > "$SNAP_DIR/nginx-test.txt" 2>&1 || true

curl -fsS "http://127.0.0.1:8080${HEALTH_PATH}" > "$SNAP_DIR/health-local.json" || true
if [[ -n "$DOMAIN" ]]; then
  curl -fsS "https://${DOMAIN}${HEALTH_PATH}" > "$SNAP_DIR/health-public.json" || true
fi

python - << 'PY' > "$SNAP_DIR/webhook-queue.txt"
import os, sqlite3
p = os.getenv('WEBHOOK_DB_PATH', 'data/webhook.db')
conn = sqlite3.connect(p)
for state in ('pending','processing','failed','processed'):
    try:
        row = conn.execute("SELECT COUNT(*) FROM callbacks WHERE processing_state=?", (state,)).fetchone()
        n = int(row[0]) if row else 0
    except sqlite3.OperationalError:
        n = 0
    print(f"{state}={n}")
PY

echo "evidence_capture_dir=$SNAP_DIR"
