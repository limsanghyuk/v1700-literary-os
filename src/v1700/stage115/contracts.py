from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage115Contract:
    stage: str = "115"
    baseline_stage: str = "114"
    title: str = "CharacterInfluenceMatrix + Structural Balance"
    matrix_must_be_asymmetric: bool = True
    triangle_tension_required: bool = True
    centrality_required: bool = True
    role_tier_assignment_required: bool = True
    live_provider_calls_allowed_in_release_gate: bool = False
    physics_reward_bridge_llm_calls_allowed: bool = False
    next_development_order: tuple[str, ...] = ("Stage116", "Stage117", "Stage118", "Stage119", "Stage120")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "matrix_must_be_asymmetric": self.matrix_must_be_asymmetric,
            "triangle_tension_required": self.triangle_tension_required,
            "centrality_required": self.centrality_required,
            "role_tier_assignment_required": self.role_tier_assignment_required,
            "live_provider_calls_allowed_in_release_gate": self.live_provider_calls_allowed_in_release_gate,
            "physics_reward_bridge_llm_calls_allowed": self.physics_reward_bridge_llm_calls_allowed,
            "next_development_order": list(self.next_development_order),
        }
