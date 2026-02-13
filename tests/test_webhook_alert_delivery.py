import json

from apps.telegram_webhook.alert_delivery import process_pending_alert_manifests


def test_alert_delivery_sent_and_receipt(tmp_path):
    delivery = tmp_path / "delivery"
    delivery.mkdir(parents=True)
    manifest = delivery / "webhook-incident-alert-1.json"
    manifest.write_text(json.dumps({"channel": "telegram", "target": "123"}))

    out = process_pending_alert_manifests(
        str(delivery),
        max_attempts=2,
        backoff_seconds=0,
        provider="telegram",
        signing_key="secret-key",
    )
    assert len(out) == 1
    assert out[0]["status"] == "sent"
    assert out[0]["provider"] == "telegram"
    assert (delivery / "sent" / manifest.name).exists()

    receipt_path = delivery / "receipts" / manifest.name
    assert receipt_path.exists()
    receipt = json.loads(receipt_path.read_text())
    assert receipt["status"] == "delivered"
    assert receipt["signature_alg"] == "hmac-sha256"
    assert receipt["signature"]


def test_alert_delivery_dead_letter_on_forced_failure(tmp_path):
    delivery = tmp_path / "delivery"
    delivery.mkdir(parents=True)
    manifest = delivery / "webhook-incident-alert-2.json"
    manifest.write_text(json.dumps({"channel": "telegram", "target": "123", "force_fail": True}))

    out = process_pending_alert_manifests(str(delivery), max_attempts=2, backoff_seconds=0)
    assert len(out) == 1
    assert out[0]["status"] == "dead_letter"
    assert (delivery / "dead_letter" / manifest.name).exists()
