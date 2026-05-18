from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RevealEntropyReport:
    entropy_by_episode: tuple[dict[str, Any], ...]
    premature_reveal_penalty: float
    reveal_leakage_count: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "entropy_by_episode": list(self.entropy_by_episode),
            "premature_reveal_penalty": self.premature_reveal_penalty,
            "reveal_leakage_count": self.reveal_leakage_count,
            "status": self.status,
        }


class RevealEntropyBudgetEngine:
    def calculate(self, season_evidence: dict[str, Any]) -> RevealEntropyReport:
        rows: list[dict[str, Any]] = []
        penalty = 0.0
        leakage = 0
        episodes = season_evidence.get("episodes", [])
        for index, episode in enumerate(episodes, start=1):
            blocked = int(episode.get("blocked_direct_reveal_count", 0))
            policies = max(1, int(episode.get("reveal_policy_count", 1)))
            entropy = round(min(1.0, blocked / policies), 3)
            if index <= max(1, len(episodes) // 4) and entropy < 0.25:
                penalty += 0.25
            rows.append(
                {
                    "episode_id": episode.get("episode_id", ""),
                    "entropy": entropy,
                    "blocked_direct_reveal_count": blocked,
                    "reveal_policy_count": policies,
                }
            )
            leakage += sum(1 for scene in episode.get("scenes", []) if "RAW_REVEAL:" in str(scene))
        return RevealEntropyReport(
            entropy_by_episode=tuple(rows),
            premature_reveal_penalty=round(penalty, 3),
            reveal_leakage_count=leakage,
            status="pass" if leakage == 0 and penalty <= 0.5 else "blocked",
        )
