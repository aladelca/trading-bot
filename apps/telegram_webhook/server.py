from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.webhook.callback_store import CallbackStore
from src.webhook.telegram_processor import enqueue_telegram_update

WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8080"))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram/webhook")
WEBHOOK_DB_PATH = os.getenv("WEBHOOK_DB_PATH", "data/webhook.db")


class Handler(BaseHTTPRequestHandler):
    store = CallbackStore(WEBHOOK_DB_PATH)

    def _json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):  # noqa: N802
        if self.path != WEBHOOK_PATH:
            self._json(404, {"error": "not_found"})
            return

        header_secret = self.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not WEBHOOK_SECRET or header_secret != WEBHOOK_SECRET:
            self._json(401, {"error": "unauthorized"})
            return

        try:
            content_len = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_len)
            update = json.loads(body.decode() or "{}")
            result = enqueue_telegram_update(update, self.store)
            self._json(200, result)
        except Exception as exc:  # defensive boundary
            self._json(500, {"error": str(exc)})


def run() -> None:
    server = HTTPServer((WEBHOOK_HOST, WEBHOOK_PORT), Handler)
    print(f"Telegram webhook listening on http://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    run()
