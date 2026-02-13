from __future__ import annotations

from hashlib import sha256

from src.broker.base import OrderRequest


def build_order_idempotency_key(order: OrderRequest, request_id: str) -> str:
    raw = f"{request_id}|{order.symbol}|{order.side}|{order.quantity}|{order.order_type}|{order.extended_hours}"
    return sha256(raw.encode()).hexdigest()
