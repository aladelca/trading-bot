from src.config.settings import load_settings


def test_load_settings_has_symbols():
    settings = load_settings("config")
    assert settings.runtime.symbols
    assert "SPY" in settings.runtime.symbols
