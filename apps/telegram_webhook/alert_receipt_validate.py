from __future__ import annotations

import argparse
import json

from apps.telegram_webhook.alert_delivery import validate_receipt_directory


def main() -> None:
    p = argparse.ArgumentParser(description="Validate webhook delivery receipt signatures and provider ack metadata")
    p.add_argument("--receipts-dir", default="apps/telegram_webhook/reports/delivery/receipts")
    p.add_argument("--signing-key", default="")
    args = p.parse_args()

    out = validate_receipt_directory(args.receipts_dir, signing_key=args.signing_key)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
