import os

from dotenv import load_dotenv

from src.config.models import PortfolioState, RiskPolicy
from src.data.news_ingestors.free_feed import fetch_free_news_events
from src.execution.paper_engine import PaperExecutionEngine
from src.risk.hard_limits import RiskLimitError, enforce_hard_limits
from src.risk.position_sizing import position_size_from_risk
from src.signals.generator import generate_signal_from_news_event
from src.telegram.approval import ApprovalGate


def run_once() -> list[dict]:
    load_dotenv()
    policy = RiskPolicy(
        risk_per_trade=float(os.getenv("RISK_PER_TRADE", "0.005")),
        max_trades_per_day=int(os.getenv("MAX_TRADES_PER_DAY", "4")),
        max_open_positions=int(os.getenv("MAX_OPEN_POSITIONS", "2")),
        daily_max_drawdown=float(os.getenv("DAILY_MAX_DRAWDOWN", "0.02")),
        weekly_max_drawdown=float(os.getenv("WEEKLY_MAX_DRAWDOWN", "0.05")),
    )
    state = PortfolioState(equity=10000)
    approval = ApprovalGate()
    paper = PaperExecutionEngine()

    fills = []
    for event in fetch_free_news_events():
        signal = generate_signal_from_news_event(event)
        if not signal:
            continue
        try:
            enforce_hard_limits(state, policy)
        except RiskLimitError:
            continue

        qty = position_size_from_risk(state.equity, policy.risk_per_trade, signal.entry, signal.stop)
        if qty <= 0:
            continue

        if not approval.request(signal):
            continue

        fill = paper.execute(signal.symbol, signal.side, qty, extended_hours=True)
        fills.append(fill)
        state.trades_today += 1

    return fills


if __name__ == "__main__":
    print(run_once())
