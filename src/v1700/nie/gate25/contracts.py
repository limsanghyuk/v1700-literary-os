from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Gate25Contract:
    stage: str = "120"
    baseline_stage: str = "119"
    name: str = "Gate25 NIE v1.0"
    required_stage_reports: tuple[str, ...] = (
        "release/current/stage112_release_gate_report.json",
        "release/current/stage113_release_gate_report.json",
        "release/current/stage114_release_gate_report.json",
        "release/current/stage115_release_gate_report.json",
        "release/current/stage116_release_gate_report.json",
        "release/current/stage117_release_gate_report.json",
        "release/current/stage118_release_gate_report.json",
        "release/current/stage119_release_gate_report.json",
    )
    required_components: tuple[str, ...] = (
        "gitnexus_preflight",
        "physics_reward_bridge",
        "adaptive_momentum_weights",
        "character_influence_matrix",
        "domain_specific_rag_fusion",
        "narrative_tension_curve",
        "nil_orchestrator",
        "nie_adversarial_regression",
    )
    required_pack_files: tuple[str, ...] = (
        "gate25_nie_v1_report.json",
        "stage120_nie_v1_summary.md",
        "stage120_component_matrix.json",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "name": self.name,
            "required_stage_reports": list(self.required_stage_reports),
            "required_components": list(self.required_components),
            "required_pack_files": list(self.required_pack_files),
        }
