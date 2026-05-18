from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


@dataclass
class Stage101Preflight:
    stage: str
    baseline_stage: str
    stage100_baseline_status: str
    gitnexus_status: str
    v430_source_status: str
    absorption_mode: str
    v430_untraced_merge: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Stage101AbsorptionCandidate:
    candidate_id: str
    source_status: Literal["AVAILABLE", "MISSING", "PARTIAL"]
    value_area: str
    v1700_overlap: str
    branchpoint_risk: Literal["LOW", "MEDIUM", "HIGH"]
    proposed_action: Literal["ABSORB", "ADAPT", "DEFER", "REJECT"]
    required_branchpoints: list[str]
    required_tests: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

