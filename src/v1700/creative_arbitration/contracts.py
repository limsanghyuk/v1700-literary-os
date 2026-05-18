from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

CreativeTask = Literal["STRUCTURE", "DIALOGUE", "VISUAL", "LOCAL_PRIVACY", "PROSE_SURFACE", "SCENARIO_BEAT"]
ProviderKind = Literal["gpt", "claude", "gemini", "ollama", "fixture", "mock"]
ReleaseStatus = Literal["PASS", "WARN", "BLOCK"]


@dataclass(frozen=True)
class ProviderRole:
    provider_id: str
    provider_kind: ProviderKind
    assigned_tasks: tuple[CreativeTask, ...]
    release_mode: Literal["FIXTURE_ONLY", "SANDBOX_OPT_IN"]
    live_call_allowed_in_release: bool = False
    raw_manuscript_allowed: bool = False
    strengths: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CreativeCandidate:
    candidate_id: str
    provider_id: str
    task: CreativeTask
    mode: Literal["PROSE", "SCENARIO", "HYBRID"]
    payload_kind: Literal["feature_only", "fixture_summary"]
    score: float
    rationale: str
    contains_raw_manuscript: bool = False
    live_call_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ArbitrationDecision:
    decision_id: str
    mode: Literal["PROSE", "SCENARIO", "HYBRID"]
    selected_candidate_ids: tuple[str, ...]
    rejected_candidate_ids: tuple[str, ...]
    merge_policy: str
    final_authority: str
    provider_call_count: int
    raw_manuscript_leakage: int
    status: ReleaseStatus = "PASS"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CreativeArbitrationReport:
    stage: str
    baseline_stage: str
    status: str
    provider_roles: tuple[ProviderRole, ...]
    candidates: tuple[CreativeCandidate, ...]
    decisions: tuple[ArbitrationDecision, ...]
    issues: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "status": self.status,
            "provider_roles": [role.to_dict() for role in self.provider_roles],
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "decisions": [decision.to_dict() for decision in self.decisions],
            "issues": list(self.issues),
        }
