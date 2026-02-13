from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 0.25
    backoff_multiplier: float = 2.0


def with_retry(func: Callable[[], dict], should_retry: Callable[[dict], bool], policy: RetryPolicy) -> dict:
    attempt = 0
    delay = policy.base_delay_seconds
    last_result: dict = {"status": "error", "reason": "uninitialized"}

    while attempt < policy.max_attempts:
        attempt += 1
        result = func()
        result["attempt"] = attempt
        last_result = result

        if not should_retry(result):
            return result

        if attempt < policy.max_attempts:
            time.sleep(delay)
            delay *= policy.backoff_multiplier

    return last_result
