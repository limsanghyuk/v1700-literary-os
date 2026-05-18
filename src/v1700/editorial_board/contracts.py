from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal

ReviewerRole = Literal[
    "LITERARY_CRITIC",
    "DRAMATURG",
    "MARKET_EDITOR",
    "GENRE_EDITOR",
    "CONTINUITY_AUDITOR",
    "SCENARIO_PRODUCER",
]
ReviewMode = Literal["PROSE", "SCENARIO", "LONGFORM_STRUCTURE", "PRODUCTION_READINESS"]

@dataclass(frozen=True)
class EditorialReviewer:
    reviewer_id: str
    role: ReviewerRole
    lens: str
    weight: float
    provider_lane: str = "fixture_reviewer"

@dataclass(frozen=True)
class ReviewPacket:
    packet_id: str
    mode: ReviewMode
    payload_kind: Literal["FEATURE_ONLY", "FIXTURE_SUMMARY", "REDACTED_EXCERPT"]
    source_stage: str
    contains_raw_manuscript: bool
    prompt_sha256: str
    production_scope: str
    notes: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class EditorialScorecard:
    scorecard_id: str
    reviewer_id: str
    packet_id: str
    mode: ReviewMode
    score_total: float
    score_breakdown: dict[str, float]
    release_relevance: Literal["INFO", "WARN", "BLOCK"]
    notes: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class EditorialConsensus:
    status: Literal["pass", "warn", "blocked"]
    average_score: float
    blocker_count: int
    warn_count: int
    reviewer_count: int
    packet_count: int
    recommendations: list[str]

def to_dict(obj):
    return asdict(obj)
