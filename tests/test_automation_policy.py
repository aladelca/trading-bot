from src.agents.automation_policy import choose_auto_approve_tier, tier_allows_auto_approve


def test_choose_auto_approve_tier():
    assert choose_auto_approve_tier(0.96) == "tier-1"
    assert choose_auto_approve_tier(0.90) == "tier-2"
    assert choose_auto_approve_tier(0.86) == "tier-3"
    assert choose_auto_approve_tier(0.70) == "manual"


def test_tier_allows_auto_approve():
    assert tier_allows_auto_approve("tier-1", "SPY", {"SPY", "QQQ"}) is True
    assert tier_allows_auto_approve("manual", "SPY", {"SPY"}) is False


def test_tier_allows_auto_approve_respects_allowed_tiers():
    assert tier_allows_auto_approve("tier-3", "SPY", {"SPY"}, allowed_tiers={"tier-1", "tier-2"}) is False
    assert tier_allows_auto_approve("tier-2", "SPY", {"SPY"}, allowed_tiers={"tier-1", "tier-2"}) is True
