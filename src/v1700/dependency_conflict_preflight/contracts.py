from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DependencyOrderFinding:
    packet_id: str
    dependency_id: str
    status: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {
            "packet_id": self.packet_id,
            "dependency_id": self.dependency_id,
            "status": self.status,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ConflictRule:
    name: str
    left_packet_type: str
    right_packet_type: str
    blocked: bool
    reason: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "left_packet_type": self.left_packet_type,
            "right_packet_type": self.right_packet_type,
            "blocked": self.blocked,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class BoundaryPreflightRule:
    name: str
    packet_id: str
    boundary_level: str
    status: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "packet_id": self.packet_id,
            "boundary_level": self.boundary_level,
            "status": self.status,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class BlockedOperationRule:
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
class ConnectivityCheck:
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
