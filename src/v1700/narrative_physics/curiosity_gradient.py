from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AudienceCuriosityGradientReport:
    gradient: tuple[dict[str, Any], ...]
    finale_rise: float
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {"gradient": list(self.gradient), "finale_rise": self.finale_rise, "status": self.status}


class AudienceCuriosityGradientEngine:
    def calculate(self, season_evidence: dict[str, Any]) -> AudienceCuriosityGradientReport:
        rows = []
        episodes = season_evidence.get("episodes", [])
        total = max(1, len(episodes))
        for index, episode in enumerate(episodes, start=1):
            reveal_pressure = int(episode.get("blocked_direct_reveal_count", 0)) * 0.035
            callback_pressure = int(episode.get("callback_edge_count", 0)) * 0.05
            value = round(min(1.0, 0.38 + index / total * 0.42 + reveal_pressure + callback_pressure), 3)
            rows.append({"episode_id": episode.get("episode_id", ""), "curiosity": value})
        finale_rise = round(rows[-1]["curiosity"] - rows[0]["curiosity"], 3) if len(rows) >= 2 else 0.0
        return AudienceCuriosityGradientReport(
            gradient=tuple(rows),
            finale_rise=finale_rise,
            status="pass" if finale_rise > 0.25 else "blocked",
        )
