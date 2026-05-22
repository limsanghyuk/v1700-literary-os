from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NarrativeFieldSpec:
    name: str
    field_type: str
    required: bool
    description: str
    source_of_truth: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "field_type": self.field_type,
            "required": self.required,
            "description": self.description,
            "source_of_truth": self.source_of_truth,
        }


@dataclass(frozen=True)
class NarrativeStateContract:
    name: str
    scope: str
    purpose: str
    write_policy: str
    fields: tuple[NarrativeFieldSpec, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "scope": self.scope,
            "purpose": self.purpose,
            "write_policy": self.write_policy,
            "field_count": len(self.fields),
            "fields": [field.to_dict() for field in self.fields],
        }


@dataclass(frozen=True)
class StateHierarchyEdge:
    parent: str
    child: str
    cardinality: str
    authority: str

    def to_dict(self) -> dict[str, str]:
        return {
            "parent": self.parent,
            "child": self.child,
            "cardinality": self.cardinality,
            "authority": self.authority,
        }


@dataclass(frozen=True)
class ContinuityRule:
    name: str
    description: str
    enforced: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "enforced": self.enforced,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class RevealBoundarySpec:
    state_name: str
    node1_access: str
    node2_access: str
    node3_access: str
    rationale: str

    def to_dict(self) -> dict[str, str]:
        return {
            "state_name": self.state_name,
            "node1_access": self.node1_access,
            "node2_access": self.node2_access,
            "node3_access": self.node3_access,
            "rationale": self.rationale,
        }
