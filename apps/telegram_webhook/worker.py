from __future__ import annotations

import os
import time

from src.webhook.callback_store import CallbackStore
from src.webhook.telegram_processor import process_pending_once

WEBHOOK_DB_PATH = os.getenv("WEBHOOK_DB_PATH", "data/webhook.db")
WORKER_POLL_SECONDS = float(os.getenv("WEBHOOK_WORKER_POLL_SECONDS", "1.0"))
WORKER_BATCH_SIZE = int(os.getenv("WEBHOOK_WORKER_BATCH_SIZE", "50"))


def run() -> None:
    store = CallbackStore(WEBHOOK_DB_PATH)
    print(f"Webhook worker started (db={WEBHOOK_DB_PATH})")
    while True:
        processed = process_pending_once(store, limit=WORKER_BATCH_SIZE)
        if processed:
            print(f"Processed {len(processed)} callback event(s)")
        time.sleep(WORKER_POLL_SECONDS)


if __name__ == "__main__":
    run()
