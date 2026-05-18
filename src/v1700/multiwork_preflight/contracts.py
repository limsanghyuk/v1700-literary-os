from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class ProjectIdentity:
    project_id: str
    title: str
    owner_id: str
    genre: str
    canon_root_id: str
    license_policy_id: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CrossWorkAccessEdge:
    source_project_id: str
    target_project_id: str
    access_type: Literal["read", "reference", "adapt", "write"]
    license_edge_exists: bool
    approved_by_author: bool
    expires_at: str | None = None
    resource_scope_permits: bool = True
    isolation_policy_allows: bool = True

    def allowed(self) -> bool:
        # Stage127 formula: AccessAllowed = license_edge_exists AND isolation_policy_allows
        # AND resource_scope_permits AND author_approval_valid. Write is still disabled.
        if self.access_type == "write":
            return False
        return bool(
            self.license_edge_exists
            and self.isolation_policy_allows
            and self.resource_scope_permits
            and self.approved_by_author
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["access_allowed"] = self.allowed()
        return payload


@dataclass(frozen=True)
class IsolationAuditResult:
    project_count: int
    unauthorized_cross_reads: int
    unauthorized_cross_writes: int
    shared_character_conflicts: int
    shared_world_conflicts: int
    raw_manuscript_leakage: int
    status: Literal["PASS", "WARN", "BLOCK"]
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CanonConflict:
    conflict_id: str
    project_id: str
    entity_id: str
    conflict_type: Literal["timeline", "character_identity", "world_rule", "relationship", "license"]
    severity: float
    evidence: list[str]
    recommended_action: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MultiWorkAbsorptionPlan:
    next_stage: str
    safe_to_absorb_read_only: bool
    blocked_modules: list[str]
    adapter_required: list[str]
    required_gates: list[str]
    required_tests: list[str]
    required_manifests: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
