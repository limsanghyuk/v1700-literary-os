from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MotifResidueReport:
    motif_count: int
    callback_count: int
    payoff_count: int
    status: str
    motifs: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "motif_count": self.motif_count,
            "callback_count": self.callback_count,
            "payoff_count": self.payoff_count,
            "status": self.status,
            "motifs": list(self.motifs),
        }


class MotifResidueGraphBuilder:
    def build(self, season_evidence: dict[str, Any]) -> MotifResidueReport:
        motifs: dict[str, dict[str, Any]] = {}
        callback_count = 0
        for episode in season_evidence.get("episodes", []):
            callback_count += int(episode.get("callback_edge_count", 0))
            for scene in episode.get("scenes", []):
                marker = scene.get("afterimage_marker", "")
                key = marker.split("#", 1)[0].strip()
                if not key:
                    continue
                item = motifs.setdefault(key, {"motif": key, "appearances": 0, "episodes": set()})
                item["appearances"] += 1
                item["episodes"].add(episode.get("episode_id", ""))
        rows = tuple(
            {
                "motif": item["motif"],
                "appearances": item["appearances"],
                "episode_count": len(item["episodes"]),
            }
            for item in motifs.values()
        )
        payoff_count = sum(1 for item in rows if item["episode_count"] >= 2)
        return MotifResidueReport(
            motif_count=len(rows),
            callback_count=callback_count,
            payoff_count=payoff_count,
            status="pass" if rows and callback_count > 0 and payoff_count > 0 else "blocked",
            motifs=rows,
        )
