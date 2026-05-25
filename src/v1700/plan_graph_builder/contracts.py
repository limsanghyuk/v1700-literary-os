from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlanGraphNode:
    node_id: str
    packet_id: str
    packet_type: str
    project_id: str
    boundary_level: str
    visibility: str
    checksum: str
    level: int
    node2_projection_summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "packet_id": self.packet_id,
            "packet_type": self.packet_type,
            "project_id": self.project_id,
            "boundary_level": self.boundary_level,
            "visibility": self.visibility,
            "checksum": self.checksum,
            "level": self.level,
            "node2_projection_summary": self.node2_projection_summary,
        }


@dataclass(frozen=True)
class PlanGraphEdge:
    edge_id: str
    from_node_id: str
    to_node_id: str
    dependency_type: str

    def to_dict(self) -> dict[str, str]:
        return {
            "edge_id": self.edge_id,
            "from_node_id": self.from_node_id,
            "to_node_id": self.to_node_id,
            "dependency_type": self.dependency_type,
        }


@dataclass(frozen=True)
class PlanGraphPolicy:
    name: str
    deterministic: bool
    runtime_execution_allowed: bool
    write_allowed: bool
    provider_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "deterministic": self.deterministic,
            "runtime_execution_allowed": self.runtime_execution_allowed,
            "write_allowed": self.write_allowed,
            "provider_allowed": self.provider_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class PlanGraphProjectionRule:
    name: str
    node2_surface_allowed: bool
    hidden_payload_blocked: bool
    write_handle_blocked: bool
    provider_payload_blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "node2_surface_allowed": self.node2_surface_allowed,
            "hidden_payload_blocked": self.hidden_payload_blocked,
            "write_handle_blocked": self.write_handle_blocked,
            "provider_payload_blocked": self.provider_payload_blocked,
            "evidence": self.evidence,
        }
