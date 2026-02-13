from dataclasses import dataclass


@dataclass
class RiskPolicy:
    risk_per_trade: float = 0.005
    max_trades_per_day: int = 4
    max_open_positions: int = 2
    daily_max_drawdown: float = 0.02
    weekly_max_drawdown: float = 0.05


@dataclass
class PortfolioState:
    equity: float
    day_pnl_pct: float = 0.0
    week_pnl_pct: float = 0.0
    open_positions: int = 0
    trades_today: int = 0
