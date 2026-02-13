import os

from apps.orchestrator.main import run


def test_run_returns_list(tmp_path):
    os.environ["AUDIT_DB_PATH"] = str(tmp_path / "audit.db")
    result = run()
    assert isinstance(result, list)
