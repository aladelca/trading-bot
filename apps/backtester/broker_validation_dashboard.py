from __future__ import annotations

import argparse
import json

from src.execution.validation_metrics import compute_validation_metrics, evaluate_validation_alerts


def main() -> None:
    p = argparse.ArgumentParser(description="Broker validation rollout dashboard")
    p.add_argument("--records-json", required=True, help="JSON array of broker submission result records")
    p.add_argument("--max-blocked-rate", type=float, default=0.25)
    p.add_argument("--max-broker-error-rate", type=float, default=0.10)
    p.add_argument("--max-auto-reverted-rate", type=float, default=0.05)
    args = p.parse_args()

    records = json.loads(args.records_json)
    metrics = compute_validation_metrics(records)
    alerts = evaluate_validation_alerts(
        metrics,
        max_blocked_rate=args.max_blocked_rate,
        max_broker_error_rate=args.max_broker_error_rate,
        max_auto_reverted_rate=args.max_auto_reverted_rate,
    )
    out = {
        "metrics": metrics,
        "alerts": alerts,
        "status": "alert" if alerts else "ok",
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
