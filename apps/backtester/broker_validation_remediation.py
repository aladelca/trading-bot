from __future__ import annotations

import argparse
import json

from src.execution.validation_remediation import build_remediation_hooks, execute_remediation_hooks


def main() -> None:
    p = argparse.ArgumentParser(description="Broker validation anomaly auto-remediation hooks")
    p.add_argument("--triage-json", required=True)
    p.add_argument("--execute", action="store_true")
    args = p.parse_args()

    triage = json.loads(args.triage_json)
    hooks = build_remediation_hooks(triage)
    runs = execute_remediation_hooks(hooks, dry_run=not args.execute)
    out = {"hooks": hooks, "runs": runs, "mode": "execute" if args.execute else "dry-run"}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
