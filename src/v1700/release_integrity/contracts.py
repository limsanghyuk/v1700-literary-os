from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

CheckStatus = Literal["pass", "blocked"]


@dataclass(frozen=True)
class IntegrityCheck:
    name: str
    status: CheckStatus
    expected: str
    actual: str
    path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegrityReport:
    stage: str
    title: str
    status: CheckStatus
    checks: tuple[IntegrityCheck, ...]
    issues: tuple[str, ...] = field(default_factory=tuple)
    counters: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["checks"] = [check.to_dict() for check in self.checks]
        return payload
