from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class RuntimeSettings:
    paper_mode: bool
    timezone: str
    approval_required: bool
    allow_extended_hours: bool
    symbols: list[str]


@dataclass
class StrategySettings:
    min_signal_score: float


@dataclass
class AppSettings:
    runtime: RuntimeSettings
    strategy: StrategySettings


def _as_bool(value: str | bool | None, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return value.lower() in {"1", "true", "yes", "on"}


def load_settings(config_dir: str = "config") -> AppSettings:
    config_path = Path(config_dir)
    settings_yaml = yaml.safe_load((config_path / "settings.yaml").read_text())
    assets_yaml = yaml.safe_load((config_path / "assets_whitelist.yaml").read_text())

    paper_mode = _as_bool(os.getenv("PAPER_MODE"), settings_yaml.get("paper_mode", True))
    timezone = os.getenv("TIMEZONE", settings_yaml.get("timezone", "America/Toronto"))
    allow_extended_hours = _as_bool(
        os.getenv("ALLOW_EXTENDED_HOURS"), assets_yaml.get("allow_extended_hours", True)
    )

    symbols = os.getenv("TRADING_UNIVERSE")
    if symbols:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    else:
        symbol_list = [s.upper() for s in assets_yaml.get("symbols", ["SPY", "QQQ"])]

    min_signal_score = float(settings_yaml.get("strategy", {}).get("min_signal_score", 0.65))
    approval_required = _as_bool(os.getenv("APPROVAL_REQUIRED"), True)

    return AppSettings(
        runtime=RuntimeSettings(
            paper_mode=paper_mode,
            timezone=timezone,
            approval_required=approval_required,
            allow_extended_hours=allow_extended_hours,
            symbols=symbol_list,
        ),
        strategy=StrategySettings(min_signal_score=min_signal_score),
    )
