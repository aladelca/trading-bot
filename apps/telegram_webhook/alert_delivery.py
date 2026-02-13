from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from pathlib import Path


def _sign_receipt(payload: dict, signing_key: str) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(signing_key.encode(), raw, hashlib.sha256).hexdigest()


def _provider_send(payload: dict, provider: str) -> dict:
    # Baseline provider connector: deterministic local simulation.
    # Fails only when force_fail=true in the manifest.
    if bool(payload.get("force_fail")):
        return {"ok": False, "reason": "forced_failure"}
    return {
        "ok": True,
        "provider": provider,
        "provider_message_id": payload.get("provider_message_id") or f"{provider}-simulated-message",
    }


def deliver_alert_manifest(
    manifest_path: str,
    *,
    out_dir: str,
    max_attempts: int = 3,
    backoff_seconds: float = 0.2,
    provider: str = "local",
    signing_key: str = "",
) -> dict:
    path = Path(manifest_path)
    payload = json.loads(path.read_text())

    out_base = Path(out_dir)
    out_base.mkdir(parents=True, exist_ok=True)
    sent_dir = out_base / "sent"
    dead_dir = out_base / "dead_letter"
    receipts_dir = out_base / "receipts"
    sent_dir.mkdir(parents=True, exist_ok=True)
    dead_dir.mkdir(parents=True, exist_ok=True)
    receipts_dir.mkdir(parents=True, exist_ok=True)

    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        provider_result = _provider_send(payload, provider)
        if provider_result.get("ok"):
            out = {
                "status": "sent",
                "attempts": attempts,
                "manifest_path": str(path),
                "channel": payload.get("channel"),
                "target": payload.get("target"),
                "provider": provider_result.get("provider", provider),
                "provider_message_id": provider_result.get("provider_message_id", ""),
            }
            (sent_dir / path.name).write_text(json.dumps(out, sort_keys=True, indent=2))

            receipt = {
                "kind": "webhook_alert_delivery_receipt",
                "manifest": path.name,
                "status": "delivered",
                "provider": out["provider"],
                "provider_message_id": out["provider_message_id"],
                "attempts": attempts,
            }
            key = signing_key or os.getenv("WEBHOOK_ALERT_RECEIPT_SIGNING_KEY", "")
            if key:
                receipt["signature"] = _sign_receipt(receipt, key)
                receipt["signature_alg"] = "hmac-sha256"
            else:
                receipt["signature"] = ""
                receipt["signature_alg"] = "none"

            (receipts_dir / path.name).write_text(json.dumps(receipt, sort_keys=True, indent=2))
            return out

        if attempts < max_attempts:
            time.sleep(backoff_seconds * attempts)

    out = {
        "status": "dead_letter",
        "attempts": attempts,
        "manifest_path": str(path),
        "channel": payload.get("channel"),
        "target": payload.get("target"),
        "reason": "max_attempts_exhausted",
        "provider": provider,
    }
    (dead_dir / path.name).write_text(json.dumps(out, sort_keys=True, indent=2))
    return out


def process_pending_alert_manifests(
    delivery_dir: str,
    *,
    max_attempts: int = 3,
    backoff_seconds: float = 0.2,
    provider: str = "local",
    signing_key: str = "",
) -> list[dict]:
    base = Path(delivery_dir)
    if not base.exists():
        return []

    out: list[dict] = []
    for p in sorted(base.glob("webhook-incident-alert-*.json")):
        out.append(
            deliver_alert_manifest(
                str(p),
                out_dir=str(base),
                max_attempts=max_attempts,
                backoff_seconds=backoff_seconds,
                provider=provider,
                signing_key=signing_key,
            )
        )
    return out
