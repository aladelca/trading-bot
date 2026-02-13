from pathlib import Path

from apps.telegram_webhook.incident_report import generate_webhook_incident_report
from src.webhook.callback_store import CallbackStore


def test_generate_webhook_incident_report_with_failed_rows(tmp_path):
    db = str(tmp_path / "webhook.db")
    store = CallbackStore(db)
    store.upsert_event("k1", {"x": 1}, update_id=1, callback_query_id="cb1")
    item = store.claim_pending(limit=1)[0]
    store.mark_failed(item[0], "boom", max_attempts=1)

    out = generate_webhook_incident_report(db_path=db, out_dir=str(tmp_path))
    text = Path(out).read_text()
    assert "Webhook Incident Report" in text
    assert "Failed callbacks: 1" in text
