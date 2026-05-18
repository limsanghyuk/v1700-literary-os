from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

RoleTier = Literal["jang", "cha", "po", "ma_sang", "jol"]


def clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return round(max(low, min(high, float(value))), 6)


def sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


@dataclass(frozen=True)
class InfluenceObservation:
    source: str
    target: str
    delta: float
    evidence: str
    scene_id: str = "stage115_fixture_scene_001"

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "delta": round(float(self.delta), 6),
            "evidence": self.evidence,
            "scene_id": self.scene_id,
        }


@dataclass(frozen=True)
class TriangleTension:
    a: str
    b: str
    c: str
    w_ab: float
    w_bc: float
    w_ca: float
    balance: int
    tension: int

    @property
    def characters(self) -> tuple[str, str, str]:
        return (self.a, self.b, self.c)

    def to_dict(self) -> dict[str, Any]:
        return {
            "characters": [self.a, self.b, self.c],
            "w_ab": self.w_ab,
            "w_bc": self.w_bc,
            "w_ca": self.w_ca,
            "balance": self.balance,
            "tension": self.tension,
        }


@dataclass(frozen=True)
class CentralityReport:
    pagerank: dict[str, float]
    betweenness: dict[str, float]
    role_tiers: dict[str, RoleTier]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pagerank": self.pagerank,
            "betweenness": self.betweenness,
            "role_tiers": self.role_tiers,
        }
