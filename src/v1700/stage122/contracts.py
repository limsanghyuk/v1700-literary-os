from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Stage122Contract:
    stage: str = "122"
    baseline_stage: str = "121"
    title: str = "NIE v2.0 Stability Absorption"
    absorbed_concepts: tuple[str, ...] = (
        "NILStabilityModule",
        "AgentCalibrator",
        "TIdealLearner",
        "TemporalCIMAdapter",
        "MetaLearnerSkeleton",
    )
    blocked_concepts: tuple[str, ...] = (
        "Gate28 authority",
        "Gate29 authority",
        "runtime model training",
        "AMW alpha range relaxation",
        "direct V545/V555 merge",
    )
    required_outputs: tuple[str, ...] = (
        "manifests/stage122_manifest.json",
        "manifests/stage122_stability_absorption_manifest.json",
        "docs/stages/stage122.md",
        "release/current/stage122_nie_v2_stability_absorption_report.json",
        "release/current/stage122_release_gate_report.json",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "absorbed_concepts": list(self.absorbed_concepts),
            "blocked_concepts": list(self.blocked_concepts),
            "required_outputs": list(self.required_outputs),
        }
