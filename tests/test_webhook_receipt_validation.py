import hashlib
import hmac
import json

from apps.telegram_webhook.alert_delivery import (
    validate_receipt_directory,
)


def test_validate_receipt_directory_ok_and_tamper(tmp_path):
    receipts = tmp_path / "receipts"
    receipts.mkdir(parents=True)

    good = {
        "kind": "webhook_alert_delivery_receipt",
        "manifest": "webhook-incident-alert-1.json",
        "status": "delivered",
        "provider": "telegram",
        "provider_message_id": "telegram-123",
        "attempts": 1,
        "signature_alg": "hmac-sha256",
    }

    raw = json.dumps(
        {
            "kind": good["kind"],
            "manifest": good["manifest"],
            "status": good["status"],
            "provider": good["provider"],
            "provider_message_id": good["provider_message_id"],
            "attempts": good["attempts"],
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    good["signature"] = hmac.new(b"secret", raw, hashlib.sha256).hexdigest()

    bad = dict(good)
    bad["manifest"] = "webhook-incident-alert-2.json"
    bad["signature"] = "deadbeef"

    (receipts / "webhook-incident-alert-1.json").write_text(json.dumps(good))
    (receipts / "webhook-incident-alert-2.json").write_text(json.dumps(bad))

    out = validate_receipt_directory(str(receipts), signing_key="secret")
    assert len(out) == 2
    ok = [x for x in out if x["receipt"] == "webhook-incident-alert-1.json"][0]
    bad_out = [x for x in out if x["receipt"] == "webhook-incident-alert-2.json"][0]
    assert ok["ok"] is True
    assert bad_out["ok"] is False
    assert bad_out["reason"] == "receipt_signature_mismatch"


def test_validate_receipt_missing_provider_ack(tmp_path):
    receipts = tmp_path / "receipts"
    receipts.mkdir(parents=True)
    payload = {
        "kind": "webhook_alert_delivery_receipt",
        "manifest": "webhook-incident-alert-3.json",
        "status": "delivered",
        "provider": "",
        "provider_message_id": "",
        "attempts": 1,
        "signature_alg": "none",
        "signature": "",
    }
    (receipts / "webhook-incident-alert-3.json").write_text(json.dumps(payload))

    out = validate_receipt_directory(str(receipts))
    assert out[0]["ok"] is False
    assert out[0]["reason"] == "missing_provider_ack"
