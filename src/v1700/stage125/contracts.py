from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Stage125Contract:
    stage: str = "125"
    baseline_stage: str = "124"
    title: str = "Gate25/28/29 Governor"
    absorbed_concepts: tuple[str, ...] = (
        "Gate25 primary release authority preservation",
        "Gate28 secondary quality gate arbitration",
        "Gate29 secondary predictive gate arbitration",
        "single deterministic release governor decision",
    )
    blocked_concepts: tuple[str, ...] = (
        "Gate28 primary authority",
        "Gate29 primary authority",
        "release-gate runtime training",
        "auto-repair mutation during release",
        "live provider calls in governor",
        "direct V545/V555 package merge",
    )
    invariants: dict[str, Any] = field(default_factory=lambda: {
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "gate28_primary_authority_enabled": False,
        "gate29_primary_authority_enabled": False,
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
