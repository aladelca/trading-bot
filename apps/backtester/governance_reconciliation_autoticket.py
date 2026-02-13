from __future__ import annotations

import argparse
import json

from src.agents.governance_autoticket import build_reconciliation_tickets


def main() -> None:
    p = argparse.ArgumentParser(description="Generate governance reconciliation auto-tickets")
    p.add_argument("--reconciliation-json", required=True)
    p.add_argument("--default-owner", default="ops-owner")
    args = p.parse_args()

    reconciliation = json.loads(args.reconciliation_json)
    out = build_reconciliation_tickets(reconciliation, default_owner=args.default_owner)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
