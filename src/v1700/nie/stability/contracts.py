from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Status = Literal["pass", "warn", "blocked"]


@dataclass(frozen=True)
class StabilitySignal:
    name: str
    value: float
    weight: float
    target: float
    tolerance: float
    status: Status

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "weight": self.weight,
            "target": self.target,
            "tolerance": self.tolerance,
            "status": self.status,
        }


@dataclass(frozen=True)
class StabilityReport:
    status: Status
    score: float
    signals: list[StabilitySignal] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "score": round(self.score, 6),
            "signals": [s.to_dict() for s in self.signals],
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class CalibrationReport:
    status: Status
    weights_before: dict[str, float]
    weights_after: dict[str, float]
    max_shift: float
    total_shift: float
    normalized_sum: float
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "weights_before": dict(self.weights_before),
            "weights_after": dict(self.weights_after),
            "max_shift": round(self.max_shift, 6),
            "total_shift": round(self.total_shift, 6),
            "normalized_sum": round(self.normalized_sum, 6),
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class TIdealReport:
    status: Status
    coefficients_before: dict[str, float]
    coefficients_after: dict[str, float]
    max_shift: float
    loss_before: float
    loss_after: float
    applied: bool
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "coefficients_before": dict(self.coefficients_before),
            "coefficients_after": dict(self.coefficients_after),
            "max_shift": round(self.max_shift, 6),
            "loss_before": round(self.loss_before, 6),
            "loss_after": round(self.loss_after, 6),
            "applied": self.applied,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class TemporalCIMReport:
    status: Status
    episode_count: int
    mean_volatility: float
    role_continuity: float
    unstable_roles: list[str]
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "episode_count": self.episode_count,
            "mean_volatility": round(self.mean_volatility, 6),
            "role_continuity": round(self.role_continuity, 6),
            "unstable_roles": list(self.unstable_roles),
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class MetaLearnerReport:
    status: Status
    mode: Literal["proposal_only", "apply"]
    proposal_count: int
    applied_count: int
    provider_calls: int
    runtime_training_performed: bool
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "mode": self.mode,
            "proposal_count": self.proposal_count,
            "applied_count": self.applied_count,
            "provider_calls": self.provider_calls,
            "runtime_training_performed": self.runtime_training_performed,
            "issues": list(self.issues),
        }
