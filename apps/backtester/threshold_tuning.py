from __future__ import annotations

import argparse
import json

from src.agents.threshold_tuning import recommend_governance_thresholds


def main() -> None:
    p = argparse.ArgumentParser(description="Governance threshold tuning from paper KPI metrics")
    p.add_argument("--kpi-json", default="{}", help="JSON object with approval_rate, equity_pnl_total, signals_rejected")
    args = p.parse_args()

    kpi = json.loads(args.kpi_json)
    out = recommend_governance_thresholds(kpi)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
