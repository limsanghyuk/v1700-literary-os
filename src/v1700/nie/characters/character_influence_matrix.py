from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations, permutations
from typing import Any, Iterable

from v1700.nie.characters.centrality import betweenness_unweighted, pagerank_positive
from v1700.nie.characters.contracts import CentralityReport, InfluenceObservation, TriangleTension, clamp
from v1700.nie.characters.role_tier_assigner import assign_role_tiers
from v1700.nie.characters.structural_balance import compute_triangle_tension


@dataclass
class CharacterInfluenceMatrix:
    """Asymmetric W[n×n] narrative influence matrix for Stage115 NIE.

    W[i][j] means how character i changes character j's narrative pressure. The
    matrix is intentionally asymmetric: a secret keeper may dominate a witness
    even when the reverse influence is weak.
    """

    characters: tuple[str, ...]
    weights: dict[tuple[str, str], float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.characters = tuple(dict.fromkeys(self.characters))
        for src in self.characters:
            for dst in self.characters:
                if src == dst:
                    self.weights[(src, dst)] = 0.0
                else:
                    self.weights[(src, dst)] = clamp(self.weights.get((src, dst), 0.0))

    def update(self, observations: Iterable[InfluenceObservation]) -> None:
        for obs in observations:
            if obs.source not in self.characters or obs.target not in self.characters:
                raise ValueError(f"unknown character in influence observation: {obs.source}->{obs.target}")
            if obs.source == obs.target:
                continue
            before = self.weights.get((obs.source, obs.target), 0.0)
            self.weights[(obs.source, obs.target)] = clamp(before + obs.delta)

    def get_influence(self, source: str, target: str) -> float:
        return float(self.weights.get((source, target), 0.0))

    def matrix(self) -> list[list[float]]:
        return [[self.get_influence(src, dst) for dst in self.characters] for src in self.characters]

    def as_dict_matrix(self) -> dict[str, dict[str, float]]:
        return {src: {dst: self.get_influence(src, dst) for dst in self.characters} for src in self.characters}

    def asymmetric_pair_count(self) -> int:
        count = 0
        for a, b in combinations(self.characters, 2):
            if self.get_influence(a, b) != self.get_influence(b, a):
                count += 1
        return count

    def all_triangles(self) -> tuple[TriangleTension, ...]:
        result: list[TriangleTension] = []
        for a, b, c in permutations(self.characters, 3):
            if len({a, b, c}) == 3:
                result.append(compute_triangle_tension(a, b, c, self.get_influence(a, b), self.get_influence(b, c), self.get_influence(c, a)))
        # keep one canonical ordering per unordered trio by selecting sorted permutation start.
        canonical: dict[tuple[str, str, str], TriangleTension] = {}
        for tri in result:
            key = tuple(sorted(tri.characters))
            canonical.setdefault(key, tri)
        return tuple(canonical.values())

    def high_tension_triangles(self, threshold: float = 1.5) -> tuple[TriangleTension, ...]:
        return tuple(tri for tri in self.all_triangles() if tri.tension >= threshold)

    def pagerank(self) -> dict[str, float]:
        return pagerank_positive(self.characters, self.weights)

    def betweenness(self) -> dict[str, float]:
        return betweenness_unweighted(self.characters, self.weights)

    def centrality_report(self) -> CentralityReport:
        pr = self.pagerank()
        bc = self.betweenness()
        return CentralityReport(pagerank=pr, betweenness=bc, role_tiers=assign_role_tiers(pr, bc))

    def to_dict(self) -> dict[str, Any]:
        centrality = self.centrality_report()
        triangles = self.all_triangles()
        high = self.high_tension_triangles()
        return {
            "characters": list(self.characters),
            "matrix": self.as_dict_matrix(),
            "asymmetric_pair_count": self.asymmetric_pair_count(),
            "triangle_count": len(triangles),
            "high_tension_triangle_count": len(high),
            "triangles": [tri.to_dict() for tri in triangles],
            "high_tension_triangles": [tri.to_dict() for tri in high],
            "centrality": centrality.to_dict(),
        }
