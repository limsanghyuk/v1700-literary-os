from dataclasses import dataclass, field

@dataclass
class CharacterEventTimeLedger:
    facts: list[str] = field(default_factory=list)
    timeline_position: str = "UNKNOWN"
