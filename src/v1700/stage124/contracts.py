from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Stage124Contract:
    stage: str = "124"
    baseline_stage: str = "123"
    title: str = "PNE / Gate29 Absorption"
    absorbed_concepts: tuple[str, ...] = (
        "PNECore",
        "DebtPredictor",
        "PreemptiveGate",
        "FeedbackLearner",
        "Gate29 secondary predictive gate",
    )
    blocked_concepts: tuple[str, ...] = (
        "direct V555 package merge",
        "Gate29 primary release authority",
        "release-gate runtime model training",
        "mandatory sklearn dependency",
        "graph mutation during prediction",
    )
    invariants: dict[str, Any] = field(default_factory=lambda: {
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "pne_runtime_training_enabled": False,
        "sklearn_required": False,
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
