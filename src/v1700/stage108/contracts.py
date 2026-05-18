from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class Stage108ReleaseContract:
    stage: str = "108"
    baseline_stage: str = "107.5"
    title: str = "External Review & Editorial Board Mode"
    release_gate_affected: bool = False
    live_provider_call_count_in_release_gate: int = 0
    raw_manuscript_provider_leakage: int = 0
    credential_leakage: int = 0
    required_reviewers: int = 6

@dataclass(frozen=True)
class Stage108Status:
    status: Literal["pass", "blocked"]
    reviewer_count: int
    scorecard_count: int
    average_score: float
