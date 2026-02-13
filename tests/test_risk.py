from src.config.models import PortfolioState, RiskPolicy
from src.risk.hard_limits import RiskLimitError, enforce_hard_limits
from src.risk.position_sizing import position_size_from_risk


def test_position_sizing_positive_qty():
    qty = position_size_from_risk(10000, 0.005, 100, 99)
    assert qty == 50


def test_hard_limit_daily_drawdown_blocks():
    state = PortfolioState(equity=10000, day_pnl_pct=-0.03)
    policy = RiskPolicy(daily_max_drawdown=0.02)
    try:
        enforce_hard_limits(state, policy)
        assert False, "Expected RiskLimitError"
    except RiskLimitError:
        assert True
