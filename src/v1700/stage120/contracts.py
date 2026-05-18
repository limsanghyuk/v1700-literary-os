from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage120Contract:
    stage: str = "120"
    baseline_stage: str = "119"
    title: str = "Gate25 NIE v1.0 Release"
    gate_name: str = "Gate25"
    required_previous_stages: tuple[str, ...] = ("112", "113", "114", "115", "116", "117", "118", "119")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "gate_name": self.gate_name,
            "required_previous_stages": list(self.required_previous_stages),
        }
