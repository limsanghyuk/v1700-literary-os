from __future__ import annotations

from typing import Any, Iterable

from v1700.nie.arc.narrative_tension_curve import NarrativeTensionCurve


def coverage_loss(scenes: Iterable[Any], target_counts: dict[int, int] | None = None) -> float:
    return NarrativeTensionCurve().coverage_loss(list(scenes), target_counts=target_counts)
