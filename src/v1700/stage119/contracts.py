from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage119Contract:
    min_adversarial_cases: int = 12
    baseline_stage: str = "118"
    stage: str = "119"
    required_pack_files: tuple[str, ...] = (
        "adversarial_case_index.json",
        "adversarial_results.json",
        "stage119_summary.md",
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "min_adversarial_cases": self.min_adversarial_cases,
            "required_pack_files": list(self.required_pack_files),
        }
