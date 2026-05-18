from dataclasses import dataclass, field

@dataclass(frozen=True)
class RenderedProseIR:
    scene_id: str
    final_text: str
    surface_score: dict[str, float] = field(default_factory=dict)
    constraint_score: dict[str, float] = field(default_factory=dict)
    risk_flags: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "scene_id": self.scene_id,
            "final_text": self.final_text,
            "surface_score": dict(self.surface_score),
            "constraint_score": dict(self.constraint_score),
            "risk_flags": list(self.risk_flags),
        }
