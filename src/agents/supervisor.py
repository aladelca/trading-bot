from __future__ import annotations

import os
from uuid import uuid4

from src.agents.comms import AgentSessionBridge
from src.agents.contracts import StageEnvelope, blocked, error, ok
from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient
from src.config.models import PortfolioState, RiskPolicy
from src.config.settings import AppSettings
from src.data.news_ingestors.free_feed import fetch_free_news_events
from src.execution.router import ExecutionRouter
from src.risk.hard_limits import RiskLimitError, enforce_hard_limits
from src.risk.position_sizing import position_size_from_risk
from src.signals.generator import generate_signal_from_news_event
from src.storage.audit_log import AuditLogger
from src.telegram.approval import ApprovalGate


class SupervisorAgent:
    def __init__(self, settings: AppSettings, policy: RiskPolicy, audit: AuditLogger):
        self.settings = settings
        self.policy = policy
        self.audit = audit
        self.state = PortfolioState(equity=10000)

        self.approval = ApprovalGate(
            required=settings.runtime.approval_required,
            timeout_seconds=settings.runtime.approval_timeout_seconds,
        )
        self.broker = QuestradeClient(
            client_id=os.getenv("QUESTRADE_CLIENT_ID", ""),
            refresh_token=os.getenv("QUESTRADE_REFRESH_TOKEN", ""),
            practice=os.getenv("QUESTRADE_PRACTICE", "true").lower() in {"1", "true", "yes", "on"},
        )
        self.router = ExecutionRouter(self.broker)
        cli_enabled = os.getenv("AGENT_CLI_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
        cli_allowed = {
            c.strip()
            for c in os.getenv("AGENT_CLI_ALLOWED_COMMANDS", "python").split(",")
            if c.strip()
        }
        cli_timeout = float(os.getenv("AGENT_CLI_TIMEOUT_SECONDS", "5"))
        cli_retries = int(os.getenv("AGENT_CLI_MAX_RETRIES", "1"))

        self.bridge = AgentSessionBridge(
            allowed_routes={
                ("market-intel", "signal"),
                ("signal", "risk"),
                ("risk", "approval"),
                ("approval", "execution"),
            },
            cli_enabled=cli_enabled,
            cli_allowed_commands=cli_allowed,
            cli_timeout_seconds=cli_timeout,
            cli_max_retries=cli_retries,
            audit=self.audit,
        )

    def run_one_cycle(self) -> list[StageEnvelope]:
        request_id = uuid4().hex[:12]
        out: list[StageEnvelope] = []

        events = fetch_free_news_events(symbols=self.settings.runtime.symbols)
        intel_env = ok(request_id, "market-intel", {"events": events, "count": len(events)})
        out.append(intel_env)

        if not events:
            out.append(blocked(request_id, "signal", "no_events"))
            return out

        event = events[0]
        signal = generate_signal_from_news_event(event)
        if signal is None:
            out.append(blocked(request_id, "signal", "signal_threshold", {"event": event}))
            return out
        out.append(ok(request_id, "signal", {"signal": signal.__dict__}, source_agent="market-intel", target_agent="signal"))

        handoff = self.bridge.send(
            request_id=request_id,
            source_agent="signal",
            target_agent="risk",
            payload={"symbol": signal.symbol, "confidence": signal.confidence},
        )
        out.append(handoff)
        if handoff.status != "ok":
            return out

        try:
            enforce_hard_limits(self.state, self.policy)
        except RiskLimitError as exc:
            out.append(blocked(request_id, "risk", str(exc), {"signal": signal.__dict__}))
            return out

        qty = position_size_from_risk(self.state.equity, self.policy.risk_per_trade, signal.entry, signal.stop)
        if qty <= 0:
            out.append(blocked(request_id, "risk", "invalid_position_size", {"signal": signal.__dict__}))
            return out

        out.append(ok(request_id, "risk", {"quantity": qty}))

        approved, source, appr_id = self.approval.request_with_meta(signal)
        if not approved:
            out.append(blocked(request_id, "approval", "not_approved", {"source": source, "approval_id": appr_id}))
            return out
        out.append(ok(request_id, "approval", {"source": source, "approval_id": appr_id}))

        order = OrderRequest(
            symbol=signal.symbol,
            side=signal.side,
            quantity=qty,
            order_type="market",
            extended_hours=self.settings.runtime.allow_extended_hours,
        )
        try:
            fill = self.router.execute(order, paper_mode=self.settings.runtime.paper_mode, request_id=request_id)
        except Exception as exc:  # defensive boundary for stage isolation
            out.append(error(request_id, "execution", str(exc), {"order": order.__dict__}))
            return out

        out.append(ok(request_id, "execution", {"fill": fill}))
        self.audit.log("agentic_cycle", {"request_id": request_id, "stages": [e.stage for e in out], "status": [e.status for e in out]})
        return out
