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
