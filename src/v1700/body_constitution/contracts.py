from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FormulaClassificationEntry:
    name: str
    family: str
    status: str
    first_stage: str
    rationale: str
    notes: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "family": self.family,
            "status": self.status,
            "first_stage": self.first_stage,
            "rationale": self.rationale,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ConstitutionInvariant:
    name: str
    description: str
    enforced: bool
    enforcement: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "enforced": self.enforced,
            "enforcement": self.enforcement,
        }


@dataclass(frozen=True)
class BodyLayerSpec:
    name: str
    purpose: str
    first_stage: str
    next_stage: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "purpose": self.purpose,
            "first_stage": self.first_stage,
            "next_stage": self.next_stage,
        }


@dataclass(frozen=True)
class StageEntryCriterion:
    name: str
    description: str
    required: bool
    source_stage: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "source_stage": self.source_stage,
        }
