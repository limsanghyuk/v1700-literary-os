from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class LearnableCriticConfig:
    critic_id: str
    critic_name: str
    critic_axis: str
    allowed_input_types: tuple[str, ...]
    allowed_output_types: tuple[str, ...]
    coefficient_schema_ref: str
    source_policy_ref: str
    approval_policy_ref: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CriticInputSourceRecord:
    input_source_id: str
    critic_id: str
    source_record_id: str
    source_record_type: str
    source_class: str
    rights_status: str
    formula_signal_ref: str
    corpus_signal_ref: str
    value_proof_ref: str
    provenance_ref: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class CoefficientStateRecord:
    coefficient_state_id: str
    critic_id: str
    formula_id: str
    coefficient_name: str
    coefficient_value: float
    coefficient_version: str
    created_at: str
    source_basis: str
    review_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CoefficientDiffRecord:
    coefficient_diff_id: str
    before_state_id: str
    after_state_id: str
    changed_fields: tuple[str, ...]
    old_values: dict[str, float]
    new_values: dict[str, float]
    change_reason: str
    source_signal_refs: tuple[str, ...]
    calibration_run_ref: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DeterministicSeedRecord:
    seed_id: str
    seed_value: int
    run_id: str
    randomization_scope: str
    reproducibility_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationRunRecord:
    calibration_run_id: str
    critic_id: str
    input_source_refs: tuple[str, ...]
    formula_signal_refs: tuple[str, ...]
    value_proof_refs: tuple[str, ...]
    learning_rate: float
    iteration_count: int
    loss_or_error_metric: str
    seed_ref: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AlignmentResultRecord:
    alignment_result_id: str
    calibration_run_id: str
    before_alignment: float
    after_alignment: float
    improvement_delta: float
    failure_notes: tuple[str, ...]
    overfit_warning: bool
    human_review_required: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RollbackRecord:
    rollback_id: str
    coefficient_diff_id: str
    rollback_target_state_id: str
    rollback_reason: str
    rollback_status: str
    performed_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HumanApprovalRecord:
    approval_id: str
    coefficient_diff_id: str
    reviewer_role: str
    approval_status: str
    approval_note: str
    approved_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AdvisoryOutputRecord:
    advisory_output_id: str
    critic_id: str
    input_source_refs: tuple[str, ...]
    output_type: str
    score_or_label: str
    explanation: str
    confidence: float
    suggested_action: str
    canonical_mutation_allowed: bool
    review_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
