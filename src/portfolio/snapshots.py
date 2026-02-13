from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def init_snapshot_schema(db_path: str = "data/portfolio.db") -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pnl_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def save_snapshot(snapshot: dict, db_path: str = "data/portfolio.db") -> None:
    init_snapshot_schema(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO pnl_snapshots(snapshot_json) VALUES (?)", (json.dumps(snapshot, sort_keys=True),))
    conn.commit()
