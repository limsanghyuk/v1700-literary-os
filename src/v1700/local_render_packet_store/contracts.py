from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RenderPacketRecord:
    render_packet_id: str
    project_id: str
    render_type: str
    source_rendering_contract_id: str
    source_execution_packet_ids: tuple[str, ...]
    source_trace_ids: tuple[str, ...]
    surface_channel: str
    boundary_level: str
    visibility: str
    render_mode: str
    render_payload_summary: str
    node2_projection_summary: str
    created_from: str
    checksum: str
    write_policy: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "render_packet_id": self.render_packet_id,
            "project_id": self.project_id,
            "render_type": self.render_type,
            "source_rendering_contract_id": self.source_rendering_contract_id,
            "source_execution_packet_ids": list(self.source_execution_packet_ids),
            "source_trace_ids": list(self.source_trace_ids),
            "surface_channel": self.surface_channel,
            "boundary_level": self.boundary_level,
            "visibility": self.visibility,
            "render_mode": self.render_mode,
            "render_payload_summary": self.render_payload_summary,
            "node2_projection_summary": self.node2_projection_summary,
            "created_from": self.created_from,
            "checksum": self.checksum,
            "write_policy": self.write_policy,
        }


@dataclass(frozen=True)
class RenderPacketStorePolicy:
    name: str
    read_only: bool
    runtime_write_allowed: bool
    provider_generation_allowed: bool
    render_mutation_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "read_only": self.read_only,
            "runtime_write_allowed": self.runtime_write_allowed,
            "provider_generation_allowed": self.provider_generation_allowed,
            "render_mutation_allowed": self.render_mutation_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class RenderPacketProjectionRule:
    name: str
    render_type: str
    node2_surface_allowed: bool
    hidden_render_payload_blocked: bool
    provider_handle_blocked: bool
    write_handle_blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "render_type": self.render_type,
            "node2_surface_allowed": self.node2_surface_allowed,
            "hidden_render_payload_blocked": self.hidden_render_payload_blocked,
            "provider_handle_blocked": self.provider_handle_blocked,
            "write_handle_blocked": self.write_handle_blocked,
            "evidence": self.evidence,
        }
