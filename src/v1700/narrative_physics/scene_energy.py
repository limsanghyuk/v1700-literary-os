from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SceneEnergyReport:
    average_energy: float
    minimum_energy: float
    dead_scene_count: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class SceneEnergyConservationAudit:
    def audit(self, season_evidence: dict[str, Any]) -> SceneEnergyReport:
        energies = [
            round(float(scene.get("quality_score", 0.0)) / 10.0, 3)
            for episode in season_evidence.get("episodes", [])
            for scene in episode.get("scenes", [])
        ]
        dead_scene_count = sum(1 for value in energies if value < 0.72)
        average = round(sum(energies) / len(energies), 3) if energies else 0.0
        minimum = round(min(energies), 3) if energies else 0.0
        return SceneEnergyReport(
            average_energy=average,
            minimum_energy=minimum,
            dead_scene_count=dead_scene_count,
            status="pass" if energies and dead_scene_count == 0 else "blocked",
        )
