from dataclasses import dataclass, field

@dataclass
class StyleMemory:
    profile_features: dict = field(default_factory=dict)
    avoid_patterns: list[str] = field(default_factory=list)
    preferred_axes: list[str] = field(default_factory=lambda: ["light", "temperature", "object_texture"])
