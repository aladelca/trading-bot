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
                reason TEXT,
                payload_json TEXT NOT NULL,
                processed INTEGER NOT NULL DEFAULT 0,
                processing_state TEXT NOT NULL DEFAULT 'pending',
                attempts INTEGER NOT NULL DEFAULT 0,
                last_error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._ensure_column("reason", "TEXT")
        self._ensure_column("processing_state", "TEXT NOT NULL DEFAULT 'pending'")
        self._ensure_column("attempts", "INTEGER NOT NULL DEFAULT 0")
        self._ensure_column("last_error", "TEXT")
        self.conn.commit()

    def _ensure_column(self, name: str, ddl: str) -> None:
        cols = self.conn.execute("PRAGMA table_info(callback_events)").fetchall()
        existing = {c[1] for c in cols}
        if name not in existing:
            self.conn.execute(f"ALTER TABLE callback_events ADD COLUMN {name} {ddl}")

    def upsert_event(self, event_key: str, payload: dict, update_id: int | None, callback_query_id: str | None) -> bool:
        cur = self.conn.execute("SELECT 1 FROM callback_events WHERE event_key=?", (event_key,)).fetchone()
        if cur:
            return False
        self.conn.execute(
            """
            INSERT INTO callback_events(
                event_key, update_id, callback_query_id, payload_json, processed, processing_state, attempts
            ) VALUES (?, ?, ?, ?, 0, 'pending', 0)
            """,
            (event_key, update_id, callback_query_id, json.dumps(payload, sort_keys=True)),
        )
        self.conn.commit()
        return True

    def claim_pending(self, limit: int = 50) -> list[tuple[str, dict]]:
        rows = self.conn.execute(
            "SELECT event_key, payload_json FROM callback_events WHERE processing_state='pending' ORDER BY created_at ASC LIMIT ?",
            (limit,),
        ).fetchall()
        out: list[tuple[str, dict]] = []
        for event_key, payload_json in rows:
            self.conn.execute(
                "UPDATE callback_events SET processing_state='in_progress', attempts=attempts+1 WHERE event_key=?",
                (event_key,),
            )
            out.append((event_key, json.loads(payload_json)))
        self.conn.commit()
        return out

    def mark_processed(self, event_key: str, request_id: str, decision: str) -> None:
        self.conn.execute(
            """
            UPDATE callback_events
            SET processed=1, processing_state='processed', request_id=?, decision=?, reason=NULL, last_error=NULL
            WHERE event_key=?
            """,
            (request_id, decision, event_key),
        )
        self.conn.commit()

    def mark_ignored(self, event_key: str, reason: str) -> None:
        self.conn.execute(
            """
            UPDATE callback_events
            SET processed=1, processing_state='ignored', reason=?, last_error=NULL
            WHERE event_key=?
            """,
            (reason, event_key),
        )
        self.conn.commit()

    def mark_failed(self, event_key: str, error_text: str, max_attempts: int = 5) -> None:
        row = self.conn.execute("SELECT attempts FROM callback_events WHERE event_key=?", (event_key,)).fetchone()
        attempts = int(row[0]) if row else max_attempts
        next_state = "failed" if attempts >= max_attempts else "pending"
        self.conn.execute(
            "UPDATE callback_events SET processing_state=?, last_error=? WHERE event_key=?",
            (next_state, error_text[:500], event_key),
        )
        self.conn.commit()
