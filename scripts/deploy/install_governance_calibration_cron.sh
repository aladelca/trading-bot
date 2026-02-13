#!/usr/bin/env bash
set -euo pipefail

CRON_EXPR="${GOV_CALIBRATION_CRON_EXPR:-0 13 * * 1}"
WORKDIR="${TRADING_BOT_DIR:-/opt/trading-bot}"
PYTHON_BIN="${PYTHON_BIN:-$WORKDIR/.venv/bin/python}"

CMD="cd $WORKDIR && $PYTHON_BIN apps/backtester/scheduled_governance_delivery.py >> $WORKDIR/data/governance_delivery.log 2>&1"

( crontab -l 2>/dev/null | grep -v "scheduled_governance_delivery.py" ; echo "$CRON_EXPR $CMD" ) | crontab -

echo "Installed governance calibration cron: $CRON_EXPR"
