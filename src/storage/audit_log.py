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
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comms_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT NOT NULL,
                source_agent TEXT NOT NULL,
                target_agent TEXT NOT NULL,
                transport TEXT NOT NULL,
                status TEXT NOT NULL,
                reason TEXT NOT NULL DEFAULT '',
                correlation_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS governance_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_id TEXT NOT NULL,
                version_tag TEXT NOT NULL,
                status TEXT NOT NULL,
                decided_by TEXT NOT NULL,
                payload_json TEXT NOT NULL,
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

    def log_comms(
        self,
        *,
        request_id: str,
        source_agent: str,
        target_agent: str,
        transport: str,
        status: str,
        reason: str,
        correlation_id: str,
        payload: dict,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO comms_events(
                request_id, source_agent, target_agent, transport, status, reason, correlation_id, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                source_agent,
                target_agent,
                transport,
                status,
                reason,
                correlation_id,
                json.dumps(payload, sort_keys=True),
            ),
        )
        self.conn.commit()

    def list_dead_letters(self, limit: int = 20) -> list[dict]:
        rows = self.conn.execute(
            """
            SELECT id, request_id, source_agent, target_agent, transport, reason, correlation_id, payload_json
            FROM comms_events
            WHERE status='error' AND payload_json LIKE '%"dead_letter": true%'
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
        out: list[dict] = []
        for row in rows:
            out.append(
                {
                    "id": int(row[0]),
                    "request_id": str(row[1]),
                    "source_agent": str(row[2]),
                    "target_agent": str(row[3]),
                    "transport": str(row[4]),
                    "reason": str(row[5]),
                    "correlation_id": str(row[6]),
                    "payload": json.loads(row[7]),
                }
            )
        return out

    def log_governance_version(
        self,
        *,
        recommendation_id: str,
        version_tag: str,
        status: str,
        decided_by: str,
        payload: dict,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO governance_versions(
                recommendation_id, version_tag, status, decided_by, payload_json
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                recommendation_id,
                version_tag,
                status,
                decided_by,
                json.dumps(payload, sort_keys=True),
            ),
        )
        self.conn.commit()

    def list_governance_versions(self, recommendation_id: str) -> list[dict]:
        rows = self.conn.execute(
            """
            SELECT id, recommendation_id, version_tag, status, decided_by, payload_json, created_at
            FROM governance_versions
            WHERE recommendation_id=?
            ORDER BY id ASC
            """,
            (recommendation_id,),
        ).fetchall()
        out: list[dict] = []
        for row in rows:
            out.append(
                {
                    "id": int(row[0]),
                    "recommendation_id": str(row[1]),
                    "version_tag": str(row[2]),
                    "status": str(row[3]),
                    "decided_by": str(row[4]),
                    "payload": json.loads(row[5]),
                    "created_at": str(row[6]),
                }
            )
        return out

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

    def count_comms(self, status: str | None = None) -> int:
        if status:
            row = self.conn.execute("SELECT COUNT(*) FROM comms_events WHERE status=?", (status,)).fetchone()
        else:
            row = self.conn.execute("SELECT COUNT(*) FROM comms_events").fetchone()
        return int(row[0]) if row else 0
