from src.agents.contracts import blocked, error, ok


def test_stage_envelope_builders():
    a = ok("r1", "signal", {"x": 1})
    b = blocked("r1", "risk", "limit")
    c = error("r1", "exec", "boom")

    assert a.status == "ok"
    assert b.status == "blocked"
    assert c.status == "error"
    assert a.request_id == b.request_id == c.request_id == "r1"
