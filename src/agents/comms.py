from __future__ import annotations

import json
import shlex
import subprocess
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.agents.contracts import StageEnvelope, blocked, error, ok

if TYPE_CHECKING:
    from src.storage.audit_log import AuditLogger


@dataclass
class AgentSessionBridge:
    """Allow-listed inter-agent bridge with optional CLI transport."""

    allowed_routes: set[tuple[str, str]] = field(default_factory=set)
    cli_enabled: bool = False
    cli_allowed_commands: set[str] = field(default_factory=set)
    cli_timeout_seconds: float = 5.0
    cli_max_retries: int = 1
    cli_retry_backoff_seconds: float = 0.2
    audit: AuditLogger | None = None

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
            env = blocked(
                request_id,
                "agent-comms",
                "route_not_allowed",
                {"route": [source_agent, target_agent]},
                source_agent=source_agent,
                target_agent=target_agent,
                transport=transport,
                correlation_id=correlation_id,
            )
            self._audit_env(env)
            return env

        if transport == "cli":
            return self._send_cli(
                request_id=request_id,
                source_agent=source_agent,
                target_agent=target_agent,
                payload=payload,
                correlation_id=correlation_id,
            )

        env = ok(
            request_id,
            "agent-comms",
            {"delivered": True, "message": payload},
            source_agent=source_agent,
            target_agent=target_agent,
            transport=transport,
            correlation_id=correlation_id,
        )
        self._audit_env(env)
        return env

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
            env = blocked(
                request_id,
                "agent-comms",
                "cli_transport_disabled",
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )
            self._audit_env(env)
            return env

        command_raw = str(payload.get("command", "")).strip()
        if not command_raw:
            env = blocked(
                request_id,
                "agent-comms",
                "missing_cli_command",
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )
            self._audit_env(env)
            return env

        cmd = shlex.split(command_raw)
        if not cmd:
            env = blocked(
                request_id,
                "agent-comms",
                "invalid_cli_command",
                {"command": command_raw},
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )
            self._audit_env(env)
            return env

        base = cmd[0]
        if self.cli_allowed_commands and base not in self.cli_allowed_commands:
            env = blocked(
                request_id,
                "agent-comms",
                "cli_command_not_allowed",
                {"command": base},
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )
            self._audit_env(env)
            return env

        attempts = 0
        while attempts <= self.cli_max_retries:
            attempts += 1
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
                if attempts <= self.cli_max_retries:
                    time.sleep(self.cli_retry_backoff_seconds * attempts)
                    continue
                env = error(
                    request_id,
                    "agent-comms",
                    "cli_timeout",
                    {
                        "command": command_raw,
                        "timeout_seconds": self.cli_timeout_seconds,
                        "attempts": attempts,
                        "dead_letter": True,
                    },
                    source_agent=source_agent,
                    target_agent=target_agent,
                    transport="cli",
                    correlation_id=correlation_id,
                )
                self._audit_env(env)
                return env

            if result.returncode == 0:
                env = ok(
                    request_id,
                    "agent-comms",
                    {
                        "delivered": True,
                        "command": command_raw,
                        "returncode": result.returncode,
                        "stdout": result.stdout.strip(),
                        "stderr": result.stderr.strip(),
                        "attempts": attempts,
                        "message": json.dumps(payload),
                    },
                    source_agent=source_agent,
                    target_agent=target_agent,
                    transport="cli",
                    correlation_id=correlation_id,
                )
                self._audit_env(env)
                return env

            if attempts <= self.cli_max_retries:
                time.sleep(self.cli_retry_backoff_seconds * attempts)
                continue

            env = error(
                request_id,
                "agent-comms",
                "cli_failed",
                {
                    "delivered": False,
                    "command": command_raw,
                    "returncode": result.returncode,
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip(),
                    "attempts": attempts,
                    "dead_letter": True,
                },
                source_agent=source_agent,
                target_agent=target_agent,
                transport="cli",
                correlation_id=correlation_id,
            )
            self._audit_env(env)
            return env

        env = error(
            request_id,
            "agent-comms",
            "cli_failed",
            {"dead_letter": True, "attempts": attempts},
            source_agent=source_agent,
            target_agent=target_agent,
            transport="cli",
            correlation_id=correlation_id,
        )
        self._audit_env(env)
        return env

    def _audit_env(self, env: StageEnvelope) -> None:
        if not self.audit:
            return
        self.audit.log_comms(
            request_id=env.request_id,
            source_agent=env.source_agent,
            target_agent=env.target_agent,
            transport=env.transport,
            status=env.status,
            reason=env.reason,
            correlation_id=env.correlation_id,
            payload=env.payload,
        )
