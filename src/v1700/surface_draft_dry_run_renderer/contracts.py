from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SurfaceDraftUnit:
    draft_unit_id: str
    render_plan_node_id: str
    render_packet_id: str
    render_type: str
    surface_channel: str
    project_id: str
    boundary_level: str
    visibility: str
    draft_text: str
    checksum: str
    order_index: int
    node2_projection_summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "draft_unit_id": self.draft_unit_id,
            "render_plan_node_id": self.render_plan_node_id,
            "render_packet_id": self.render_packet_id,
            "render_type": self.render_type,
            "surface_channel": self.surface_channel,
            "project_id": self.project_id,
            "boundary_level": self.boundary_level,
            "visibility": self.visibility,
            "draft_text": self.draft_text,
            "checksum": self.checksum,
            "order_index": self.order_index,
            "node2_projection_summary": self.node2_projection_summary,
        }


@dataclass(frozen=True)
class DryRunRenderTraceStep:
    step_id: str
    draft_unit_id: str
    action: str
    deterministic: bool
    provider_call_allowed: bool
    write_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "step_id": self.step_id,
            "draft_unit_id": self.draft_unit_id,
            "action": self.action,
            "deterministic": self.deterministic,
            "provider_call_allowed": self.provider_call_allowed,
            "write_allowed": self.write_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class SurfaceDraftPolicy:
    name: str
    deterministic: bool
    dry_run_only: bool
    provider_generation_allowed: bool
    runtime_render_allowed: bool
    write_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "deterministic": self.deterministic,
            "dry_run_only": self.dry_run_only,
            "provider_generation_allowed": self.provider_generation_allowed,
            "runtime_render_allowed": self.runtime_render_allowed,
            "write_allowed": self.write_allowed,
            "evidence": self.evidence,
        }
