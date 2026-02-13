from __future__ import annotations

from dataclasses import asdict

from src.config.models import PortfolioState, RiskPolicy
from src.config.settings import AppSettings
from src.data.news_ingestors.free_feed import fetch_free_news_events
from src.execution.paper_engine import PaperExecutionEngine
from src.risk.hard_limits import RiskLimitError, enforce_hard_limits
from src.risk.position_sizing import position_size_from_risk
from src.signals.generator import generate_signal_from_news_event
from src.storage.audit_log import AuditLogger
from src.telegram.approval import ApprovalGate


def run_once(settings: AppSettings, policy: RiskPolicy, audit: AuditLogger) -> list[dict]:
    state = PortfolioState(equity=10000)
    approval = ApprovalGate(
        required=settings.runtime.approval_required,
        timeout_seconds=settings.runtime.approval_timeout_seconds,
    )
    paper = PaperExecutionEngine()

    fills: list[dict] = []

    for event in fetch_free_news_events():
        signal = generate_signal_from_news_event(event)
        if not signal:
            continue
        if signal.confidence < settings.strategy.min_signal_score:
            continue
        if signal.symbol not in settings.runtime.symbols:
            audit.log("signal_rejected", {"reason": "symbol_not_whitelisted", **asdict(signal)})
            continue

        try:
            enforce_hard_limits(state, policy)
        except RiskLimitError as exc:
            audit.log("signal_rejected", {"reason": str(exc), **asdict(signal)})
            continue

        qty = position_size_from_risk(state.equity, policy.risk_per_trade, signal.entry, signal.stop)
        if qty <= 0:
            audit.log("signal_rejected", {"reason": "invalid_position_size", **asdict(signal)})
            continue

        approved = approval.request(signal)
        audit.log("approval", {"approved": approved, **asdict(signal)})
        if not approved:
            continue

        fill = paper.execute(
            signal.symbol,
            signal.side,
            qty,
            extended_hours=settings.runtime.allow_extended_hours,
        )
        fills.append(fill)
        audit.log("fill", fill)
        state.trades_today += 1

    return fills
