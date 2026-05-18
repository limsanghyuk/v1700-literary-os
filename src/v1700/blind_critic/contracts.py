from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any


EVALUATION_AXES = (
    "series_story_arc",
    "macro_plot_architecture",
    "episode_microplot_linkage",
    "supporting_character_web",
    "causal_event_weaving",
    "emotional_accessibility",
    "prose_naturalness",
    "mise_en_scene_density",
    "reveal_safety",
    "longform_expandability",
)


@dataclass(frozen=True)
class CandidateSample:
    candidate_id: str
    source_label: str
    hidden_label: str
    text: str
    evidence: dict[str, Any]

    def to_blind_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "hidden_label": self.hidden_label,
            "text": self.text,
            "evidence": dict(self.evidence),
        }

    def to_revealed_dict(self) -> dict[str, Any]:
        data = self.to_blind_dict()
        data["source_label"] = self.source_label
        return data


@dataclass(frozen=True)
class CandidateScore:
    candidate_id: str
    axes: dict[str, float]
    rationale: dict[str, str]

    @property
    def average(self) -> float:
        if not self.axes:
            return 0.0
        return round(mean(self.axes.values()), 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "axes": dict(self.axes),
            "average": self.average,
            "rationale": dict(self.rationale),
        }


@dataclass(frozen=True)
class BlindCriticBenchmarkReport:
    status: str
    prompt: str
    axes: tuple[str, ...]
    blind_candidates: tuple[CandidateSample, ...]
    scores: tuple[CandidateScore, ...]
    winner_candidate_id: str
    winner_source_label: str
    pure_gpt_baseline_candidate_id: str
    v1700_candidate_id: str
    v1700_margin_over_pure_gpt: float
    reveal_leakage_count: int
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    benchmark_mode: str
    pass_meaning: str

    def score_by_source(self, source_label: str) -> CandidateScore | None:
        source_to_id = {c.source_label: c.candidate_id for c in self.blind_candidates}
        cid = source_to_id.get(source_label)
        if not cid:
            return None
        return next((score for score in self.scores if score.candidate_id == cid), None)

    def to_dict(self, reveal_sources: bool = True) -> dict[str, Any]:
        candidates = [
            candidate.to_revealed_dict() if reveal_sources else candidate.to_blind_dict()
            for candidate in self.blind_candidates
        ]
        return {
            "status": self.status,
            "prompt": self.prompt,
            "axes": list(self.axes),
            "blind_candidates": candidates,
            "scores": [score.to_dict() for score in self.scores],
            "winner_candidate_id": self.winner_candidate_id,
            "winner_source_label": self.winner_source_label if reveal_sources else "REDACTED_UNTIL_REVEAL",
            "pure_gpt_baseline_candidate_id": self.pure_gpt_baseline_candidate_id,
            "v1700_candidate_id": self.v1700_candidate_id,
            "v1700_margin_over_pure_gpt": self.v1700_margin_over_pure_gpt,
            "reveal_leakage_count": self.reveal_leakage_count,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "benchmark_mode": self.benchmark_mode,
            "pass_meaning": self.pass_meaning,
        }
