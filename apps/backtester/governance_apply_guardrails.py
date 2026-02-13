from __future__ import annotations

import argparse
import json

from src.agents.governance_apply import build_rollback_template, evaluate_application_guardrails


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate governance apply guardrails and build rollback template")
    p.add_argument("--approved-package-json", required=True)
    p.add_argument("--previous-policy-json", default="{}")
    args = p.parse_args()

    package = json.loads(args.approved_package_json)
    previous = json.loads(args.previous_policy_json)

    guard = evaluate_application_guardrails(package)
    out = {"guardrails": guard}
    if guard.get("ok"):
        out["rollback_template"] = build_rollback_template(package, previous_policy=previous)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
