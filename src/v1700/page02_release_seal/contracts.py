from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page02StageSeal:
    stage: str
    title: str
    report_path: str
    gate_path: str
    status: str
    sealed: bool

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "stage": self.stage,
            "title": self.title,
            "report_path": self.report_path,
            "gate_path": self.gate_path,
            "status": self.status,
            "sealed": self.sealed,
        }


@dataclass(frozen=True)
class SealCheck:
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
class ReleaseSealAsset:
    path: str
    required: bool
    category: str
    exists: bool
    generated_by_stage154: bool = False

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "path": self.path,
            "required": self.required,
            "category": self.category,
            "exists": self.exists,
            "generated_by_stage154": self.generated_by_stage154,
        }


@dataclass(frozen=True)
class Page02Blocker:
    capability: str
    blocked: bool
    rationale: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "capability": self.capability,
            "blocked": self.blocked,
            "rationale": self.rationale,
        }
