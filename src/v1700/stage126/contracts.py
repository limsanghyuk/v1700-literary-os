from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Stage126Contract:
    stage: str = "126"
    baseline_stage: str = "125"
    title: str = "Cross-Lineage Intelligence Release"
    absorbed_concepts: tuple[str, ...] = (
        "Stage120 Gate25 NIE v1.0 release authority",
        "Stage122 NIE v2.0 stability absorption",
        "Stage123 ASD/Gate28 secondary quality gate",
        "Stage124 PNE/Gate29 secondary predictive gate",
        "Stage125 deterministic Gate25/28/29 Governor",
    )
    blocked_concepts: tuple[str, ...] = (
        "direct V545/V555 package merge",
        "Gate28 primary authority",
        "Gate29 primary authority",
        "release-gate runtime model training",
        "auto-repair graph mutation during release",
        "live provider calls in release governor",
    )
    invariants: dict[str, Any] = field(default_factory=lambda: {
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "release_gate_runtime_training_enabled": False,
        "auto_repair_mutation_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
    })

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "absorbed_concepts": list(self.absorbed_concepts),
            "blocked_concepts": list(self.blocked_concepts),
            "invariants": self.invariants,
        }
