from __future__ import annotations

import argparse
import json

from src.agents.policy_simulation import simulate_governance_policy


def main() -> None:
    p = argparse.ArgumentParser(description="Governance policy simulation sandbox")
    p.add_argument("--confidence", type=float, required=True)
    p.add_argument("--symbol", required=True)
    p.add_argument("--allowed-symbols", default="SPY,QQQ")
    p.add_argument("--allowed-tiers", default="tier-1,tier-2")
    p.add_argument("--current-kpi-json", default="{}")
    p.add_argument("--baseline-kpi-json", default="{}")
    args = p.parse_args()

    current_kpi = json.loads(args.current_kpi_json)
    baseline_kpi = json.loads(args.baseline_kpi_json)

    out = simulate_governance_policy(
        confidence=args.confidence,
        symbol=args.symbol,
        allowed_symbols={s.strip().upper() for s in args.allowed_symbols.split(",") if s.strip()},
        allowed_tiers={t.strip().lower() for t in args.allowed_tiers.split(",") if t.strip()},
        current_kpi=current_kpi,
        baseline_kpi=baseline_kpi,
    )
    print(json.dumps(out))


if __name__ == "__main__":
    main()
