from __future__ import annotations

import json
import time
from pathlib import Path


def deliver_alert_manifest(
    manifest_path: str,
    *,
    out_dir: str,
    max_attempts: int = 3,
    backoff_seconds: float = 0.2,
) -> dict:
    path = Path(manifest_path)
    payload = json.loads(path.read_text())

    out_base = Path(out_dir)
    out_base.mkdir(parents=True, exist_ok=True)
    sent_dir = out_base / "sent"
    dead_dir = out_base / "dead_letter"
    sent_dir.mkdir(parents=True, exist_ok=True)
    dead_dir.mkdir(parents=True, exist_ok=True)

    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        # connector baseline: route-ready dry-run always succeeds unless forced failure flag.
        force_fail = bool(payload.get("force_fail"))
        if not force_fail:
            out = {
                "status": "sent",
                "attempts": attempts,
                "manifest_path": str(path),
                "channel": payload.get("channel"),
                "target": payload.get("target"),
            }
            (sent_dir / path.name).write_text(json.dumps(out, sort_keys=True, indent=2))
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
    }
    (dead_dir / path.name).write_text(json.dumps(out, sort_keys=True, indent=2))
    return out


def process_pending_alert_manifests(delivery_dir: str, *, max_attempts: int = 3, backoff_seconds: float = 0.2) -> list[dict]:
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
            )
        )
    return out
