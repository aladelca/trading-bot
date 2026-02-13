from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass
class PositionState:
    qty: int = 0
    avg_cost: float = 0.0
    realized_pnl: float = 0.0


def _signed_qty(side: str, quantity: int) -> int:
    return quantity if side.lower() == "buy" else -quantity


def _apply_fill(state: PositionState, side: str, quantity: int, price: float) -> PositionState:
    signed = _signed_qty(side, quantity)
    if state.qty == 0:
        state.qty = signed
        state.avg_cost = price
        return state

    # same direction -> weighted avg
    if (state.qty > 0 and signed > 0) or (state.qty < 0 and signed < 0):
        total_abs = abs(state.qty) + abs(signed)
        state.avg_cost = ((abs(state.qty) * state.avg_cost) + (abs(signed) * price)) / total_abs
        state.qty += signed
        return state

    # opposite direction -> realize PnL on closing leg
    close_qty = min(abs(state.qty), abs(signed))
    if state.qty > 0:
        # closing long with sell
        state.realized_pnl += close_qty * (price - state.avg_cost)
    else:
        # closing short with buy
        state.realized_pnl += close_qty * (state.avg_cost - price)

    new_qty = state.qty + signed
    if new_qty == 0:
        state.qty = 0
        state.avg_cost = 0.0
        return state

    # flip direction: remainder starts new position at fill price
    if (state.qty > 0 and new_qty < 0) or (state.qty < 0 and new_qty > 0):
        state.qty = new_qty
        state.avg_cost = price
        return state

    state.qty = new_qty
    return state


def compute_positions_and_pnl(db_path: str = "data/portfolio.db", mark_prices: dict[str, float] | None = None) -> dict:
    mark_prices = mark_prices or {}
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT symbol, side, quantity, price FROM trades ORDER BY id ASC").fetchall()
    except sqlite3.OperationalError:
        rows = []

    per_symbol: dict[str, PositionState] = {}
    for symbol, side, quantity, price in rows:
        s = per_symbol.setdefault(symbol, PositionState())
        per_symbol[symbol] = _apply_fill(s, side, int(quantity), float(price))

    realized_total = 0.0
    unrealized_total = 0.0
    symbols = {}

    for symbol, st in per_symbol.items():
        realized_total += st.realized_pnl
        mark = mark_prices.get(symbol, st.avg_cost)
        if st.qty > 0:
            unrealized = st.qty * (mark - st.avg_cost)
        elif st.qty < 0:
            unrealized = abs(st.qty) * (st.avg_cost - mark)
        else:
            unrealized = 0.0
        unrealized_total += unrealized
        symbols[symbol] = {
            "qty": st.qty,
            "avg_cost": round(st.avg_cost, 6),
            "realized_pnl": round(st.realized_pnl, 6),
            "unrealized_pnl": round(unrealized, 6),
            "mark_price": mark,
        }

    return {
        "symbols": symbols,
        "realized_pnl_total": round(realized_total, 6),
        "unrealized_pnl_total": round(unrealized_total, 6),
        "equity_pnl_total": round(realized_total + unrealized_total, 6),
    }
