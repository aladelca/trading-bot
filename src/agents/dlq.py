from __future__ import annotations

from src.agents.comms import AgentSessionBridge
from src.storage.audit_log import AuditLogger


def replay_dead_letters(audit: AuditLogger, bridge: AgentSessionBridge, limit: int = 10) -> list[dict]:
    items = audit.list_dead_letters(limit=limit)
    out: list[dict] = []
    for item in items:
        command = str(item.get("payload", {}).get("command", "")).strip()
        if not command:
            continue
        env = bridge.send(
            request_id=f"replay-{item['request_id']}",
            source_agent=item["source_agent"],
            target_agent=item["target_agent"],
            payload={"command": command},
            transport=item.get("transport", "cli"),
        )
        row = {
            "dead_letter_id": item["id"],
            "original_request_id": item["request_id"],
            "replay_status": env.status,
            "replay_reason": env.reason,
            "correlation_id": env.correlation_id,
        }
        audit.log("comms_deadletter_replay", row)
        out.append(row)
    return out
