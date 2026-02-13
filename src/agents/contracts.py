from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StageEnvelope:
    request_id: str
    stage: str
    status: str  # ok|blocked|error
    payload: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    timestamp_utc: str = field(default_factory=utc_now_iso)


def ok(request_id: str, stage: str, payload: dict[str, Any]) -> StageEnvelope:
    return StageEnvelope(request_id=request_id, stage=stage, status="ok", payload=payload)


def blocked(request_id: str, stage: str, reason: str, payload: dict[str, Any] | None = None) -> StageEnvelope:
    return StageEnvelope(request_id=request_id, stage=stage, status="blocked", reason=reason, payload=payload or {})


def error(request_id: str, stage: str, reason: str, payload: dict[str, Any] | None = None) -> StageEnvelope:
    return StageEnvelope(request_id=request_id, stage=stage, status="error", reason=reason, payload=payload or {})
