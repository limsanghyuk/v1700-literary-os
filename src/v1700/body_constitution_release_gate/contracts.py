from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionGateRule:
    name: str
    description: str
    passed: bool
    source_stage: str
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "passed": self.passed,
            "source_stage": self.source_stage,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class ReleaseBlocker:
    name: str
    description: str
    blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "blocked": self.blocked,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class StageReadinessCheck:
    name: str
    description: str
    ready: bool
    upstream: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "ready": self.ready,
            "upstream": self.upstream,
        }


@dataclass(frozen=True)
class LineageEvidence:
    stage: str
    title: str
    report_path: str
    manifest_path: str
    docs_path: str
    present: bool

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "stage": self.stage,
            "title": self.title,
            "report_path": self.report_path,
            "manifest_path": self.manifest_path,
            "docs_path": self.docs_path,
            "present": self.present,
        }
