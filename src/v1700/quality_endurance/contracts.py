from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class QualityScore:
    axes: dict[str, float]

    @property
    def average(self) -> float:
        if not self.axes:
            return 0.0
        return round(mean(self.axes.values()), 2)

    @property
    def blockers(self) -> tuple[str, ...]:
        return tuple(axis for axis, score in self.axes.items() if score < 8.0)

    def to_dict(self) -> dict:
        return {"axes": dict(self.axes), "average": self.average, "blockers": list(self.blockers)}


@dataclass(frozen=True)
class RevisionTrace:
    scene_id: str
    before_text: str
    after_text: str
    before_score: QualityScore
    after_score: QualityScore
    delta: float
    constraints: dict[str, float]
    risk_flags: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "scene_id": self.scene_id,
            "before_text": self.before_text,
            "after_text": self.after_text,
            "before_score": self.before_score.to_dict(),
            "after_score": self.after_score.to_dict(),
            "delta": self.delta,
            "constraints": dict(self.constraints),
            "risk_flags": list(self.risk_flags),
        }


@dataclass(frozen=True)
class QualityEnduranceReport:
    status: str
    scene_count: int
    revised_scene_count: int
    average_before: float
    average_after: float
    average_delta: float
    blocker_count_before: int
    blocker_count_after: int
    anti_llm_min_after: float
    reveal_leakage_count: int
    timeline_contradiction_count: int
    traces: tuple[RevisionTrace, ...]

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "scene_count": self.scene_count,
            "revised_scene_count": self.revised_scene_count,
            "average_before": self.average_before,
            "average_after": self.average_after,
            "average_delta": self.average_delta,
            "blocker_count_before": self.blocker_count_before,
            "blocker_count_after": self.blocker_count_after,
            "anti_llm_min_after": self.anti_llm_min_after,
            "reveal_leakage_count": self.reveal_leakage_count,
            "timeline_contradiction_count": self.timeline_contradiction_count,
            "traces": [trace.to_dict() for trace in self.traces],
        }
