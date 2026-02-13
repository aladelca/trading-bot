#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${WEBHOOK_PUBLIC_DOMAIN:-}" ]]; then
  echo "WEBHOOK_PUBLIC_DOMAIN is required"
  exit 1
fi

if [[ -z "${CERTBOT_EMAIL:-}" ]]; then
  echo "CERTBOT_EMAIL is required"
  exit 1
fi

sudo mkdir -p /var/www/certbot
sudo certbot certonly --webroot \
  -w /var/www/certbot \
  -d "$WEBHOOK_PUBLIC_DOMAIN" \
  --agree-tos \
  --email "$CERTBOT_EMAIL" \
  --non-interactive

echo "TLS bootstrap complete for $WEBHOOK_PUBLIC_DOMAIN"
