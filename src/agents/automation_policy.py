from __future__ import annotations


def choose_auto_approve_tier(confidence: float) -> str:
    if confidence >= 0.95:
        return "tier-1"
    if confidence >= 0.90:
        return "tier-2"
    if confidence >= 0.85:
        return "tier-3"
    return "manual"


def tier_allows_auto_approve(
    tier: str,
    symbol: str,
    allowed_symbols: set[str],
    allowed_tiers: set[str] | None = None,
) -> bool:
    if tier == "manual":
        return False
    tiers = {t.lower() for t in (allowed_tiers or {"tier-1", "tier-2", "tier-3"})}
    if tier.lower() not in tiers:
        return False
    return symbol.upper() in {s.upper() for s in allowed_symbols}
