from __future__ import annotations


def calculate_reward(values: dict[str, float]) -> float:
    return round(sum(max(0.0, min(1.0, value)) for value in values.values()), 3)
