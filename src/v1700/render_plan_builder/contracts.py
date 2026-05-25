from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RenderPlanNode:
    node_id: str
    render_packet_id: str
    render_type: str
    project_id: str
    surface_channel: str
    boundary_level: str
    visibility: str
    render_mode: str
    checksum: str
    level: int
    node2_projection_summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "render_packet_id": self.render_packet_id,
            "render_type": self.render_type,
            "project_id": self.project_id,
            "surface_channel": self.surface_channel,
            "boundary_level": self.boundary_level,
            "visibility": self.visibility,
            "render_mode": self.render_mode,
            "checksum": self.checksum,
            "level": self.level,
            "node2_projection_summary": self.node2_projection_summary,
        }


@dataclass(frozen=True)
class RenderPlanEdge:
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
class RenderPlanPolicy:
    name: str
    deterministic: bool
    dry_run_only: bool
    runtime_render_allowed: bool
    provider_generation_allowed: bool
    write_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "deterministic": self.deterministic,
            "dry_run_only": self.dry_run_only,
            "runtime_render_allowed": self.runtime_render_allowed,
            "provider_generation_allowed": self.provider_generation_allowed,
            "write_allowed": self.write_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class RenderPlanProjectionRule:
    name: str
    node2_surface_allowed: bool
    hidden_render_payload_blocked: bool
    provider_generation_payload_blocked: bool
    write_handle_blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "node2_surface_allowed": self.node2_surface_allowed,
            "hidden_render_payload_blocked": self.hidden_render_payload_blocked,
            "provider_generation_payload_blocked": self.provider_generation_payload_blocked,
            "write_handle_blocked": self.write_handle_blocked,
            "evidence": self.evidence,
        }
