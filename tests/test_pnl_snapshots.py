import sqlite3

from src.portfolio.snapshots import save_snapshot


def test_save_snapshot_writes_row(tmp_path):
    db = str(tmp_path / "portfolio.db")
    save_snapshot({"equity_pnl_total": 1.23}, db_path=db)

    conn = sqlite3.connect(db)
    row = conn.execute("SELECT COUNT(*) FROM pnl_snapshots").fetchone()
    assert row[0] == 1
