from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

AuditDecision = Literal["OBSERVE", "RECOMMEND_REVIEW", "RECOMMEND_WEIGHT_CANDIDATE"]
AuditStatus = Literal["pass", "blocked"]


@dataclass(frozen=True)
class MetaLearnerAuditCase:
    case_id: str
    source_classification: str
    tensor_status: str
    lowest_dimension: str
    lowest_score: float
    recommendation: AuditDecision
    rationale: str
    writer_review_required: bool
    training_allowed: bool = False
    mutation_allowed: bool = False
    active_learning_allowed: bool = False
    provider_call_required: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class MetaLearnerAuditReport:
    stage: str
    baseline_stage: str
    status: AuditStatus
    mode: str
    cases: tuple[MetaLearnerAuditCase, ...]
    audit_only: bool = True
    issues: tuple[str, ...] = ()
    aggregate: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["cases"] = [case.to_dict() for case in self.cases]
        return payload
