from __future__ import annotations

import argparse
import json

from src.agents.governance_emergency_multisig import (
    create_emergency_override_multisig,
    evaluate_emergency_override_multisig,
)


def main() -> None:
    p = argparse.ArgumentParser(description="Governance emergency override multisig workflow")
    p.add_argument("--policy-id", required=True)
    p.add_argument("--incident-id", required=True)
    p.add_argument("--reason", default="")
    p.add_argument("--severity", default="critical")
    p.add_argument("--approvers", default="")
    p.add_argument("--min-approvals", type=int, default=2)
    p.add_argument("--override-minutes", type=int, default=30)
    p.add_argument("--changes-json", default="{}")
    p.add_argument("--override-json", default="")
    args = p.parse_args()

    if args.override_json:
        override = json.loads(args.override_json)
    else:
        approvers = [x.strip() for x in args.approvers.split(",") if x.strip()]
        override = create_emergency_override_multisig(
            policy_id=args.policy_id,
            incident_id=args.incident_id,
            reason=args.reason,
            severity=args.severity,
            approvers=approvers,
            min_approvals=args.min_approvals,
            override_minutes=args.override_minutes,
            changes=json.loads(args.changes_json),
        )

    out = {
        "override": override,
        "evaluation": evaluate_emergency_override_multisig(override),
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
