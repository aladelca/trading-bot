from __future__ import annotations

from dataclasses import dataclass

from src.broker.base import OrderRequest


@dataclass
class ValidationResult:
    ok: bool
    reason: str = ""


def validate_order_matrix(order: OrderRequest, broker: str = "generic") -> ValidationResult:
    symbol = order.symbol.strip().upper()
    if not symbol or len(symbol) > 10:
        return ValidationResult(False, "invalid_symbol")

    allowed_symbol_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
    if any(ch not in allowed_symbol_chars for ch in symbol):
        return ValidationResult(False, "invalid_symbol_chars")

    side = order.side.strip().lower()
    if side not in {"buy", "sell"}:
        return ValidationResult(False, "invalid_side")

    if order.quantity <= 0:
        return ValidationResult(False, "invalid_quantity")

    if order.quantity > 100000:
        return ValidationResult(False, "quantity_exceeds_max")

    allowed_order_types = {"market", "limit", "stop"}
    order_type = order.order_type.lower()
    if order_type not in allowed_order_types:
        return ValidationResult(False, "unsupported_order_type")

    # Session matrix baseline:
    if order.extended_hours and order_type == "stop":
        return ValidationResult(False, "stop_not_allowed_in_extended_hours")

    # Broker-specific edge matrix.
    if broker.lower() == "questrade":
        if order.extended_hours and order.quantity > 5000:
            return ValidationResult(False, "extended_hours_quantity_exceeds_questrade_cap")
        if order.extended_hours and side == "sell" and symbol.endswith(".TO"):
            return ValidationResult(False, "sell_extended_hours_tsx_restricted")

    return ValidationResult(True, "ok")
