from src.config.models import PortfolioState, RiskPolicy


class RiskLimitError(Exception):
    pass


def enforce_hard_limits(state: PortfolioState, policy: RiskPolicy) -> None:
    if state.day_pnl_pct <= -policy.daily_max_drawdown:
        raise RiskLimitError("Daily drawdown limit reached")
    if state.week_pnl_pct <= -policy.weekly_max_drawdown:
        raise RiskLimitError("Weekly drawdown limit reached")
    if state.open_positions >= policy.max_open_positions:
        raise RiskLimitError("Max open positions reached")
    if state.trades_today >= policy.max_trades_per_day:
        raise RiskLimitError("Max trades per day reached")
