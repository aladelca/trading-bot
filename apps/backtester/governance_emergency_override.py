from __future__ import annotations

import argparse
import json

from src.agents.governance_emergency_override import (
    create_emergency_override,
    evaluate_emergency_override,
)


def main() -> None:
    p = argparse.ArgumentParser(description="Governance emergency override protocol")
    p.add_argument("--policy-id", required=True)
    p.add_argument("--approved-by", default="human")
    p.add_argument("--reason", default="")
    p.add_argument("--severity", default="critical")
    p.add_argument("--override-minutes", type=int, default=30)
    p.add_argument("--changes-json", default="{}")
    p.add_argument("--override-json", default="")
    args = p.parse_args()

    if args.override_json:
        override = json.loads(args.override_json)
    else:
        override = create_emergency_override(
            policy_id=args.policy_id,
            approved_by=args.approved_by,
            reason=args.reason,
            severity=args.severity,
            override_minutes=args.override_minutes,
            changes=json.loads(args.changes_json),
        )

    out = {
        "override": override,
        "evaluation": evaluate_emergency_override(override),
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
