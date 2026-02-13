from src.agents.comms import AgentSessionBridge
from src.storage.audit_log import AuditLogger


def test_agent_session_bridge_allows_route(tmp_path):
    audit = AuditLogger(str(tmp_path / "audit.db"))
    bridge = AgentSessionBridge(allowed_routes={("signal", "risk")}, audit=audit)
    env = bridge.send(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        payload={"x": 1},
    )
    assert env.status == "ok"
    assert env.stage == "agent-comms"
    assert env.correlation_id == "r1:signal->risk"
    assert audit.count_comms("ok") == 1


def test_agent_session_bridge_blocks_disallowed_route(tmp_path):
    audit = AuditLogger(str(tmp_path / "audit.db"))
    bridge = AgentSessionBridge(allowed_routes={("signal", "risk")}, audit=audit)
    env = bridge.send(
        request_id="r1",
        source_agent="risk",
        target_agent="execution",
        payload={"x": 1},
    )
    assert env.status == "blocked"
    assert env.reason == "route_not_allowed"
    assert audit.count_comms("blocked") == 1


def test_agent_cli_transport_disabled_by_default():
    bridge = AgentSessionBridge(allowed_routes={("signal", "risk")}, cli_enabled=False)
    env = bridge.send(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        payload={"command": "python -c \"print('ok')\""},
        transport="cli",
    )
    assert env.status == "blocked"
    assert env.reason == "cli_transport_disabled"


def test_agent_cli_transport_blocks_non_allowlisted_command():
    bridge = AgentSessionBridge(
        allowed_routes={("signal", "risk")},
        cli_enabled=True,
        cli_allowed_commands={"python"},
    )
    env = bridge.send(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        payload={"command": "bash -lc 'echo hello'"},
        transport="cli",
    )
    assert env.status == "blocked"
    assert env.reason == "cli_command_not_allowed"


def test_agent_cli_transport_executes_allowlisted_command():
    bridge = AgentSessionBridge(
        allowed_routes={("signal", "risk")},
        cli_enabled=True,
        cli_allowed_commands={"python"},
        cli_timeout_seconds=3,
    )
    env = bridge.send(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        payload={"command": "python -c \"print('bridge-ok')\""},
        transport="cli",
    )
    assert env.status == "ok"
    assert env.payload["returncode"] == 0
    assert "bridge-ok" in env.payload["stdout"]


def test_agent_cli_transport_dead_letter_after_retry(tmp_path):
    audit = AuditLogger(str(tmp_path / "audit.db"))
    bridge = AgentSessionBridge(
        allowed_routes={("signal", "risk")},
        cli_enabled=True,
        cli_allowed_commands={"python"},
        cli_timeout_seconds=3,
        cli_max_retries=1,
        audit=audit,
    )
    env = bridge.send(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        payload={"command": "python -c \"import sys; sys.exit(2)\""},
        transport="cli",
    )
    assert env.status == "error"
    assert env.reason == "cli_failed"
    assert env.payload["dead_letter"] is True
    assert env.payload["attempts"] == 2
    assert audit.count_comms("error") == 1
