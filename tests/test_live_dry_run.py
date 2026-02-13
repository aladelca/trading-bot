from src.broker.base import OrderRequest
from src.broker.questrade.client import QuestradeClient
from src.execution.router import ExecutionRouter


def test_live_router_uses_dry_run_when_enabled(monkeypatch):
    monkeypatch.setenv("LIVE_TRADING_ENABLED", "true")
    monkeypatch.setenv("LIVE_TRADING_CONFIRM", "I_UNDERSTAND_LIVE_TRADING_RISK")
    monkeypatch.setenv("LIVE_ORDER_DRY_RUN", "true")

    router = ExecutionRouter(QuestradeClient())
    out = router.execute(OrderRequest("SPY", "buy", 1), paper_mode=False)
    assert out["status"] == "dry-run"
