from src.telegram.client import parse_callback_decision


def test_parse_callback_decision_approve():
    assert parse_callback_decision("approve:abc123", "abc123") is True


def test_parse_callback_decision_reject():
    assert parse_callback_decision("reject:abc123", "abc123") is False


def test_parse_callback_decision_ignores_other_ids():
    assert parse_callback_decision("approve:zzz999", "abc123") is None
