from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QualityMetric:
    name: str
    status: str
    score: float
    threshold: float
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "score": round(float(self.score), 6),
            "threshold": round(float(self.threshold), 6),
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class BoundaryRule:
    name: str
    status: str
    provider_generation_allowed: bool
    runtime_render_allowed: bool
    write_allowed: bool
    hidden_payload_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "provider_generation_allowed": self.provider_generation_allowed,
            "runtime_render_allowed": self.runtime_render_allowed,
            "write_allowed": self.write_allowed,
            "hidden_payload_allowed": self.hidden_payload_allowed,
            "evidence": self.evidence,
        }
