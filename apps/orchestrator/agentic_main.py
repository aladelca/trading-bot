import os

from dotenv import load_dotenv

from src.agents.supervisor import SupervisorAgent
from src.config.models import RiskPolicy
from src.config.settings import load_settings
from src.storage.audit_log import AuditLogger


def run_agentic_cycle() -> list[dict]:
    load_dotenv()
    settings = load_settings("config")
    policy = RiskPolicy(
        risk_per_trade=float(os.getenv("RISK_PER_TRADE", "0.005")),
        max_trades_per_day=int(os.getenv("MAX_TRADES_PER_DAY", "4")),
        max_open_positions=int(os.getenv("MAX_OPEN_POSITIONS", "2")),
        daily_max_drawdown=float(os.getenv("DAILY_MAX_DRAWDOWN", "0.02")),
        weekly_max_drawdown=float(os.getenv("WEEKLY_MAX_DRAWDOWN", "0.05")),
    )
    audit = AuditLogger(os.getenv("AUDIT_DB_PATH", "data/audit.db"))

    supervisor = SupervisorAgent(settings, policy, audit)
    envs = supervisor.run_one_cycle()
    return [e.__dict__ for e in envs]


if __name__ == "__main__":
    print(run_agentic_cycle())
