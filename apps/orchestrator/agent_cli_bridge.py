from __future__ import annotations

import argparse
import json
import os

from src.agents.comms import AgentSessionBridge
from src.storage.audit_log import AuditLogger


def main() -> None:
    p = argparse.ArgumentParser(description="Agent CLI bridge runner")
    p.add_argument("--request-id", required=True)
    p.add_argument("--source-agent", required=True)
    p.add_argument("--target-agent", required=True)
    p.add_argument("--command", required=True)
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
        audit=audit,
    )

    env = bridge.send(
        request_id=args.request_id,
        source_agent=args.source_agent,
        target_agent=args.target_agent,
        payload={"command": args.command},
        transport="cli",
    )
    print(json.dumps(env.__dict__))


if __name__ == "__main__":
    main()
