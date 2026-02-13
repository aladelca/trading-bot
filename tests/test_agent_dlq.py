from src.agents.comms import AgentSessionBridge
from src.agents.dlq import replay_dead_letters
from src.storage.audit_log import AuditLogger


def test_list_dead_letters_and_replay(tmp_path):
    audit = AuditLogger(str(tmp_path / "audit.db"))

    # seed dead-letter comms event
    audit.log_comms(
        request_id="r1",
        source_agent="signal",
        target_agent="risk",
        transport="cli",
        status="error",
        reason="cli_failed",
        correlation_id="r1:signal->risk",
        payload={"dead_letter": True, "command": "python -c \"print('replay-ok')\""},
    )

    items = audit.list_dead_letters(limit=5)
    assert len(items) == 1
    assert items[0]["request_id"] == "r1"

    bridge = AgentSessionBridge(
        allowed_routes={("signal", "risk")},
        cli_enabled=True,
        cli_allowed_commands={"python"},
        cli_timeout_seconds=3,
        cli_max_retries=1,
        audit=audit,
    )

    out = replay_dead_letters(audit=audit, bridge=bridge, limit=5)
    assert len(out) == 1
    assert out[0]["replay_status"] == "ok"
    assert audit.count("comms_deadletter_replay") == 1
