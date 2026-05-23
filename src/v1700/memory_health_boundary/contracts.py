from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthCheckResult:
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


@dataclass(frozen=True)
class LeakageScanRule:
    name: str
    forbidden_pattern: str
    scope: str
    leak_count: int
    evidence: str

    def to_dict(self) -> dict[str, str | int | bool]:
        return {
            "name": self.name,
            "forbidden_pattern": self.forbidden_pattern,
            "scope": self.scope,
            "leak_count": self.leak_count,
            "passed": self.leak_count == 0,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class BoundaryProbe:
    name: str
    probe_query: str
    candidate_count: int
    node2_projection_count: int
    blocked_projection_count: int
    raw_reveal_access: int
    passed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | int | bool]:
        return {
            "name": self.name,
            "probe_query": self.probe_query,
            "candidate_count": self.candidate_count,
            "node2_projection_count": self.node2_projection_count,
            "blocked_projection_count": self.blocked_projection_count,
            "raw_reveal_access": self.raw_reveal_access,
            "passed": self.passed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class BoundaryHealthEntry:
    boundary_level: str
    record_count: int
    node2_access: str
    expected_node2_access: str
    passed: bool

    def to_dict(self) -> dict[str, str | int | bool]:
        return {
            "boundary_level": self.boundary_level,
            "record_count": self.record_count,
            "node2_access": self.node2_access,
            "expected_node2_access": self.expected_node2_access,
            "passed": self.passed,
        }
