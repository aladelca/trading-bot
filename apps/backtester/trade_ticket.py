from __future__ import annotations

import argparse
import json

from src.broker.base import OrderRequest
from src.execution.trade_ticket import build_trade_ticket


def main() -> None:
    p = argparse.ArgumentParser(description="Build manual trade ticket for retail broker execution")
    p.add_argument("--symbol", required=True)
    p.add_argument("--side", required=True)
    p.add_argument("--quantity", required=True, type=int)
    p.add_argument("--order-type", default="market")
    p.add_argument("--extended-hours", action="store_true")
    p.add_argument("--strategy-id", default="")
    p.add_argument("--rationale", default="")
    args = p.parse_args()

    order = OrderRequest(
        symbol=args.symbol,
        side=args.side,
        quantity=args.quantity,
        order_type=args.order_type,
        extended_hours=args.extended_hours,
    )
    print(json.dumps(build_trade_ticket(order, strategy_id=args.strategy_id, rationale=args.rationale)))


if __name__ == "__main__":
    main()
