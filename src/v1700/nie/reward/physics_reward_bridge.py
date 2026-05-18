from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from v1700.narrative_optimization.coefficients import NarrativePhysicsCoefficientSet
from v1700.nie.reward.contracts import (
    CoefficientUpdateProposal,
    MAEResult,
    PhysicsRewardSignal,
)

AGENT_REWARD_WEIGHTS: dict[str, float] = {
    "reader": 0.35,
    "writer": 0.25,
    "editor": 0.25,
    "cultural": 0.15,
}
EMA_BASELINE_KEEP = 0.95
EMA_REWARD_MIX = 0.05
DEFAULT_BASELINE = 0.50
DEFAULT_LR = 0.01
MAX_SINGLE_UPDATE_DELTA = 0.03


@dataclass(frozen=True)
class PhysicsRewardBridge:
    """Convert cached/fixture MAE scores into physics reward signals.

    This class is intentionally provider-blind. It accepts already-normalized MAE
    output and performs only deterministic arithmetic. LLM calls in this bridge
    would violate Stage113 and ADR-006-style isolation rules.
    """

    baseline: float = DEFAULT_BASELINE
    lr: float = DEFAULT_LR

    def calculate_reward_signal(self, mae_result: MAEResult) -> PhysicsRewardSignal:
        reward = round(
            AGENT_REWARD_WEIGHTS["reader"] * mae_result.reader_score
            + AGENT_REWARD_WEIGHTS["writer"] * mae_result.writer_score
            + AGENT_REWARD_WEIGHTS["editor"] * mae_result.editor_score
            + AGENT_REWARD_WEIGHTS["cultural"] * mae_result.cultural_score,
            6,
        )
        baseline_before = round(float(self.baseline), 6)
        advantage = round(reward - baseline_before, 6)
        baseline_after = round(EMA_BASELINE_KEEP * baseline_before + EMA_REWARD_MIX * reward, 6)
        return PhysicsRewardSignal(
            scene_id=mae_result.scene_id,
            reward=reward,
            baseline_before=baseline_before,
            baseline_after=baseline_after,
            advantage=advantage,
            weights=AGENT_REWARD_WEIGHTS.copy(),
            provider_call_count=mae_result.live_provider_call_count,
            physics_reward_bridge_llm_call_count=0,
        )

    def propose_coefficient_updates(
        self,
        signal: PhysicsRewardSignal,
        feature_vector: dict[str, float],
        coefficients: NarrativePhysicsCoefficientSet | None = None,
    ) -> tuple[CoefficientUpdateProposal, ...]:
        coefficients = coefficients or NarrativePhysicsCoefficientSet()
        values = coefficients.to_dict()
        proposals: list[CoefficientUpdateProposal] = []
        for name, feature in sorted(feature_vector.items()):
            if name not in values:
                continue
            feature_value = _clamp01(feature)
            baseline_value = float(values[name])
            direction = 1.0 if signal.advantage >= 0 else -1.0
            raw_delta = direction * self.lr * abs(signal.advantage) * (feature_value - min(1.0, baseline_value))
            delta = _bounded(raw_delta, MAX_SINGLE_UPDATE_DELTA)
            proposed = round(max(0.0, baseline_value + delta), 6)
            proposals.append(
                CoefficientUpdateProposal(
                    coefficient=name,
                    feature_value=feature_value,
                    baseline_value=round(baseline_value, 6),
                    proposed_value=proposed,
                    delta=delta,
                    reason="positive_advantage_moves_toward_feature" if signal.advantage >= 0 else "negative_advantage_moves_away_from_feature",
                )
            )
        return tuple(proposals)

    def drift_guard(self, proposals: tuple[CoefficientUpdateProposal, ...]) -> dict[str, Any]:
        issues = []
        max_delta = max((abs(p.delta) for p in proposals), default=0.0)
        if max_delta > MAX_SINGLE_UPDATE_DELTA:
            issues.append("max_single_update_delta_exceeded")
        return {
            "status": "pass" if not issues else "blocked",
            "max_single_update_delta": round(max_delta, 6),
            "limit": MAX_SINGLE_UPDATE_DELTA,
            "proposal_count": len(proposals),
            "issues": issues,
        }


def _bounded(value: float, limit: float) -> float:
    return round(max(-limit, min(limit, float(value))), 6)


def _clamp01(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 6)
