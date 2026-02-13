from apps.orchestrator.main import run_once


def test_run_once_returns_list():
    result = run_once()
    assert isinstance(result, list)
