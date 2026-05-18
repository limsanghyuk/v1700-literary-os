from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage121Contract:
    stage: str = "121"
    baseline_stage: str = "120"
    title: str = "Cross-Lineage Formula Reconciliation & Absorption Preflight"
    required_candidate_versions: tuple[str, ...] = ("V545_HF", "V546_cleanup", "V555_PNE")
    required_outputs: tuple[str, ...] = (
        "manifests/stage121_formula_ledger.json",
        "manifests/stage121_lineage_relationship_map.json",
        "manifests/stage121_conflict_matrix.json",
        "manifests/stage121_absorption_candidate_registry.json",
        "manifests/stage121_gate_authority_map.json",
        "release/current/stage121_cross_lineage_preflight_report.json",
        "release/current/stage121_formula_conflict_report.json",
        "release/current/stage121_packaging_cleanliness_report.json",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "required_candidate_versions": list(self.required_candidate_versions),
            "required_outputs": list(self.required_outputs),
        }
