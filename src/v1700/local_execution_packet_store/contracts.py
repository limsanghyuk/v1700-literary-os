from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExecutionPacketRecord:
    packet_id: str
    project_id: str
    packet_type: str
    source_execution_contract_id: str
    source_memory_record_ids: tuple[str, ...]
    dependency_ids: tuple[str, ...]
    boundary_level: str
    visibility: str
    execution_mode: str
    payload_summary: str
    node2_projection_summary: str
    created_from: str
    checksum: str
    write_policy: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "project_id": self.project_id,
            "packet_type": self.packet_type,
            "source_execution_contract_id": self.source_execution_contract_id,
            "source_memory_record_ids": list(self.source_memory_record_ids),
            "dependency_ids": list(self.dependency_ids),
            "boundary_level": self.boundary_level,
            "visibility": self.visibility,
            "execution_mode": self.execution_mode,
            "payload_summary": self.payload_summary,
            "node2_projection_summary": self.node2_projection_summary,
            "created_from": self.created_from,
            "checksum": self.checksum,
            "write_policy": self.write_policy,
        }


@dataclass(frozen=True)
class PacketStorePolicy:
    name: str
    read_only: bool
    runtime_write_allowed: bool
    provider_execution_allowed: bool
    mutation_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "read_only": self.read_only,
            "runtime_write_allowed": self.runtime_write_allowed,
            "provider_execution_allowed": self.provider_execution_allowed,
            "mutation_allowed": self.mutation_allowed,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class PacketProjectionRule:
    name: str
    packet_type: str
    node2_surface_allowed: bool
    hidden_payload_blocked: bool
    write_handle_blocked: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "packet_type": self.packet_type,
            "node2_surface_allowed": self.node2_surface_allowed,
            "hidden_payload_blocked": self.hidden_payload_blocked,
            "write_handle_blocked": self.write_handle_blocked,
            "evidence": self.evidence,
        }
