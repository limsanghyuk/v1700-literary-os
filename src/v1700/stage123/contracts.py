from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage123Contract:
    stage: str = "123"
    baseline_stage: str = "122"
    title: str = "ASD / Gate28 Absorption"
    absorbed_concepts: tuple[str, ...] = (
        "NarrativeDebtDetector",
        "ArcConsistencyChecker",
        "StoryDoctorOrchestrator",
        "AutoRepairExecutorDryRun",
        "Gate28SecondaryQualityGate",
    )
    blocked_concepts: tuple[str, ...] = (
        "Gate28 primary authority",
        "graph mutation auto-repair",
        "LLM repair generation",
        "direct V545 package merge",
        "Gate29 predictive authority",
    )
    required_outputs: tuple[str, ...] = (
        "manifests/stage123_manifest.json",
        "manifests/stage123_asd_gate28_manifest.json",
        "docs/stages/stage123.md",
        "release/current/stage123_asd_gate28_absorption_report.json",
        "release/current/stage123_story_doctor_report.json",
        "release/current/stage123_gate28_report.json",
        "release/current/stage123_release_gate_report.json",
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
