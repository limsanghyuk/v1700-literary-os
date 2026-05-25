from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DryRunTraceStep:
    trace_id: str
    step_index: int
    packet_id: str
    node_id: str
    packet_type: str
    boundary_level: str
    dependency_ids: tuple[str, ...]
    dry_run_action: str
    status: str
    node2_projection_summary: str
    checksum: str

    def to_dict(self) -> dict[str, object]:
        return {
            "trace_id": self.trace_id,
            "step_index": self.step_index,
            "packet_id": self.packet_id,
            "node_id": self.node_id,
            "packet_type": self.packet_type,
            "boundary_level": self.boundary_level,
            "dependency_ids": list(self.dependency_ids),
            "dry_run_action": self.dry_run_action,
            "status": self.status,
            "node2_projection_summary": self.node2_projection_summary,
            "checksum": self.checksum,
        }


@dataclass(frozen=True)
class DryRunPolicyRule:
    name: str
    enabled: bool
    must_remain_disabled: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "enabled": self.enabled,
            "must_remain_disabled": self.must_remain_disabled,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class TraceConnectivityCheck:
    name: str
    path: str
    required: bool
    exists: bool

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "path": self.path,
            "required": self.required,
            "exists": self.exists,
        }
