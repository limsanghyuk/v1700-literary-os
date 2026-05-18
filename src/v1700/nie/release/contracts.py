from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Decision = Literal["pass", "warn", "blocked"]


@dataclass(frozen=True)
class ReleaseLayer:
    stage: str
    title: str
    report_path: str
    status: str
    authority_mode: str = "advisory"
    absorbed_capabilities: tuple[str, ...] = ()
    blocked_concepts: tuple[str, ...] = ()
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "title": self.title,
            "report_path": self.report_path,
            "status": self.status,
            "authority_mode": self.authority_mode,
            "absorbed_capabilities": list(self.absorbed_capabilities),
            "blocked_concepts": list(self.blocked_concepts),
            "metrics": self.metrics,
        }


@dataclass(frozen=True)
class CrossLineageReleaseDecision:
    status: Decision
    title: str
    baseline_stage: str
    release_stage: str
    release_authority: str
    lineage_layers: tuple[ReleaseLayer, ...]
    blocked_by: tuple[str, ...]
    warnings: tuple[str, ...]
    checks: dict[str, bool]
    invariants: dict[str, Any]
    final_release_pack: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "title": self.title,
            "baseline_stage": self.baseline_stage,
            "release_stage": self.release_stage,
            "release_authority": self.release_authority,
            "lineage_layers": [layer.to_dict() for layer in self.lineage_layers],
            "blocked_by": list(self.blocked_by),
            "warnings": list(self.warnings),
            "checks": self.checks,
            "invariants": self.invariants,
            "final_release_pack": self.final_release_pack,
        }
