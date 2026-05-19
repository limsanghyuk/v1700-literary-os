from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

CandidateDecision = Literal["ACCEPT_CANDIDATE", "REJECT_CANDIDATE", "REVIEW_ONLY"]
LearningQualityStatus = Literal["pass", "blocked"]


@dataclass(frozen=True)
class LearningCandidate:
    case_id: str
    source_stage: str
    source_recommendation: str
    decision: CandidateDecision
    reason: str
    gate_verified: bool
    writer_review_required: bool
    learning_allowed: bool = False
    training_triggered: bool = False
    mutation_allowed: bool = False
    provider_call_required: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CandidateRegistry:
    stage: str
    baseline_stage: str
    status: LearningQualityStatus
    candidates: tuple[LearningCandidate, ...]
    issues: tuple[str, ...] = ()
    counters: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["candidates"] = [candidate.to_dict() for candidate in self.candidates]
        return payload
