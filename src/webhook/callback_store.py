from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class CallbackStore:
    def __init__(self, db_path: str = "data/webhook.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS callback_events (
                event_key TEXT PRIMARY KEY,
                update_id INTEGER,
                callback_query_id TEXT,
                request_id TEXT,
                decision TEXT,
                payload_json TEXT NOT NULL,
                processed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def upsert_event(self, event_key: str, payload: dict, update_id: int | None, callback_query_id: str | None) -> bool:
        cur = self.conn.execute("SELECT 1 FROM callback_events WHERE event_key=?", (event_key,)).fetchone()
        if cur:
            return False
        self.conn.execute(
            "INSERT INTO callback_events(event_key, update_id, callback_query_id, payload_json, processed) VALUES (?, ?, ?, ?, 0)",
            (event_key, update_id, callback_query_id, json.dumps(payload, sort_keys=True)),
        )
        self.conn.commit()
        return True

    def mark_processed(self, event_key: str, request_id: str, decision: str) -> None:
        self.conn.execute(
            "UPDATE callback_events SET processed=1, request_id=?, decision=? WHERE event_key=?",
            (request_id, decision, event_key),
        )
        self.conn.commit()
