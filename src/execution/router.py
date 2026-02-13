from __future__ import annotations

from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient
from src.execution.guardrails import LiveExecutionBlocked, assert_live_execution_allowed
from src.execution.paper_engine import PaperExecutionEngine


class ExecutionRouter:
    def __init__(self, broker: QuestradeClient):
        self.broker = broker
        self.paper = PaperExecutionEngine()

    def execute(self, order: OrderRequest, paper_mode: bool = True) -> dict:
        if paper_mode:
            return self.paper.execute(order.symbol, order.side, order.quantity, order.extended_hours)

        try:
            assert_live_execution_allowed()
        except LiveExecutionBlocked as exc:
            return {
                "status": "blocked",
                "reason": str(exc),
                "mode": "live",
            }

        return self.broker.place_order(order)
