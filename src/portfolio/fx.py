from __future__ import annotations


def fx_rate_for(currency: str, base_currency: str, fx_rates: dict[str, float] | None) -> float:
    c = currency.upper()
    b = base_currency.upper()
    if c == b:
        return 1.0
    fx_rates = fx_rates or {}
    return float(fx_rates.get(c, 1.0))


def convert_to_base(amount: float, currency: str, base_currency: str, fx_rates: dict[str, float] | None) -> float:
    return float(amount) * fx_rate_for(currency, base_currency, fx_rates)
