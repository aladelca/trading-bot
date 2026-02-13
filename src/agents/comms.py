from __future__ import annotations

from dataclasses import dataclass, field

from src.agents.contracts import StageEnvelope, blocked, ok


@dataclass
class AgentSessionBridge:
    """Allow-listed inter-agent session/CLI bridge scaffold."""

    allowed_routes: set[tuple[str, str]] = field(default_factory=set)

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

        return ok(
            request_id,
            "agent-comms",
            {"delivered": True, "message": payload},
            source_agent=source_agent,
            target_agent=target_agent,
            transport=transport,
            correlation_id=correlation_id,
        )
