from __future__ import annotations


def bounded_delta(delta: float, *, limit: float = 0.05) -> float:
    return round(max(-limit, min(limit, delta)), 3)
