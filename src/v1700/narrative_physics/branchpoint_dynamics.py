from __future__ import annotations

from dataclasses import dataclass
from typing import Any


REQUIRED_BRANCHPOINTS = (
    "stage25_guardrails",
    "stage72_graphnexus",
    "stage83_commercial_release_candidate",
    "stage85_traceability",
    "stage86_arc_reveal_knowledge",
    "stage94_provider_evaluation",
)


@dataclass(frozen=True)
class BranchpointSurvivalReport:
    required_branchpoints: tuple[str, ...]
    preserved_branchpoints: tuple[str, ...]
    missing_branchpoints: tuple[str, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "required_branchpoints": list(self.required_branchpoints),
            "preserved_branchpoints": list(self.preserved_branchpoints),
            "missing_branchpoints": list(self.missing_branchpoints),
            "status": self.status,
        }


class BranchpointSurvivalDynamics:
    def evaluate(self, evidence: dict[str, Any]) -> BranchpointSurvivalReport:
        preserved = set(evidence.get("preserved_branchpoints", REQUIRED_BRANCHPOINTS))
        missing = tuple(item for item in REQUIRED_BRANCHPOINTS if item not in preserved)
        return BranchpointSurvivalReport(
            required_branchpoints=REQUIRED_BRANCHPOINTS,
            preserved_branchpoints=tuple(item for item in REQUIRED_BRANCHPOINTS if item in preserved),
            missing_branchpoints=missing,
            status="pass" if not missing else "blocked",
        )
