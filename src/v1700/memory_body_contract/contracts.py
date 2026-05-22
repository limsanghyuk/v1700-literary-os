from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryFieldSpec:
    name: str
    field_type: str
    required: bool
    visibility: str
    description: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "field_type": self.field_type,
            "required": self.required,
            "visibility": self.visibility,
            "description": self.description,
        }


@dataclass(frozen=True)
class MemoryRecordContract:
    name: str
    record_type: str
    purpose: str
    source_authority: str
    write_policy: str
    node2_projection: str
    fields: tuple[MemoryFieldSpec, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "record_type": self.record_type,
            "purpose": self.purpose,
            "source_authority": self.source_authority,
            "write_policy": self.write_policy,
            "node2_projection": self.node2_projection,
            "field_count": len(self.fields),
            "fields": [field.to_dict() for field in self.fields],
        }


@dataclass(frozen=True)
class MemoryBoundaryRule:
    name: str
    boundary_level: str
    node1_access: str
    node2_access: str
    node3_access: str
    enforced: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "boundary_level": self.boundary_level,
            "node1_access": self.node1_access,
            "node2_access": self.node2_access,
            "node3_access": self.node3_access,
            "enforced": self.enforced,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class MemoryWritePolicyRule:
    name: str
    default_enabled: bool
    future_policy_only: bool
    human_approval_required: bool
    runtime_write_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "default_enabled": self.default_enabled,
            "future_policy_only": self.future_policy_only,
            "human_approval_required": self.human_approval_required,
            "runtime_write_allowed": self.runtime_write_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class Node2ProjectionRule:
    name: str
    description: str
    forbidden_payload: str
    blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "forbidden_payload": self.forbidden_payload,
            "blocked": self.blocked,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class PreflightCheck:
    name: str
    description: str
    status: str
    evidence: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "evidence": self.evidence,
        }
