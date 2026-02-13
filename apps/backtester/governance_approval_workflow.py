from __future__ import annotations

import argparse
import json

from src.agents.governance_approval import apply_decision, build_recommendation_package


def main() -> None:
    p = argparse.ArgumentParser(description="Governance recommendation approval workflow")
    p.add_argument("--recommendation-json", required=True)
    p.add_argument("--decision", required=True, choices=["accept", "reject", "change-set"])
    p.add_argument("--decided-by", default="human")
    p.add_argument("--overrides-json", default="{}")
    p.add_argument("--reason", default="")
    args = p.parse_args()

    recommendation = json.loads(args.recommendation_json)
    overrides = json.loads(args.overrides_json)

    package = build_recommendation_package(recommendation)
    out = apply_decision(
        package,
        decision=args.decision,
        decided_by=args.decided_by,
        overrides=overrides,
        reason=args.reason,
    )
    print(json.dumps(out))


if __name__ == "__main__":
    main()
