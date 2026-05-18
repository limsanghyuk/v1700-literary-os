from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage118Contract:
    stage: str = "118"
    baseline_stage: str = "117"
    title: str = "NIL Orchestrator"
    components_required: tuple[str, ...] = (
        "reward_bridge",
        "adaptive_momentum_weights",
        "character_influence_matrix",
        "domain_rag_fusion",
        "narrative_tension_curve",
    )
    release_gate_live_provider_calls_allowed: bool = False
    physics_reward_bridge_llm_call_allowed: bool = False
    next_development_order: tuple[str, ...] = ("Stage119", "Stage120")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "components_required": list(self.components_required),
            "release_gate_live_provider_calls_allowed": self.release_gate_live_provider_calls_allowed,
            "physics_reward_bridge_llm_call_allowed": self.physics_reward_bridge_llm_call_allowed,
            "next_development_order": list(self.next_development_order),
        }
