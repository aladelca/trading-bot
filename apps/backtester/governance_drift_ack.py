from __future__ import annotations

import argparse
import json

from src.agents.governance_drift_ack import create_drift_ack, evaluate_drift_ack


def main() -> None:
    p = argparse.ArgumentParser(description="Governance drift acknowledgement workflow")
    p.add_argument("--policy-id", required=True)
    p.add_argument("--severity", default="medium")
    p.add_argument("--acknowledged-by", default="human")
    p.add_argument("--valid-minutes", type=int, default=60)
    p.add_argument("--ack-json", default="")
    args = p.parse_args()

    if args.ack_json:
        ack = json.loads(args.ack_json)
    else:
        ack = create_drift_ack(
            policy_id=args.policy_id,
            severity=args.severity,
            acknowledged_by=args.acknowledged_by,
            valid_for_minutes=args.valid_minutes,
        )

    out = {"ack": ack, "evaluation": evaluate_drift_ack(ack)}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
