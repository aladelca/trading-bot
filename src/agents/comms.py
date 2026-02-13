from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass, field

from src.agents.contracts import StageEnvelope, blocked, error, ok


@dataclass
class AgentSessionBridge:
    """Allow-listed inter-agent bridge with optional CLI transport."""

    allowed_routes: set[tuple[str, str]] = field(default_factory=set)
    cli_enabled: bool = False
    cli_allowed_commands: set[str] = field(default_factory=set)
    cli_timeout_seconds: float = 5.0

    def send(
        self,
        *,
        request_id: str,
        source_agent: str,
        target_agent: str,
        payload: dict,
        transport: str = "session-bridge",
    ) -> StageEnvelope:
        correlation_id = f"{request_id}:{source_agent}->{target_agent}"
        route = (source_agent.lower(), target_agent.lower())

        if self.allowed_routes and route not in self.allowed_routes:
            return blocked(
                request_id,
                "agent-comms",
                "route_not_allowed",
                {"route": [source_agent, target_agent]},
                source_agent=source_agent,
                target_agent=target_agent,
                transport=transport,
                correlation_id=correlation_id,
            )

        if transport == "cli":
            return self._send_cli(
                request_id=request_id,
                source_agent=source_agent,
                target_agent=target_agent,
                payload=payload,
                correlation_id=correlation_id,
            )

        return ok(
            request_id,
            "agent-comms",
            {"delivered": True, "message": payload},
            source_agent=source_agent,
            target_agent=target_agent,
            transport=transport,
            correlation_id=correlation_id,
        )

    def _send_cli(
        self,
        *,
        request_id: str,
        source_agent: str,
        target_agent: str,
        payload: dict,
        correlation_id: str,
    ) -> StageEnvelope:
        if not self.cli_enabled:
            return blocked(
                request_id,
                "agent-comms",
                "cli_transport_disabled",
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )

        command_raw = str(payload.get("command", "")).strip()
        if not command_raw:
            return blocked(
                request_id,
                "agent-comms",
                "missing_cli_command",
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )

        cmd = shlex.split(command_raw)
        if not cmd:
            return blocked(
                request_id,
                "agent-comms",
                "invalid_cli_command",
                {"command": command_raw},
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )

        base = cmd[0]
        if self.cli_allowed_commands and base not in self.cli_allowed_commands:
            return blocked(
                request_id,
                "agent-comms",
                "cli_command_not_allowed",
                {"command": base},
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )

        try:
            result = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=self.cli_timeout_seconds,
                shell=False,
            )
        except subprocess.TimeoutExpired:
            return error(
                request_id,
                "agent-comms",
                "cli_timeout",
                {"command": command_raw, "timeout_seconds": self.cli_timeout_seconds},
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )

        return ok(
            request_id,
            "agent-comms",
            {
                "delivered": result.returncode == 0,
                "command": command_raw,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "message": json.dumps(payload),
            },
            source_agent=source_agent,
            target_agent=target_agent,
            transport="cli",
            correlation_id=correlation_id,
        )
