from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient
from src.execution.router import ExecutionRouter


def test_router_uses_paper_mode_by_default():
    router = ExecutionRouter(QuestradeClient())
    result = router.execute(OrderRequest("SPY", "buy", 1), paper_mode=True)
    assert result["mode"] == "paper"


def test_router_blocks_live_without_flags(monkeypatch):
    monkeypatch.delenv("LIVE_TRADING_ENABLED", raising=False)
    monkeypatch.delenv("LIVE_TRADING_CONFIRM", raising=False)
    router = ExecutionRouter(QuestradeClient())
    result = router.execute(OrderRequest("SPY", "buy", 1), paper_mode=False)
    assert result["status"] == "blocked"
