from src.portfolio.fx import convert_to_base, fx_rate_for


def test_fx_rate_for_base_currency_is_one():
    assert fx_rate_for("USD", "USD", {"USD": 1.0}) == 1.0


def test_convert_to_base_with_fx_map():
    assert convert_to_base(100, "CAD", "USD", {"CAD": 0.75}) == 75.0
