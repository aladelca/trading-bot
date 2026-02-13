from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.agents.threshold_calibration import ReplayScenario, calibrate_thresholds


def main() -> None:
    p = argparse.ArgumentParser(description="Governance threshold calibration from replay pack")
    p.add_argument("--replay-pack", required=True, help="Path to replay scenarios JSON")
    p.add_argument("--candidates", default="0.85,0.88,0.90,0.92,0.95")
    args = p.parse_args()

    path = Path(args.replay_pack)
    scenarios_raw = json.loads(path.read_text())
    scenarios = [
        ReplayScenario(
            confidence=float(x["confidence"]),
            pnl_outcome=float(x["pnl_outcome"]),
            approved=bool(x["approved"]),
        )
        for x in scenarios_raw
    ]
    candidates = [float(x.strip()) for x in args.candidates.split(",") if x.strip()]

    out = calibrate_thresholds(scenarios, candidates)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
