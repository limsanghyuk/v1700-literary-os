from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal


TensorStatus = Literal["PASS", "WATCH", "REVIEW_REQUIRED"]


@dataclass(frozen=True)
class NarrativeStateTensor:
    case_id: str
    classification: str
    dimensions: dict[str, float]
    status: TensorStatus
    lowest_dimension: str
    lowest_score: float
    writer_review_required: bool
    mutation_allowed: bool = False
    provider_call_required: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class TensorMeasurementReport:
    stage: str
    baseline_stage: str
    status: str
    dimensions: tuple[str, ...]
    tensors: tuple[NarrativeStateTensor, ...]
    average_vector: dict[str, float] = field(default_factory=dict)
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["tensors"] = [item.to_dict() for item in self.tensors]
        return payload
