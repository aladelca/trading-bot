from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class AuditLogger:
    def __init__(self, db_path: str = "data/audit.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                request_id TEXT PRIMARY KEY,
                approved INTEGER NOT NULL,
                source TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def log(self, kind: str, payload: dict) -> None:
        self.conn.execute(
            "INSERT INTO events(kind, payload_json) VALUES (?, ?)",
            (kind, json.dumps(payload, sort_keys=True)),
        )
        self.conn.commit()

    def save_decision(self, request_id: str, approved: bool, source: str) -> None:
        self.conn.execute(
            """
            INSERT INTO decisions(request_id, approved, source)
            VALUES (?, ?, ?)
            ON CONFLICT(request_id) DO UPDATE SET approved=excluded.approved, source=excluded.source
            """,
            (request_id, int(approved), source),
        )
        self.conn.commit()

    def get_decision(self, request_id: str) -> bool | None:
        row = self.conn.execute(
            "SELECT approved FROM decisions WHERE request_id=?",
            (request_id,),
        ).fetchone()
        if row is None:
            return None
        return bool(row[0])

    def count(self, kind: str | None = None) -> int:
        if kind:
            row = self.conn.execute("SELECT COUNT(*) FROM events WHERE kind=?", (kind,)).fetchone()
        else:
            row = self.conn.execute("SELECT COUNT(*) FROM events").fetchone()
        return int(row[0]) if row else 0
