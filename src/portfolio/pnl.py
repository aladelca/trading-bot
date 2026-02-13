from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from src.portfolio.fx import convert_to_base


@dataclass
class PositionState:
    qty: int = 0
    avg_cost_base: float = 0.0
    realized_pnl_base: float = 0.0
    currency: str = "USD"


def _signed_qty(side: str, quantity: int) -> int:
    return quantity if side.lower() == "buy" else -quantity


def _apply_fill(state: PositionState, side: str, quantity: int, price_base: float, currency: str) -> PositionState:
    signed = _signed_qty(side, quantity)
    state.currency = currency.upper()

    if state.qty == 0:
        state.qty = signed
        state.avg_cost_base = price_base
        return state

    if (state.qty > 0 and signed > 0) or (state.qty < 0 and signed < 0):
        total_abs = abs(state.qty) + abs(signed)
        state.avg_cost_base = ((abs(state.qty) * state.avg_cost_base) + (abs(signed) * price_base)) / total_abs
        state.qty += signed
        return state

    close_qty = min(abs(state.qty), abs(signed))
    if state.qty > 0:
        state.realized_pnl_base += close_qty * (price_base - state.avg_cost_base)
    else:
        state.realized_pnl_base += close_qty * (state.avg_cost_base - price_base)

    new_qty = state.qty + signed
    if new_qty == 0:
        state.qty = 0
        state.avg_cost_base = 0.0
        return state

    if (state.qty > 0 and new_qty < 0) or (state.qty < 0 and new_qty > 0):
        state.qty = new_qty
        state.avg_cost_base = price_base
        return state

    state.qty = new_qty
    return state


def compute_positions_and_pnl(
    db_path: str = "data/portfolio.db",
    mark_prices: dict[str, float] | None = None,
    fx_rates: dict[str, float] | None = None,
    base_currency: str = "USD",
) -> dict:
    mark_prices = mark_prices or {}
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT symbol, side, quantity, price, currency FROM trades ORDER BY id ASC").fetchall()
    except sqlite3.OperationalError:
        rows = []

    per_symbol: dict[str, PositionState] = {}
    for symbol, side, quantity, price, currency in rows:
        ccy = str(currency or base_currency).upper()
        px_base = convert_to_base(float(price), ccy, base_currency, fx_rates)
        s = per_symbol.setdefault(symbol, PositionState(currency=ccy))
        per_symbol[symbol] = _apply_fill(s, side, int(quantity), px_base, ccy)

    realized_total = 0.0
    unrealized_total = 0.0
    symbols = {}

    for symbol, st in per_symbol.items():
        realized_total += st.realized_pnl_base
        mark_local = mark_prices.get(symbol, st.avg_cost_base)
        mark_base = convert_to_base(float(mark_local), st.currency, base_currency, fx_rates)

        if st.qty > 0:
            unrealized = st.qty * (mark_base - st.avg_cost_base)
        elif st.qty < 0:
            unrealized = abs(st.qty) * (st.avg_cost_base - mark_base)
        else:
            unrealized = 0.0

        unrealized_total += unrealized
        symbols[symbol] = {
            "qty": st.qty,
            "currency": st.currency,
            "avg_cost_base": round(st.avg_cost_base, 6),
            "realized_pnl_base": round(st.realized_pnl_base, 6),
            "unrealized_pnl_base": round(unrealized, 6),
            "mark_price_local": mark_local,
            "mark_price_base": round(mark_base, 6),
        }

    return {
        "base_currency": base_currency.upper(),
        "symbols": symbols,
        "realized_pnl_total": round(realized_total, 6),
        "unrealized_pnl_total": round(unrealized_total, 6),
        "equity_pnl_total": round(realized_total + unrealized_total, 6),
    }
