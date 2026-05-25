from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionFieldSpec:
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
class ExecutionPacketContract:
    name: str
    packet_type: str
    purpose: str
    source_authority: str
    execution_mode: str
    write_policy: str
    node2_projection: str
    fields: tuple[ExecutionFieldSpec, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "packet_type": self.packet_type,
            "purpose": self.purpose,
            "source_authority": self.source_authority,
            "execution_mode": self.execution_mode,
            "write_policy": self.write_policy,
            "node2_projection": self.node2_projection,
            "field_count": len(self.fields),
            "fields": [field.to_dict() for field in self.fields],
        }


@dataclass(frozen=True)
class ExecutionBoundaryRule:
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
class ExecutionWritePolicyRule:
    name: str
    default_enabled: bool
    future_policy_only: bool
    runtime_execution_allowed: bool
    runtime_write_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "default_enabled": self.default_enabled,
            "future_policy_only": self.future_policy_only,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "runtime_write_allowed": self.runtime_write_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class Node2ExecutionProjectionRule:
    name: str
    allowed_surface: str
    forbidden_payload: str
    blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "allowed_surface": self.allowed_surface,
            "forbidden_payload": self.forbidden_payload,
            "blocked": self.blocked,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class Page03ReadinessCheck:
    name: str
    status: str
    evidence: str
    description: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "status": self.status,
            "evidence": self.evidence,
            "description": self.description,
        }
