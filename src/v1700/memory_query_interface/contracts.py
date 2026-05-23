
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MemoryQueryRequest:
    project_id: str
    query: str
    record_types: tuple[str, ...]
    node: str = "node1"
    limit: int = 10

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "query": self.query,
            "record_types": list(self.record_types),
            "node": self.node,
            "limit": self.limit,
        }


@dataclass(frozen=True)
class MemoryQueryCandidate:
    record_id: str
    record_type: str
    project_id: str
    source_state_id: str
    boundary_level: str
    summary: str
    score: float
    rank: int
    node2_projection: str
    checksum: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "record_type": self.record_type,
            "project_id": self.project_id,
            "source_state_id": self.source_state_id,
            "boundary_level": self.boundary_level,
            "summary": self.summary,
            "score": self.score,
            "rank": self.rank,
            "node2_projection": self.node2_projection,
            "checksum": self.checksum,
        }


@dataclass(frozen=True)
class QueryPolicyRule:
    name: str
    description: str
    passed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "passed": self.passed,
            "evidence": self.evidence,
        }
