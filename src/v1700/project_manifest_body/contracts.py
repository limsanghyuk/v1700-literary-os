from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ManifestBodySection:
    name: str
    source_path: str
    target_state: str
    required_fields: tuple[str, ...]
    read_only: bool
    synthetic_only: bool
    public_safe_only: bool
    notes: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "source_path": self.source_path,
            "target_state": self.target_state,
            "required_fields": list(self.required_fields),
            "read_only": self.read_only,
            "synthetic_only": self.synthetic_only,
            "public_safe_only": self.public_safe_only,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ManifestStateBinding:
    manifest_section: str
    state_contract: str
    binding_scope: str
    bound_fields: tuple[str, ...]
    derived_fields: tuple[str, ...]
    write_policy: str

    def to_dict(self) -> dict[str, object]:
        return {
            "manifest_section": self.manifest_section,
            "state_contract": self.state_contract,
            "binding_scope": self.binding_scope,
            "bound_fields": list(self.bound_fields),
            "derived_fields": list(self.derived_fields),
            "write_policy": self.write_policy,
        }


@dataclass(frozen=True)
class PolicyBoundaryControl:
    name: str
    description: str
    enforced: bool
    evidence: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "enforced": self.enforced,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class ManifestLoadStep:
    order_index: int
    name: str
    depends_on: tuple[str, ...]
    output: str
    rationale: str

    def to_dict(self) -> dict[str, object]:
        return {
            "order_index": self.order_index,
            "name": self.name,
            "depends_on": list(self.depends_on),
            "output": self.output,
            "rationale": self.rationale,
        }
