from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationEvidenceRef:
    ref_id: str
    source_stage: str
    source_path: str
    required: bool
    read_only: bool

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "ref_id": self.ref_id,
            "source_stage": self.source_stage,
            "source_path": self.source_path,
            "required": self.required,
            "read_only": self.read_only,
        }


@dataclass(frozen=True)
class EvaluationArtifactEnvelope:
    artifact_id: str
    project_id: str
    source_stage: str
    source_artifact_ref: str
    artifact_type: str
    visibility: str
    checksum: str
    created_from: str
    provider_calls: int
    write_policy: str

    def to_dict(self) -> dict[str, str | int]:
        return {
            "artifact_id": self.artifact_id,
            "project_id": self.project_id,
            "source_stage": self.source_stage,
            "source_artifact_ref": self.source_artifact_ref,
            "artifact_type": self.artifact_type,
            "visibility": self.visibility,
            "checksum": self.checksum,
            "created_from": self.created_from,
            "provider_calls": self.provider_calls,
            "write_policy": self.write_policy,
        }


@dataclass(frozen=True)
class EvaluationSubject:
    subject_id: str
    subject_type: str
    lineage_anchor: str
    visibility_policy: str
    read_only: bool
    evidence_refs: tuple[EvaluationEvidenceRef, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "subject_id": self.subject_id,
            "subject_type": self.subject_type,
            "lineage_anchor": self.lineage_anchor,
            "visibility_policy": self.visibility_policy,
            "read_only": self.read_only,
            "evidence_refs": [ref.to_dict() for ref in self.evidence_refs],
        }


@dataclass(frozen=True)
class EvaluationMetric:
    metric_id: str
    metric_group: str
    weight: float
    range_min: float
    range_max: float
    deterministic: bool
    boundary_sensitive: bool

    def to_dict(self) -> dict[str, str | float | bool]:
        return {
            "metric_id": self.metric_id,
            "metric_group": self.metric_group,
            "weight": self.weight,
            "range_min": self.range_min,
            "range_max": self.range_max,
            "deterministic": self.deterministic,
            "boundary_sensitive": self.boundary_sensitive,
        }


@dataclass(frozen=True)
class EvaluationThresholdPolicy:
    quality_threshold: float
    regression_delta_threshold: float
    continuity_hard_fail_allowed: int
    boundary_violation_allowed: int
    determinism_required: bool
    boundary_override: str

    def to_dict(self) -> dict[str, float | int | bool | str]:
        return {
            "quality_threshold": self.quality_threshold,
            "regression_delta_threshold": self.regression_delta_threshold,
            "continuity_hard_fail_allowed": self.continuity_hard_fail_allowed,
            "boundary_violation_allowed": self.boundary_violation_allowed,
            "determinism_required": self.determinism_required,
            "boundary_override": self.boundary_override,
        }


@dataclass(frozen=True)
class EvaluationRubric:
    rubric_id: str
    rubric_version: str
    metrics: tuple[EvaluationMetric, ...]
    threshold_policy: EvaluationThresholdPolicy
    provider_evaluation_enabled: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "rubric_id": self.rubric_id,
            "rubric_version": self.rubric_version,
            "metrics": [metric.to_dict() for metric in self.metrics],
            "threshold_policy": self.threshold_policy.to_dict(),
            "provider_evaluation_enabled": self.provider_evaluation_enabled,
        }


@dataclass(frozen=True)
class QualityCriterion:
    criterion_id: str
    metric_id: str
    pass_rule: str

    def to_dict(self) -> dict[str, str]:
        return {
            "criterion_id": self.criterion_id,
            "metric_id": self.metric_id,
            "pass_rule": self.pass_rule,
        }


@dataclass(frozen=True)
class ContinuityCriterion:
    criterion_id: str
    continuity_axis: str
    hard_fail_on_violation: bool

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "criterion_id": self.criterion_id,
            "continuity_axis": self.continuity_axis,
            "hard_fail_on_violation": self.hard_fail_on_violation,
        }


@dataclass(frozen=True)
class RegressionCriterion:
    criterion_id: str
    baseline_source: str
    max_allowed_delta: float

    def to_dict(self) -> dict[str, str | float]:
        return {
            "criterion_id": self.criterion_id,
            "baseline_source": self.baseline_source,
            "max_allowed_delta": self.max_allowed_delta,
        }


@dataclass(frozen=True)
class BoundaryCriterion:
    criterion_id: str
    blocked_payload: str
    overridable: bool

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "criterion_id": self.criterion_id,
            "blocked_payload": self.blocked_payload,
            "overridable": self.overridable,
        }


@dataclass(frozen=True)
class EvaluationVerdict:
    verdict_id: str
    evaluation_packet_id: str
    quality_score: float
    continuity_violation_index: float
    regression_delta_index: float
    boundary_violation_count: int
    deterministic_checksum: str
    status: str
    block_reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "verdict_id": self.verdict_id,
            "evaluation_packet_id": self.evaluation_packet_id,
            "quality_score": self.quality_score,
            "continuity_violation_index": self.continuity_violation_index,
            "regression_delta_index": self.regression_delta_index,
            "boundary_violation_count": self.boundary_violation_count,
            "deterministic_checksum": self.deterministic_checksum,
            "status": self.status,
            "block_reasons": list(self.block_reasons),
        }


@dataclass(frozen=True)
class EvaluationAuthorityPolicy:
    provider_evaluation_enabled: bool
    evaluation_write_enabled: bool
    memory_write_enabled: bool
    canon_mutation_enabled: bool
    runtime_training_enabled: bool
    auto_repair_apply_enabled: bool
    cross_project_write_enabled: bool
    node2_surface_only: bool
    boundary_criteria_non_overridable: bool

    def to_dict(self) -> dict[str, bool]:
        return {
            "provider_evaluation_enabled": self.provider_evaluation_enabled,
            "evaluation_write_enabled": self.evaluation_write_enabled,
            "memory_write_enabled": self.memory_write_enabled,
            "canon_mutation_enabled": self.canon_mutation_enabled,
            "runtime_training_enabled": self.runtime_training_enabled,
            "auto_repair_apply_enabled": self.auto_repair_apply_enabled,
            "cross_project_write_enabled": self.cross_project_write_enabled,
            "node2_surface_only": self.node2_surface_only,
            "boundary_criteria_non_overridable": self.boundary_criteria_non_overridable,
        }

