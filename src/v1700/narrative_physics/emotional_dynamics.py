from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EmotionalMomentumReport:
    curve: tuple[dict[str, Any], ...]
    spike_count: int
    fatigue_count: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "curve": list(self.curve),
            "spike_count": self.spike_count,
            "fatigue_count": self.fatigue_count,
            "status": self.status,
        }


class EmotionalMomentumDynamicsEngine:
    def evaluate(self, season_evidence: dict[str, Any]) -> EmotionalMomentumReport:
        curve = []
        previous = None
        spike_count = 0
        fatigue_count = 0
        for episode in season_evidence.get("episodes", []):
            value = round(float(episode.get("tension_level", 0.0)), 3)
            delta = 0.0 if previous is None else round(value - previous, 3)
            if abs(delta) > 0.42:
                spike_count += 1
            if previous is not None and abs(delta) < 0.015:
                fatigue_count += 1
            curve.append({"episode_id": episode.get("episode_id", ""), "momentum": value, "delta": delta})
            previous = value
        return EmotionalMomentumReport(
            curve=tuple(curve),
            spike_count=spike_count,
            fatigue_count=fatigue_count,
            status="pass" if spike_count <= 2 and fatigue_count <= 4 else "blocked",
        )
