from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderingFieldSpec:
    name: str
    type: str
    required: bool
    visibility: str
    description: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "visibility": self.visibility,
            "description": self.description,
        }


@dataclass(frozen=True)
class RenderingContractSpec:
    name: str
    render_type: str
    purpose: str
    source_authority: str
    render_mode: str
    generation_policy: str
    node2_projection: str
    fields: tuple[RenderingFieldSpec, ...]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "render_type": self.render_type,
            "purpose": self.purpose,
            "source_authority": self.source_authority,
            "render_mode": self.render_mode,
            "generation_policy": self.generation_policy,
            "node2_projection": self.node2_projection,
            "fields": [field.to_dict() for field in self.fields],
        }


@dataclass(frozen=True)
class RenderingBoundaryRule:
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
class RenderingWritePolicyRule:
    name: str
    default_enabled: bool
    future_policy_only: bool
    generation_runtime_allowed: bool
    runtime_write_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "default_enabled": self.default_enabled,
            "future_policy_only": self.future_policy_only,
            "generation_runtime_allowed": self.generation_runtime_allowed,
            "runtime_write_allowed": self.runtime_write_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class Node2RenderingProjectionRule:
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
class Page04ReadinessCheck:
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
