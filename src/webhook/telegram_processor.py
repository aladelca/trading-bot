from __future__ import annotations

from src.telegram.client import parse_callback_decision
from src.webhook.callback_store import CallbackStore


def _safe_callback_query(update: dict) -> dict:
    cb = update.get("callback_query", {})
    return cb if isinstance(cb, dict) else {}


def _event_key(update: dict) -> str:
    update_id = update.get("update_id")
    cb = _safe_callback_query(update)
    cb_id = cb.get("id", "")
    return f"u:{update_id}|cb:{cb_id}"


def enqueue_telegram_update(update: dict, store: CallbackStore) -> dict:
    key = _event_key(update)
    update_id = update.get("update_id")
    cb = _safe_callback_query(update)
    cb_id = cb.get("id")

    inserted = store.upsert_event(key, update, update_id, cb_id)
    if not inserted:
        return {"status": "duplicate", "event_key": key}
    return {"status": "queued", "event_key": key}


def process_pending_once(store: CallbackStore, limit: int = 50) -> list[dict]:
    out: list[dict] = []
    for event_key, update in store.claim_pending(limit=limit):
        try:
            cb = _safe_callback_query(update)
            data = cb.get("data", "")

            if ":" not in data:
                store.mark_ignored(event_key, "invalid_callback_data")
                out.append({"status": "ignored", "event_key": event_key})
                continue

            action, request_id = data.split(":", 1)
            decision = parse_callback_decision(f"{action}:{request_id}", request_id)
            if decision is None:
                store.mark_ignored(event_key, "unrecognized_decision")
                out.append({"status": "ignored", "event_key": event_key})
                continue

            store.mark_processed(event_key, request_id=request_id, decision="approve" if decision else "reject")
            out.append(
                {
                    "status": "processed",
                    "event_key": event_key,
                    "request_id": request_id,
                    "decision": bool(decision),
                }
            )
        except Exception as exc:
            store.mark_failed(event_key, str(exc))
            out.append({"status": "error", "event_key": event_key, "error": str(exc)})
    return out
