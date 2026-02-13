from __future__ import annotations

import argparse
import json

from apps.telegram_webhook.alert_delivery import process_pending_alert_manifests


def main() -> None:
    p = argparse.ArgumentParser(description="Webhook alert manifest delivery connector")
    p.add_argument("--delivery-dir", default="apps/telegram_webhook/reports/delivery")
    p.add_argument("--max-attempts", type=int, default=3)
    p.add_argument("--backoff-seconds", type=float, default=0.2)
    args = p.parse_args()

    out = process_pending_alert_manifests(
        args.delivery_dir,
        max_attempts=args.max_attempts,
        backoff_seconds=args.backoff_seconds,
    )
    print(json.dumps(out))


if __name__ == "__main__":
    main()
