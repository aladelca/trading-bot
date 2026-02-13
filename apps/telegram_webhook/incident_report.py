from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def generate_webhook_incident_report(
    db_path: str = "data/webhook.db",
    out_dir: str = "apps/telegram_webhook/reports",
) -> str:
    conn = sqlite3.connect(db_path)
    failed_rows = []
    try:
        failed_rows = conn.execute(
            """
            SELECT rowid, update_id, processing_state, attempts, last_error, created_at
            FROM callback_events
            WHERE processing_state='failed'
            ORDER BY rowid DESC
            LIMIT 100
            """
        ).fetchall()
    except sqlite3.OperationalError:
        failed_rows = []

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = Path(out_dir) / f"webhook-incident-{ts}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Webhook Incident Report",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"Failed callbacks: {len(failed_rows)}",
        "",
        "## Failed Callback Samples",
    ]

    if failed_rows:
        for row in failed_rows:
            lines.append(
                f"- id={row[0]} update_id={row[1]} attempts={row[3]} error={row[4]} created_at={row[5]}"
            )
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Recommended Actions",
            "- Validate Telegram webhook secret and endpoint reachability.",
            "- Confirm worker service is active and queue is draining.",
            "- Reprocess or inspect failed callbacks after root-cause fix.",
            "",
        ]
    )

    out_path.write_text("\n".join(lines))
    return str(out_path)


if __name__ == "__main__":
    print(generate_webhook_incident_report())
