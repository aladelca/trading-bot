from __future__ import annotations

from src.telegram.client import parse_callback_decision
from src.webhook.callback_store import CallbackStore


def _event_key(update: dict) -> str:
    update_id = update.get("update_id")
    cb = update.get("callback_query", {})
    cb_id = cb.get("id", "")
    return f"u:{update_id}|cb:{cb_id}"


def process_telegram_update(update: dict, store: CallbackStore) -> dict:
    key = _event_key(update)
    update_id = update.get("update_id")
    cb = update.get("callback_query", {})
    cb_id = cb.get("id")

    inserted = store.upsert_event(key, update, update_id, cb_id)
    if not inserted:
        return {"status": "duplicate", "event_key": key}

    data = cb.get("data", "")
    if ":" not in data:
        return {"status": "ignored", "event_key": key}

    action, request_id = data.split(":", 1)
    decision = parse_callback_decision(f"{action}:{request_id}", request_id)
    if decision is None:
        return {"status": "ignored", "event_key": key}

    store.mark_processed(key, request_id=request_id, decision="approve" if decision else "reject")
    return {
        "status": "processed",
        "event_key": key,
        "request_id": request_id,
        "decision": bool(decision),
    }
