from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

NILComponentName = Literal[
    "reward_bridge",
    "adaptive_momentum_weights",
    "character_influence_matrix",
    "domain_rag_fusion",
    "narrative_tension_curve",
]


@dataclass(frozen=True)
class NILComponentStatus:
    name: NILComponentName
    status: Literal["pass", "blocked"]
    stage: str
    issue_count: int = 0
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "stage": self.stage,
            "issue_count": int(self.issue_count),
            "summary": self.summary,
        }


@dataclass(frozen=True)
class NILLoopReport:
    stage: str
    baseline_stage: str
    title: str
    status: Literal["pass", "blocked"]
    components: tuple[NILComponentStatus, ...]
    loop_order: tuple[str, ...]
    convergence: dict[str, Any]
    invariant_counts: dict[str, int]
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "status": self.status,
            "components": [component.to_dict() for component in self.components],
            "loop_order": list(self.loop_order),
            "convergence": self.convergence,
            "invariant_counts": self.invariant_counts,
            "issues": list(self.issues),
        }
