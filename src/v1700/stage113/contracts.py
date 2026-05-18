from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage113Contract:
    stage: str = "113"
    baseline_stage: str = "112"
    title: str = "PhysicsRewardBridge + MAE Reward Wiring"
    mae_live_calls_allowed_in_release_gate: bool = False
    physics_reward_bridge_llm_calls_allowed: bool = False
    reward_weights: dict[str, float] | None = None
    next_development_order: tuple[str, ...] = ("Stage114", "Stage115", "Stage116", "Stage117", "Stage118", "Stage119", "Stage120")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "mae_live_calls_allowed_in_release_gate": self.mae_live_calls_allowed_in_release_gate,
            "physics_reward_bridge_llm_calls_allowed": self.physics_reward_bridge_llm_calls_allowed,
            "reward_weights": self.reward_weights or {"reader": 0.35, "writer": 0.25, "editor": 0.25, "cultural": 0.15},
            "next_development_order": list(self.next_development_order),
        }
