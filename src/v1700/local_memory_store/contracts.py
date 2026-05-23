from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalMemoryStoreSpec:
    name: str
    path: str
    format: str
    mode: str
    source_contract: str
    write_enabled: bool

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "path": self.path,
            "format": self.format,
            "mode": self.mode,
            "source_contract": self.source_contract,
            "write_enabled": self.write_enabled,
        }


@dataclass(frozen=True)
class StoreRecordValidation:
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
class StoreIndexEntry:
    record_id: str
    record_type: str
    source_state_id: str
    boundary_level: str
    node2_projection: str
    checksum: str

    def to_dict(self) -> dict[str, str]:
        return {
            "record_id": self.record_id,
            "record_type": self.record_type,
            "source_state_id": self.source_state_id,
            "boundary_level": self.boundary_level,
            "node2_projection": self.node2_projection,
            "checksum": self.checksum,
        }


@dataclass(frozen=True)
class ReadOnlyAccessRule:
    name: str
    description: str
    read_allowed: bool
    write_allowed: bool
    mutation_allowed: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "read_allowed": self.read_allowed,
            "write_allowed": self.write_allowed,
            "mutation_allowed": self.mutation_allowed,
            "evidence": self.evidence,
        }
