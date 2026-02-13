from __future__ import annotations

from datetime import datetime, timezone

from src.broker.base import OrderRequest


def build_trade_ticket(order: OrderRequest, *, strategy_id: str = "", rationale: str = "") -> dict:
    return {
        "kind": "manual_trade_ticket",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "strategy_id": strategy_id,
        "rationale": rationale,
        "symbol": order.symbol.upper(),
        "side": order.side.lower(),
        "quantity": int(order.quantity),
        "order_type": order.order_type.lower(),
        "extended_hours": bool(order.extended_hours),
        "execution_mode": "manual_in_questrade",
    }
