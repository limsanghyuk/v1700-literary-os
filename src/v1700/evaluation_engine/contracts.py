from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvaluationMetricValue:
    metric_id: str
    normalized_value: float
    weight: float
    weighted_value: float
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "normalized_value": self.normalized_value,
            "weight": self.weight,
            "weighted_value": self.weighted_value,
            "source": self.source,
        }


@dataclass(frozen=True)
class ContinuityFinding:
    finding_id: str
    axis: str
    severity: str
    hard_violation: bool
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "axis": self.axis,
            "severity": self.severity,
            "hard_violation": self.hard_violation,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class BoundaryFinding:
    finding_id: str
    blocked_payload: str
    violation_count: int
    overridable: bool
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "blocked_payload": self.blocked_payload,
            "violation_count": self.violation_count,
            "overridable": self.overridable,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class EvaluationScorecard:
    evaluation_packet_id: str
    quality_score: float
    continuity_violation_index: float
    regression_delta_index: float
    boundary_violation_count: int
    deterministic_checksum: str
    status: str
    block_reasons: tuple[str, ...]
    metrics: tuple[EvaluationMetricValue, ...]
    continuity_findings: tuple[ContinuityFinding, ...]
    boundary_findings: tuple[BoundaryFinding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_packet_id": self.evaluation_packet_id,
            "quality_score": self.quality_score,
            "continuity_violation_index": self.continuity_violation_index,
            "regression_delta_index": self.regression_delta_index,
            "boundary_violation_count": self.boundary_violation_count,
            "deterministic_checksum": self.deterministic_checksum,
            "status": self.status,
            "block_reasons": list(self.block_reasons),
            "metrics": [metric.to_dict() for metric in self.metrics],
            "continuity_findings": [finding.to_dict() for finding in self.continuity_findings],
            "boundary_findings": [finding.to_dict() for finding in self.boundary_findings],
        }
