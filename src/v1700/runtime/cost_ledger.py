from dataclasses import dataclass, field

@dataclass
class CostLedger:
    events: list[dict] = field(default_factory=list)

    def add(self, event: dict) -> None:
        self.events.append(dict(event))

    @property
    def total_events(self) -> int:
        return len(self.events)
