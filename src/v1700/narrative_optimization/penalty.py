from __future__ import annotations


def calculate_penalty(*, leakage_count: int = 0, fatigue: float = 0.0, confusion: float = 0.0, repetition: float = 0.0) -> float:
    return round(leakage_count * 2.0 + fatigue * 0.6 + confusion * 0.8 + repetition * 0.5, 3)
