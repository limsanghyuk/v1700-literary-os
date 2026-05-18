from dataclasses import dataclass, field

@dataclass
class RevealBudget:
    forbidden_reveals: set[str] = field(default_factory=set)

    def leakage(self, text: str) -> list[str]:
        return [item for item in self.forbidden_reveals if item and item in text]
