from __future__ import annotations

import argparse
import json
import os

from src.agents.comms import AgentSessionBridge
from src.agents.dlq import replay_dead_letters
from src.storage.audit_log import AuditLogger


def main() -> None:
    p = argparse.ArgumentParser(description="Replay dead-letter comms events")
    p.add_argument("--limit", type=int, default=10)
    args = p.parse_args()

    allowed_routes_raw = os.getenv("AGENT_ALLOWED_ROUTES", "signal:risk")
    allowed_routes = {
        tuple(r.split(":", 1))
        for r in [x.strip() for x in allowed_routes_raw.split(",") if x.strip()]
        if len(r.split(":", 1)) == 2
    }
    allowed_commands = {c.strip() for c in os.getenv("AGENT_CLI_ALLOWED_COMMANDS", "python").split(",") if c.strip()}

    audit = AuditLogger(os.getenv("AUDIT_DB_PATH", "data/audit.db"))
    bridge = AgentSessionBridge(
        allowed_routes={(a.lower(), b.lower()) for a, b in allowed_routes},
        cli_enabled=os.getenv("AGENT_CLI_ENABLED", "false").lower() in {"1", "true", "yes", "on"},
        cli_allowed_commands=allowed_commands,
        cli_timeout_seconds=float(os.getenv("AGENT_CLI_TIMEOUT_SECONDS", "5")),
        cli_max_retries=int(os.getenv("AGENT_CLI_MAX_RETRIES", "1")),
        cli_retry_backoff_seconds=float(os.getenv("AGENT_CLI_RETRY_BACKOFF_SECONDS", "0.2")),
        audit=audit,
    )

    out = replay_dead_letters(audit=audit, bridge=bridge, limit=args.limit)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
