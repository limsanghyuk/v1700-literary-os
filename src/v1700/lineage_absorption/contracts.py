from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

AbsorptionStatus = Literal["KEEP", "ADAPT", "DEFER", "REJECT"]
RelationshipType = Literal["ancestor", "sibling", "successor_candidate", "foreign_branch"]
ReleaseMode = Literal["PRIMARY", "SECONDARY", "ADVISORY", "BLOCKED"]


@dataclass(frozen=True)
class CandidateArchiveAudit:
    name: str
    source_version: str
    sha256: str
    entry_count: int
    cache_file_count: int
    backslash_path_count: int
    has_internal_filelist: bool
    has_internal_sha256sums: bool
    clean_packaging_pass: bool
    direct_merge_allowed: bool
    observed_modules: list[str] = field(default_factory=list)
    observed_reports: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "source_version": self.source_version,
            "sha256": self.sha256,
            "entry_count": self.entry_count,
            "cache_file_count": self.cache_file_count,
            "backslash_path_count": self.backslash_path_count,
            "has_internal_filelist": self.has_internal_filelist,
            "has_internal_sha256sums": self.has_internal_sha256sums,
            "clean_packaging_pass": self.clean_packaging_pass,
            "direct_merge_allowed": self.direct_merge_allowed,
            "observed_modules": list(self.observed_modules),
            "observed_reports": list(self.observed_reports),
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class FormulaEntry:
    formula_id: str
    source_lineage: str
    source_version: str
    module_path: str
    formula_type: str
    expression: str
    constants: dict[str, float | int | str]
    conflicts_with: list[str]
    absorption_status: AbsorptionStatus
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "formula_id": self.formula_id,
            "source_lineage": self.source_lineage,
            "source_version": self.source_version,
            "module_path": self.module_path,
            "formula_type": self.formula_type,
            "expression": self.expression,
            "constants": dict(self.constants),
            "conflicts_with": list(self.conflicts_with),
            "absorption_status": self.absorption_status,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class LineageRelationship:
    trunk_stage: str
    candidate_version: str
    relationship_type: RelationshipType
    clean_packaging_pass: bool
    has_internal_filelist: bool
    has_internal_sha256sums: bool
    cache_file_count: int
    direct_merge_allowed: bool
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "trunk_stage": self.trunk_stage,
            "candidate_version": self.candidate_version,
            "relationship_type": self.relationship_type,
            "clean_packaging_pass": self.clean_packaging_pass,
            "has_internal_filelist": self.has_internal_filelist,
            "has_internal_sha256sums": self.has_internal_sha256sums,
            "cache_file_count": self.cache_file_count,
            "direct_merge_allowed": self.direct_merge_allowed,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class ConflictEntry:
    conflict_id: str
    subject: str
    trunk_value: str
    candidate_value: str
    severity: Literal["low", "medium", "high", "blocker"]
    decision: str
    required_resolution_stage: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "subject": self.subject,
            "trunk_value": self.trunk_value,
            "candidate_value": self.candidate_value,
            "severity": self.severity,
            "decision": self.decision,
            "required_resolution_stage": self.required_resolution_stage,
        }


@dataclass(frozen=True)
class AbsorptionCandidate:
    candidate_id: str
    source_version: str
    module_family: str
    priority: int
    target_stage: str
    absorption_status: AbsorptionStatus
    required_adapters: list[str]
    required_tests: list[str]
    blocked_by: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "source_version": self.source_version,
            "module_family": self.module_family,
            "priority": self.priority,
            "target_stage": self.target_stage,
            "absorption_status": self.absorption_status,
            "required_adapters": list(self.required_adapters),
            "required_tests": list(self.required_tests),
            "blocked_by": list(self.blocked_by),
        }


@dataclass(frozen=True)
class GateAuthorityEntry:
    gate_id: str
    source_lineage: str
    authority_scope: str
    release_mode: ReleaseMode
    depends_on: list[str]
    conflict_notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "source_lineage": self.source_lineage,
            "authority_scope": self.authority_scope,
            "release_mode": self.release_mode,
            "depends_on": list(self.depends_on),
            "conflict_notes": list(self.conflict_notes),
        }


@dataclass(frozen=True)
class AbsorptionPlan:
    stage: str
    title: str
    candidates: list[str]
    required_adapters: list[str]
    blocked_items: list[str]
    required_tests: list[str]
    required_manifests: list[str]
    required_release_evidence: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "title": self.title,
            "candidates": list(self.candidates),
            "required_adapters": list(self.required_adapters),
            "blocked_items": list(self.blocked_items),
            "required_tests": list(self.required_tests),
            "required_manifests": list(self.required_manifests),
            "required_release_evidence": list(self.required_release_evidence),
        }
