from src.agents.comms import AgentSessionBridge


def test_agent_session_bridge_allows_route():
    bridge = AgentSessionBridge(allowed_routes={("signal", "risk")})
    env = bridge.send(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        payload={"x": 1},
    )
    assert env.status == "ok"
    assert env.stage == "agent-comms"
    assert env.correlation_id == "r1:signal->risk"


def test_agent_session_bridge_blocks_disallowed_route():
    bridge = AgentSessionBridge(allowed_routes={("signal", "risk")})
    env = bridge.send(
        request_id="r1",
        source_agent="risk",
        target_agent="execution",
        payload={"x": 1},
    )
    assert env.status == "blocked"
    assert env.reason == "route_not_allowed"


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
