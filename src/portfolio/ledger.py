from __future__ import annotations

import sqlite3
from pathlib import Path


class PortfolioLedger:
    def __init__(self, db_path: str = "data/portfolio.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                status TEXT NOT NULL,
                mode TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def record_trade(self, symbol: str, side: str, quantity: int, price: float, status: str, mode: str) -> None:
        self.conn.execute(
            "INSERT INTO trades(symbol, side, quantity, price, status, mode) VALUES (?, ?, ?, ?, ?, ?)",
            (symbol, side, quantity, price, status, mode),
        )
        self.conn.commit()

    def metrics(self) -> dict:
        row = self.conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(quantity * price), 0) FROM trades"
        ).fetchone()
        total_trades = int(row[0]) if row else 0
        notional = float(row[1]) if row else 0.0
        buys = self.conn.execute("SELECT COUNT(*) FROM trades WHERE side='buy'").fetchone()
        sells = self.conn.execute("SELECT COUNT(*) FROM trades WHERE side='sell'").fetchone()
        return {
            "trades_total": total_trades,
            "trades_buy": int(buys[0]) if buys else 0,
            "trades_sell": int(sells[0]) if sells else 0,
            "notional_total": round(notional, 4),
        }
