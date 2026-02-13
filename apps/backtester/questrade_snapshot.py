from __future__ import annotations

import argparse
import json
import os

from src.broker.questrade.client import QuestradeClient


def main() -> None:
    p = argparse.ArgumentParser(description="Questrade balances/positions/quotes snapshot")
    p.add_argument("--symbols", default="SPY,QQQ")
    p.add_argument("--account-id", default="")
    args = p.parse_args()

    refresh_token = os.getenv("QUESTRADE_REFRESH_TOKEN", "")
    client = QuestradeClient(refresh_token=refresh_token)

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    out = client.get_account_market_snapshot(symbols=symbols, account_id=args.account_id)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
