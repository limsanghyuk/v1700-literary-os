from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

MomentumDimension = Literal["tension", "sympathy", "dread", "catharsis"]
GenreName = Literal["melodrama", "thriller", "family", "generic"]

DIMENSIONS: tuple[MomentumDimension, ...] = ("tension", "sympathy", "dread", "catharsis")


def clamp(value: float, low: float, high: float) -> float:
    return round(max(low, min(high, float(value))), 6)


def validate_unit_interval(name: str, value: float) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{name} must be in [0, 1], got {value!r}")
    return number


@dataclass(frozen=True)
class AMWInput:
    dim: MomentumDimension
    process_signal: float
    observation_signal: float
    mae_dim_score: float
    genre: GenreName = "generic"
    act_pos: float = 0.5

    def __post_init__(self) -> None:
        validate_unit_interval("process_signal", self.process_signal)
        validate_unit_interval("observation_signal", self.observation_signal)
        validate_unit_interval("mae_dim_score", self.mae_dim_score)
        validate_unit_interval("act_pos", self.act_pos)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dim": self.dim,
            "process_signal": self.process_signal,
            "observation_signal": self.observation_signal,
            "mae_dim_score": self.mae_dim_score,
            "genre": self.genre,
            "act_pos": self.act_pos,
        }


@dataclass(frozen=True)
class AMWUpdate:
    dim: MomentumDimension
    alpha_before: float
    process_signal: float
    observation_signal: float
    mae_dim_score: float
    delta_dim: float
    loss: float
    gradient: float
    raw_alpha_after: float
    alpha_after: float
    shift: float
    clamped: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "dim": self.dim,
            "alpha_before": self.alpha_before,
            "process_signal": self.process_signal,
            "observation_signal": self.observation_signal,
            "mae_dim_score": self.mae_dim_score,
            "delta_dim": self.delta_dim,
            "loss": self.loss,
            "gradient": self.gradient,
            "raw_alpha_after": self.raw_alpha_after,
            "alpha_after": self.alpha_after,
            "shift": self.shift,
            "clamped": self.clamped,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class AMWDriftGuard:
    status: Literal["pass", "blocked"]
    alpha_min: float
    alpha_max: float
    max_single_shift: float
    max_run_total_shift: float
    observed_max_single_shift: float
    observed_run_total_shift: float
    protected_policy: dict[str, Any]
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "alpha_min": self.alpha_min,
            "alpha_max": self.alpha_max,
            "max_single_shift": self.max_single_shift,
            "max_run_total_shift": self.max_run_total_shift,
            "observed_max_single_shift": self.observed_max_single_shift,
            "observed_run_total_shift": self.observed_run_total_shift,
            "protected_policy": self.protected_policy,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class AMWReport:
    stage: str
    status: Literal["pass", "blocked"]
    genre: GenreName
    scene_id: str
    alpha_before: dict[str, float]
    alpha_after: dict[str, float]
    updates: tuple[AMWUpdate, ...]
    drift_guard: AMWDriftGuard
    provider_call_count: int
    physics_reward_bridge_llm_call_count: int
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "genre": self.genre,
            "scene_id": self.scene_id,
            "alpha_before": self.alpha_before,
            "alpha_after": self.alpha_after,
            "updates": [u.to_dict() for u in self.updates],
            "drift_guard": self.drift_guard.to_dict(),
            "provider_call_count": self.provider_call_count,
            "physics_reward_bridge_llm_call_count": self.physics_reward_bridge_llm_call_count,
            "issues": list(self.issues),
        }
