from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage117Contract:
    stage: str = "117"
    baseline_stage: str = "116"
    title: str = "NarrativeTensionCurve"
    ideal_curve_required: bool = True
    tension_loss_required: bool = True
    coverage_loss_required: bool = True
    final_loss_required: bool = True
    release_gate_live_provider_calls_allowed: bool = False
    next_development_order: tuple[str, ...] = ("Stage118", "Stage119", "Stage120")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "ideal_curve_required": self.ideal_curve_required,
            "tension_loss_required": self.tension_loss_required,
            "coverage_loss_required": self.coverage_loss_required,
            "final_loss_required": self.final_loss_required,
            "release_gate_live_provider_calls_allowed": self.release_gate_live_provider_calls_allowed,
            "next_development_order": list(self.next_development_order),
        }
