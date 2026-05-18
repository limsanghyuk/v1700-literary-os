from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

AccessType = Literal["read", "reference", "adapt", "write"]
ResourceType = Literal["shared_character", "shared_world"]
AdapterStatus = Literal["PASS", "WARN", "BLOCK"]


@dataclass(frozen=True)
class SharedCharacterRecord:
    character_id: str
    owner_project_id: str
    owner_id: str
    display_name: str
    public_domain_flag: bool = False
    license_policy_id: str = "private"
    raw_manuscript_excerpt: str | None = None
    surface_traits: tuple[str, ...] = field(default_factory=tuple)

    def to_feature_only_dict(self) -> dict[str, Any]:
        return {
            "character_id": self.character_id,
            "owner_project_id": self.owner_project_id,
            "owner_id": self.owner_id,
            "display_name": self.display_name,
            "public_domain_flag": self.public_domain_flag,
            "license_policy_id": self.license_policy_id,
            "surface_traits": list(self.surface_traits),
            "raw_text_redacted": self.raw_manuscript_excerpt is not None,
        }


@dataclass(frozen=True)
class SharedWorldRecord:
    world_id: str
    owner_project_id: str
    owner_id: str
    display_name: str
    world_rule_summary: tuple[str, ...] = field(default_factory=tuple)
    canon_source_of_truth: bool = False
    raw_world_bible_excerpt: str | None = None

    def to_read_only_dict(self) -> dict[str, Any]:
        return {
            "world_id": self.world_id,
            "owner_project_id": self.owner_project_id,
            "owner_id": self.owner_id,
            "display_name": self.display_name,
            "world_rule_summary": list(self.world_rule_summary),
            "canon_source_of_truth": self.canon_source_of_truth,
            "raw_text_redacted": self.raw_world_bible_excerpt is not None,
        }


@dataclass(frozen=True)
class ReadOnlyAccessRequest:
    source_project_id: str
    target_project_id: str
    resource_id: str
    resource_type: ResourceType
    access_type: AccessType
    same_owner: bool
    license_edge_exists: bool
    author_approval_valid: bool
    isolation_policy_allows: bool = True
    resource_scope_permits: bool = True
    public_domain_flag: bool = False

    def allowed(self) -> bool:
        if self.access_type == "write":
            return False
        licensed_or_safe = self.same_owner or self.license_edge_exists or self.public_domain_flag
        return bool(
            licensed_or_safe
            and self.author_approval_valid
            and self.isolation_policy_allows
            and self.resource_scope_permits
        )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["access_allowed"] = self.allowed()
        payload["write_disabled_by_stage128"] = self.access_type == "write"
        return payload


@dataclass(frozen=True)
class ReadOnlyAdapterResult:
    adapter_name: str
    status: AdapterStatus
    read_only: bool
    allowed_reads: int
    blocked_reads: int
    blocked_writes: int
    unauthorized_cross_reads: int
    unauthorized_cross_writes: int
    raw_text_exported: bool
    raw_manuscript_provider_leakage: int
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
