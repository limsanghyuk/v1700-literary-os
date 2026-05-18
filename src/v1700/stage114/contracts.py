from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage114Contract:
    stage: str = "114"
    baseline_stage: str = "113"
    title: str = "AdaptiveMomentumWeights"
    alpha_min: float = 0.30
    alpha_max: float = 0.80
    max_single_alpha_shift: float = 0.03
    max_run_total_alpha_shift: float = 0.10
    mae_live_calls_allowed_in_release_gate: bool = False
    physics_reward_bridge_llm_calls_allowed: bool = False
    protected_policy: dict[str, Any] | None = None
    next_development_order: tuple[str, ...] = ("Stage115", "Stage116", "Stage117", "Stage118", "Stage119", "Stage120")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "alpha_min": self.alpha_min,
            "alpha_max": self.alpha_max,
            "max_single_alpha_shift": self.max_single_alpha_shift,
            "max_run_total_alpha_shift": self.max_run_total_alpha_shift,
            "mae_live_calls_allowed_in_release_gate": self.mae_live_calls_allowed_in_release_gate,
            "physics_reward_bridge_llm_calls_allowed": self.physics_reward_bridge_llm_calls_allowed,
            "protected_policy": self.protected_policy or {
                "surface_safety_tolerance_can_loosen": False,
                "branchpoint_sensitivity_can_decrease": False,
                "provider_zero_policy_can_change": False,
                "node2_raw_reveal_tolerance": 0,
            },
            "next_development_order": list(self.next_development_order),
        }
