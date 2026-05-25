from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Page04StageSeal:
    stage: str
    title: str
    report_path: str
    gate_path: str
    status: str
    sealed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "title": self.title,
            "report_path": self.report_path,
            "gate_path": self.gate_path,
            "status": self.status,
            "sealed": self.sealed,
        }


@dataclass(frozen=True)
class Page04SealCheck:
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


@dataclass(frozen=True)
class Page04ReleaseAsset:
    path: str
    required: bool
    category: str
    exists: bool
    generated_by_stage166: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "required": self.required,
            "category": self.category,
            "exists": self.exists,
            "generated_by_stage166": self.generated_by_stage166,
        }


@dataclass(frozen=True)
class Page04InvariantFreeze:
    name: str
    frozen_value: str | bool | int
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "frozen_value": self.frozen_value,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class Page04TransitionCriterion:
    name: str
    status: str
    next_page: str
    evidence: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "status": self.status,
            "next_page": self.next_page,
            "evidence": self.evidence,
        }
