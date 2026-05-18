from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class SceneTensionPoint:
    """A deterministic Stage117 scene tension sample.

    position is normalized to [0, 1]. tension_score is the observed scene
    pressure used by NarrativeTensionCurve.actual(). act is 1..4 and supports
    coverage loss without depending on generated prose.
    """

    scene_id: str
    position: float
    tension_score: float
    act: int
    function: str = "structural_scene"

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "position": self.position,
            "tension_score": self.tension_score,
            "act": self.act,
            "function": self.function,
        }


@dataclass(frozen=True)
class TensionLossReport:
    scene_count: int
    tension_loss: float
    coverage_loss: float
    final_loss: float
    lambda_coverage: float
    status: Literal["PASS", "WARN", "BLOCK"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_count": self.scene_count,
            "tension_loss": self.tension_loss,
            "coverage_loss": self.coverage_loss,
            "final_loss": self.final_loss,
            "lambda_coverage": self.lambda_coverage,
            "status": self.status,
        }
