from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConflictCollisionReport:
    collision_count: int
    protected_collision_count: int
    unresolved_collision_count: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class ConflictCollisionCalculus:
    def evaluate(self, season_evidence: dict[str, Any]) -> ConflictCollisionReport:
        collision_count = 0
        protected_count = 0
        for episode in season_evidence.get("episodes", []):
            if float(episode.get("tension_level", 0.0)) >= 0.7:
                collision_count += 1
                if int(episode.get("causal_input_count", 0)) > 0 and int(episode.get("knowledge_constraint_count", 0)) > 0:
                    protected_count += 1
        unresolved = max(0, collision_count - protected_count)
        return ConflictCollisionReport(
            collision_count=collision_count,
            protected_collision_count=protected_count,
            unresolved_collision_count=unresolved,
            status="pass" if unresolved == 0 else "blocked",
        )
