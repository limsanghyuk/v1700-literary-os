from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmotionalMomentumVector:
    tension: float = 0.0
    sympathy: float = 0.0
    dread: float = 0.0
    catharsis: float = 0.0

    def clamp(self) -> "EmotionalMomentumVector":
        return EmotionalMomentumVector(*[max(0.0, min(1.0, value)) for value in self.as_tuple()])

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.tension, self.sympathy, self.dread, self.catharsis)

    def intensity(self) -> float:
        return round(sum(self.as_tuple()) / 4.0, 4)

    def to_dict(self) -> dict:
        return {
            "tension": round(self.tension, 4),
            "sympathy": round(self.sympathy, 4),
            "dread": round(self.dread, 4),
            "catharsis": round(self.catharsis, 4),
            "intensity": self.intensity(),
        }


class EmotionalMomentumTracker:
    def from_scene_terms(self, conflict: str, emotional_from: str, emotional_to: str) -> EmotionalMomentumVector:
        hay = " ".join((conflict, emotional_from, emotional_to)).lower()
        tension = 0.35 + (0.35 if any(key in hay for key in ("충돌", "의심", "갈등", "위기", "tension")) else 0.0)
        sympathy = 0.25 + (0.25 if any(key in hay for key in ("안도", "연민", "보호", "sympathy")) else 0.0)
        dread = 0.20 + (0.35 if any(key in hay for key in ("불신", "두려", "비밀", "dread", "공포")) else 0.0)
        catharsis = 0.10 + (0.30 if any(key in hay for key in ("해소", "고백", "회수", "catharsis")) else 0.0)
        return EmotionalMomentumVector(tension, sympathy, dread, catharsis).clamp()

    def transition(self, previous: EmotionalMomentumVector, delta: EmotionalMomentumVector) -> EmotionalMomentumVector:
        return EmotionalMomentumVector(
            previous.tension * 0.55 + delta.tension * 0.45,
            previous.sympathy * 0.55 + delta.sympathy * 0.45,
            previous.dread * 0.55 + delta.dread * 0.45,
            previous.catharsis * 0.55 + delta.catharsis * 0.45,
        ).clamp()
