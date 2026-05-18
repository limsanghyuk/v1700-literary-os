from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


ScoreName = Literal["reader", "writer", "editor", "cultural"]


def clamp01(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 6)


def _validate_score(name: str, value: float) -> float:
    score = float(value)
    if not 0.0 <= score <= 1.0:
        raise ValueError(f"{name} must be in [0, 1], got {value!r}")
    return score


@dataclass(frozen=True)
class MAEDimensionScores:
    tension: float
    sympathy: float
    dread: float
    catharsis: float

    def __post_init__(self) -> None:
        for key, value in self.to_dict().items():
            _validate_score(key, value)

    def to_dict(self) -> dict[str, float]:
        return {
            "tension": float(self.tension),
            "sympathy": float(self.sympathy),
            "dread": float(self.dread),
            "catharsis": float(self.catharsis),
        }


@dataclass(frozen=True)
class MAEResult:
    """Deterministic MAE output contract.

    Stage113 deliberately consumes cached or fixture MAE results. Live LLM/provider
    calls remain isolated outside release gates. The result is already normalized
    to [0, 1] scores and includes rubric evidence for auditability.
    """

    scene_id: str
    reader_score: float
    writer_score: float
    editor_score: float
    cultural_score: float
    dimension_scores: MAEDimensionScores
    rubric_evidence: dict[str, tuple[str, ...]] = field(default_factory=dict)
    live_provider_call_count: int = 0
    source: Literal["fixture", "cached", "offline_evaluation"] = "fixture"

    def __post_init__(self) -> None:
        for key in ("reader_score", "writer_score", "editor_score", "cultural_score"):
            _validate_score(key, getattr(self, key))
        if self.live_provider_call_count != 0:
            raise ValueError("release-safe MAEResult must not include live provider calls")

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "reader_score": self.reader_score,
            "writer_score": self.writer_score,
            "editor_score": self.editor_score,
            "cultural_score": self.cultural_score,
            "dimension_scores": self.dimension_scores.to_dict(),
            "rubric_evidence": {k: list(v) for k, v in self.rubric_evidence.items()},
            "live_provider_call_count": self.live_provider_call_count,
            "source": self.source,
        }


@dataclass(frozen=True)
class PhysicsRewardSignal:
    scene_id: str
    reward: float
    baseline_before: float
    baseline_after: float
    advantage: float
    weights: dict[str, float]
    provider_call_count: int
    physics_reward_bridge_llm_call_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "reward": self.reward,
            "baseline_before": self.baseline_before,
            "baseline_after": self.baseline_after,
            "advantage": self.advantage,
            "weights": self.weights,
            "provider_call_count": self.provider_call_count,
            "physics_reward_bridge_llm_call_count": self.physics_reward_bridge_llm_call_count,
        }


@dataclass(frozen=True)
class CoefficientUpdateProposal:
    coefficient: str
    feature_value: float
    baseline_value: float
    proposed_value: float
    delta: float
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "coefficient": self.coefficient,
            "feature_value": self.feature_value,
            "baseline_value": self.baseline_value,
            "proposed_value": self.proposed_value,
            "delta": self.delta,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class PhysicsRewardBridgeReport:
    stage: str
    status: str
    mae_result: MAEResult
    reward_signal: PhysicsRewardSignal
    coefficient_update_proposals: tuple[CoefficientUpdateProposal, ...]
    drift_guard: dict[str, Any]
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "mae_result": self.mae_result.to_dict(),
            "reward_signal": self.reward_signal.to_dict(),
            "coefficient_update_proposals": [p.to_dict() for p in self.coefficient_update_proposals],
            "drift_guard": self.drift_guard,
            "issues": list(self.issues),
        }
