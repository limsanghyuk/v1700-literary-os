from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


CandidateMode = Literal[
    "PURE_GPT_DIRECT",
    "CLAUDE_REFERENCE",
    "GEMINI_REFERENCE",
    "OLLAMA_LOCAL_DRAFT",
    "V1700_PROSE",
    "V1700_SCENARIO",
    "V430_SCENARIO_ROOM",
    "V1700_HYBRID",
]


@dataclass(frozen=True)
class WriterTrialSeed:
    seed_id: str
    prompt: str
    target_mode: Literal["PROSE", "SCENARIO", "HYBRID"]
    evaluation_goal: str
    constraints: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TrialCandidate:
    candidate_id: str
    hidden_label: str
    mode: CandidateMode
    visible_excerpt: str
    evidence_markers: tuple[str, ...]
    provider_call_count: int = 0
    raw_manuscript_provider_leakage: int = 0
    node2_raw_reveal_access: int = 0

    def blind_payload(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "hidden_label": self.hidden_label,
            "visible_excerpt": self.visible_excerpt,
            "evidence_markers": list(self.evidence_markers),
        }

    def to_dict(self, *, reveal_mode: bool = True) -> dict[str, Any]:
        payload = self.blind_payload()
        if reveal_mode:
            payload.update(
                {
                    "mode": self.mode,
                    "provider_call_count": self.provider_call_count,
                    "raw_manuscript_provider_leakage": self.raw_manuscript_provider_leakage,
                    "node2_raw_reveal_access": self.node2_raw_reveal_access,
                }
            )
        return payload


@dataclass(frozen=True)
class BlindTrialScorecard:
    candidate_id: str
    reviewer_id: str
    axis_scores: dict[str, float]
    weighted_score: float
    verdict: Literal["PASS", "REVISE", "BLOCK"]
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WriterTaskResult:
    task_id: str
    description: str
    completion_status: Literal["PASS", "WARN", "BLOCK"]
    baseline_minutes: int
    v1700_minutes: int
    friction_score: float
    notes: tuple[str, ...]

    @property
    def saved_minutes(self) -> int:
        return max(0, self.baseline_minutes - self.v1700_minutes)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["saved_minutes"] = self.saved_minutes
        return payload


@dataclass(frozen=True)
class RevisionEfficiencyReport:
    baseline_revision_minutes: int
    v1700_revision_minutes: int
    issue_count_before: int
    issue_count_after: int
    unresolved_block_items: int
    plot_consistency_status: Literal["PASS", "WARN", "BLOCK"]
    payoff_debt_status: Literal["PASS", "WARN", "BLOCK"]
    scene_necessity_status: Literal["PASS", "WARN", "BLOCK"]

    @property
    def revision_time_reduction_ratio(self) -> float:
        if self.baseline_revision_minutes <= 0:
            return 0.0
        return round((self.baseline_revision_minutes - self.v1700_revision_minutes) / self.baseline_revision_minutes, 3)

    @property
    def issue_reduction_ratio(self) -> float:
        if self.issue_count_before <= 0:
            return 0.0
        return round((self.issue_count_before - self.issue_count_after) / self.issue_count_before, 3)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["revision_time_reduction_ratio"] = self.revision_time_reduction_ratio
        payload["issue_reduction_ratio"] = self.issue_reduction_ratio
        return payload
