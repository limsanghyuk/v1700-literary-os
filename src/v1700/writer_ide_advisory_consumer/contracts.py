from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WriterSessionRecord:
    writer_session_id: str
    work_id: str
    session_scope: str
    active_scene_refs: tuple[str, ...]
    active_character_refs: tuple[str, ...]
    active_corpus_refs: tuple[str, ...]
    active_formula_signal_refs: tuple[str, ...]
    active_agent_refs: tuple[str, ...]
    llm_boundary_level: str
    started_at: str
    ended_at: str
    session_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "writer_session_id": self.writer_session_id,
            "work_id": self.work_id,
            "session_scope": self.session_scope,
            "active_scene_refs": list(self.active_scene_refs),
            "active_character_refs": list(self.active_character_refs),
            "active_corpus_refs": list(self.active_corpus_refs),
            "active_formula_signal_refs": list(self.active_formula_signal_refs),
            "active_agent_refs": list(self.active_agent_refs),
            "llm_boundary_level": self.llm_boundary_level,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "session_status": self.session_status,
        }


@dataclass(frozen=True)
class WriterIdeSurfaceCard:
    card_id: str
    panel_ref: str
    zone: str
    work_id: str
    headline: str
    summary: str
    severity: str
    formula_group_badges: tuple[str, ...]
    signal_refs: tuple[str, ...]
    confidence: float
    advisory_only: bool
    canonical_mutation_allowed: bool
    review_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_id": self.card_id,
            "panel_ref": self.panel_ref,
            "zone": self.zone,
            "work_id": self.work_id,
            "headline": self.headline,
            "summary": self.summary,
            "severity": self.severity,
            "formula_group_badges": list(self.formula_group_badges),
            "signal_refs": list(self.signal_refs),
            "confidence": round(self.confidence, 6),
            "advisory_only": self.advisory_only,
            "canonical_mutation_allowed": self.canonical_mutation_allowed,
            "review_status": self.review_status,
        }


@dataclass(frozen=True)
class LearnableCriticExplanationRecord:
    explanation_record_id: str
    writer_session_id: str
    critic_id: str
    advisory_output_id: str
    formula_signal_ref: str
    coefficient_diff_id: str
    alignment_result_id: str
    confidence: float
    explanation_summary: str
    suggested_action: str
    approval_status: str
    canonical_mutation_allowed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "explanation_record_id": self.explanation_record_id,
            "writer_session_id": self.writer_session_id,
            "critic_id": self.critic_id,
            "advisory_output_id": self.advisory_output_id,
            "formula_signal_ref": self.formula_signal_ref,
            "coefficient_diff_id": self.coefficient_diff_id,
            "alignment_result_id": self.alignment_result_id,
            "confidence": round(self.confidence, 6),
            "explanation_summary": self.explanation_summary,
            "suggested_action": self.suggested_action,
            "approval_status": self.approval_status,
            "canonical_mutation_allowed": self.canonical_mutation_allowed,
        }


@dataclass(frozen=True)
class ApprovalBoundaryWarning:
    warning_id: str
    writer_session_id: str
    subject_record_id: str
    subject_record_type: str
    warning_type: str
    message: str
    required_contract_ref: str
    approval_status: str
    canonical_mutation_allowed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "warning_id": self.warning_id,
            "writer_session_id": self.writer_session_id,
            "subject_record_id": self.subject_record_id,
            "subject_record_type": self.subject_record_type,
            "warning_type": self.warning_type,
            "message": self.message,
            "required_contract_ref": self.required_contract_ref,
            "approval_status": self.approval_status,
            "canonical_mutation_allowed": self.canonical_mutation_allowed,
        }


@dataclass(frozen=True)
class WriterIdeAdvisoryBoard:
    board_id: str
    writer_session_id: str
    work_id: str
    advisory_only: bool
    canonical_mutation_allowed: bool
    panel_refs: tuple[str, ...]
    promotion_blockers: tuple[str, ...]
    cards: tuple[WriterIdeSurfaceCard, ...]
    warnings: tuple[ApprovalBoundaryWarning, ...]

    @property
    def card_count(self) -> int:
        return len(self.cards)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "board_id": self.board_id,
            "writer_session_id": self.writer_session_id,
            "work_id": self.work_id,
            "advisory_only": self.advisory_only,
            "canonical_mutation_allowed": self.canonical_mutation_allowed,
            "panel_refs": list(self.panel_refs),
            "promotion_blockers": list(self.promotion_blockers),
            "card_count": self.card_count,
            "warning_count": self.warning_count,
            "cards": [card.to_dict() for card in self.cards],
            "warnings": [warning.to_dict() for warning in self.warnings],
        }
