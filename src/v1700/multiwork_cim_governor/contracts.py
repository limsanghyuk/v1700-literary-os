from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

AccessType = Literal["read", "reference", "adapt", "write"]
CanonStatus = Literal["PASS", "WARN", "BLOCK"]


@dataclass(frozen=True)
class ProjectCIMSnapshot:
    project_id: str
    canon_root_id: str
    local_character_count: int
    local_world_rule_count: int
    local_relation_count: int
    cross_project_influence_write: int = 0
    raw_manuscript_exported: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CrossProjectInfluenceEdge:
    edge_id: str
    source_project_id: str
    target_project_id: str
    entity_id: str
    access_type: AccessType
    license_edge_exists: bool
    approved_by_author: bool
    resource_scope_permits: bool
    read_only: bool = True

    def access_allowed(self) -> bool:
        return (
            self.license_edge_exists
            and self.approved_by_author
            and self.resource_scope_permits
            and self.read_only
            and self.access_type in {"read", "reference"}
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["access_allowed"] = self.access_allowed()
        return data


@dataclass(frozen=True)
class CanonConflict:
    conflict_id: str
    source_project_id: str
    target_project_id: str
    entity_id: str
    timeline_conflict: float
    world_rule_conflict: float
    character_identity_conflict: float
    relationship_conflict: float
    evidence: tuple[str, ...]
    recommended_action: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CanonGovernorDecision:
    conflict_id: str
    score: float
    status: CanonStatus
    action: Literal["allow", "warn", "block"]
    auto_resolution_allowed: bool
    human_review_required: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Stage129EvidenceContract:
    stage: str
    baseline_stage: str
    project_local_cim_count: int
    cross_project_read_only_edges: int
    cross_project_write_edges: int
    unauthorized_cross_reads: int
    unauthorized_cross_writes: int
    canon_conflict_blocks: int
    canon_auto_resolution_count: int
    raw_manuscript_provider_leakage: int
    node2_raw_reveal_access: int
    provider_default_calls: int
    branchpoint_lineage_preserved: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
