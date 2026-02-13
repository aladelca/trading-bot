from __future__ import annotations

import argparse
import json

from src.agents.governance_signoff import evaluate_signoff_matrix


def main() -> None:
    p = argparse.ArgumentParser(description="Governance deployment sign-off matrix evaluator")
    p.add_argument("--signoff-json", required=True)
    args = p.parse_args()

    payload = json.loads(args.signoff_json)
    out = evaluate_signoff_matrix(payload)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
