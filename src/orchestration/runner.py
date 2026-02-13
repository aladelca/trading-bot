from __future__ import annotations

import os
from dataclasses import asdict

from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient
from src.config.models import PortfolioState, RiskPolicy
from src.config.settings import AppSettings
from src.data.news_ingestors.free_feed import fetch_free_news_events
from src.execution.router import ExecutionRouter
from src.portfolio.ledger import PortfolioLedger
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

    broker = QuestradeClient(
        client_id=os.getenv("QUESTRADE_CLIENT_ID", ""),
        refresh_token=os.getenv("QUESTRADE_REFRESH_TOKEN", ""),
        practice=os.getenv("QUESTRADE_PRACTICE", "true").lower() in {"1", "true", "yes", "on"},
    )
    router = ExecutionRouter(broker)
    ledger = PortfolioLedger(os.getenv("PORTFOLIO_DB_PATH", "data/portfolio.db"))

    fills: list[dict] = []

    for event in fetch_free_news_events(symbols=settings.runtime.symbols):
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

        approved, source, request_id = approval.request_with_meta(signal)
        audit.log("approval", {"approved": approved, "source": source, "request_id": request_id, **asdict(signal)})
        if request_id:
            audit.save_decision(request_id, approved, source)
        if not approved:
            continue

        order = OrderRequest(
            symbol=signal.symbol,
            side=signal.side,
            quantity=qty,
            order_type="market",
            extended_hours=settings.runtime.allow_extended_hours,
        )
        fill = router.execute(order, paper_mode=settings.runtime.paper_mode, request_id=request_id)
        fills.append(fill)
        audit.log("fill", fill)

        mode = fill.get("mode", "unknown")
        status = fill.get("status", "unknown")
        if status in {"filled", "dry-run", "submitted", "paper-simulated"}:
            ledger.record_trade(
                symbol=signal.symbol,
                side=signal.side,
                quantity=qty,
                price=signal.entry,
                status=status,
                mode=mode,
                currency=os.getenv("TRADE_CURRENCY", "USD"),
            )

        state.trades_today += 1

    return fills
