from src.agents.supervisor import SupervisorAgent
from src.config.models import RiskPolicy
from src.config.settings import load_settings
from src.storage.audit_log import AuditLogger


def test_supervisor_one_cycle_returns_stages(tmp_path, monkeypatch):
    monkeypatch.setenv("AUTO_APPROVE_ENABLED", "true")
    monkeypatch.setenv("AUTO_APPROVE_MIN_CONFIDENCE", "0.60")
    monkeypatch.setenv("AUTO_APPROVE_SYMBOLS", "SPY,QQQ")

    settings = load_settings("config")
    policy = RiskPolicy()
    audit = AuditLogger(str(tmp_path / "audit.db"))

    sup = SupervisorAgent(settings, policy, audit)
    envs = sup.run_one_cycle()

    assert len(envs) >= 3
    assert envs[0].stage == "market-intel"
    assert any(e.stage == "signal" for e in envs)
