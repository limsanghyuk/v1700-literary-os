from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvaluationPacketRecord:
    evaluation_packet_id: str
    project_id: str
    subject_id: str
    rubric_id: str
    source_stage: str
    source_artifact_ref: str
    required_stage_refs: tuple[str, ...]
    source_trace_refs: tuple[str, ...]
    evaluation_mode: str
    visibility: str
    packet_summary: str
    node2_projection_summary: str
    checksum: str
    write_policy: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_packet_id": self.evaluation_packet_id,
            "project_id": self.project_id,
            "subject_id": self.subject_id,
            "rubric_id": self.rubric_id,
            "source_stage": self.source_stage,
            "source_artifact_ref": self.source_artifact_ref,
            "required_stage_refs": list(self.required_stage_refs),
            "source_trace_refs": list(self.source_trace_refs),
            "evaluation_mode": self.evaluation_mode,
            "visibility": self.visibility,
            "packet_summary": self.packet_summary,
            "node2_projection_summary": self.node2_projection_summary,
            "checksum": self.checksum,
            "write_policy": self.write_policy,
        }


@dataclass(frozen=True)
class EvaluationPacketStorePolicy:
    name: str
    read_only: bool
    runtime_write_allowed: bool
    cross_project_write_allowed: bool
    provider_evaluation_allowed: bool
    mutation_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "read_only": self.read_only,
            "runtime_write_allowed": self.runtime_write_allowed,
            "cross_project_write_allowed": self.cross_project_write_allowed,
            "provider_evaluation_allowed": self.provider_evaluation_allowed,
            "mutation_allowed": self.mutation_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class EvaluationPacketProjectionRule:
    name: str
    subject_id: str
    node2_surface_allowed: bool
    hidden_reveal_blocked: bool
    provider_handle_blocked: bool
    mutation_handle_blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "subject_id": self.subject_id,
            "node2_surface_allowed": self.node2_surface_allowed,
            "hidden_reveal_blocked": self.hidden_reveal_blocked,
            "provider_handle_blocked": self.provider_handle_blocked,
            "mutation_handle_blocked": self.mutation_handle_blocked,
            "evidence": self.evidence,
        }

