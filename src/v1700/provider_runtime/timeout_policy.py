from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeoutPolicy:
    default_timeout_seconds: int = 30
    cold_start_timeout_seconds: int = 90
    healthcheck_timeout_seconds: int = 5

    def select_timeout(self, cold_start: bool = False) -> int:
        return self.cold_start_timeout_seconds if cold_start else self.default_timeout_seconds
