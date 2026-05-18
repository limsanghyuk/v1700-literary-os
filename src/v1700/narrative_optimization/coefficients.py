from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class NarrativePhysicsCoefficientSet:
    state_continuity_weight: float = 1.0
    belief_consistency_weight: float = 1.0
    reveal_entropy_weight: float = 1.0
    emotional_momentum_weight: float = 1.0
    conflict_collision_weight: float = 1.0
    scene_energy_weight: float = 1.0
    motif_residue_weight: float = 1.0
    curiosity_gradient_weight: float = 1.0
    surface_safety_weight: float = 1.25
    branchpoint_survival_weight: float = 1.35
    leakage_penalty_weight: float = 2.0
    fatigue_penalty_weight: float = 0.6
    confusion_penalty_weight: float = 0.8
    repetition_penalty_weight: float = 0.5

    def to_dict(self) -> dict[str, float]:
        return {field.name: float(getattr(self, field.name)) for field in fields(self)}

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "NarrativePhysicsCoefficientSet":
        allowed = {field.name for field in fields(cls)}
        return cls(**{key: float(value) for key, value in values.items() if key in allowed})


PROTECTED_NON_DECREASING_WEIGHTS = (
    "branchpoint_survival_weight",
    "surface_safety_weight",
    "leakage_penalty_weight",
)
