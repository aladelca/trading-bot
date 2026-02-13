from __future__ import annotations

import argparse
import json

from src.execution.validation_triage import build_validation_anomaly_triage


def main() -> None:
    p = argparse.ArgumentParser(description="Broker validation anomaly triage and remediation matrix")
    p.add_argument("--records-json", required=True, help="JSON array of broker validation records")
    p.add_argument("--max-blocked-rate", type=float, default=0.25)
    p.add_argument("--max-broker-error-rate", type=float, default=0.10)
    p.add_argument("--max-auto-reverted-rate", type=float, default=0.05)
    args = p.parse_args()

    records = json.loads(args.records_json)
    out = build_validation_anomaly_triage(
        records,
        max_blocked_rate=args.max_blocked_rate,
        max_broker_error_rate=args.max_broker_error_rate,
        max_auto_reverted_rate=args.max_auto_reverted_rate,
    )
    print(json.dumps(out))


if __name__ == "__main__":
    main()
