from __future__ import annotations

from dataclasses import dataclass

from src.broker.base import OrderRequest


@dataclass
class ValidationResult:
    ok: bool
    reason: str = ""


def validate_order_matrix(order: OrderRequest) -> ValidationResult:
    symbol = order.symbol.strip().upper()
    if not symbol or len(symbol) > 10:
        return ValidationResult(False, "invalid_symbol")

    if order.quantity <= 0:
        return ValidationResult(False, "invalid_quantity")

    allowed_order_types = {"market", "limit", "stop"}
    if order.order_type.lower() not in allowed_order_types:
        return ValidationResult(False, "unsupported_order_type")

    # Example session matrix:
    # - stop orders not allowed in extended hours in this baseline policy
    if order.extended_hours and order.order_type.lower() == "stop":
        return ValidationResult(False, "stop_not_allowed_in_extended_hours")

    return ValidationResult(True, "ok")
