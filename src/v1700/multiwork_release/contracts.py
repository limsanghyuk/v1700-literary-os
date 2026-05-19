from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

Status = Literal["pass", "blocked", "warn"]


@dataclass(frozen=True)
class StageEvidence:
    stage: str
    title: str
    status: Status
    report_path: str
    release_gate_path: str
    required_for_release: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MultiWorkReleaseMatrix:
    stage: str
    baseline_stage: str
    stage127_preflight_pass: bool
    stage128_read_only_absorption_pass: bool
    stage129_cim_governor_pass: bool
    direct_v571_merge_detected: bool
    cross_project_write_allowed: bool
    unauthorized_cross_reads: int
    unauthorized_cross_writes: int
    raw_manuscript_cross_project_leakage: int
    canon_auto_resolution_count: int
    provider_default_calls: int
    node2_raw_reveal_access: int
    evidence_complete: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MultiWorkOperationalSurface:
    release_id: str
    mode: Literal["MULTIWORK_RELEASE_READ_ONLY_AUTHORITY"]
    enabled_surfaces: tuple[str, ...]
    blocked_surfaces: tuple[str, ...]
    next_stage: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MultiWorkReleaseSeal:
    status: Status
    stage: str
    baseline_stage: str
    release_authority: str
    stage127_to_stage129_evidence_preserved: bool
    multiwork_release_authorized: bool
    stage131_gig_advisory_deferred: bool
    provider_zero_preserved: bool
    node2_boundary_preserved: bool
    raw_manuscript_boundary_preserved: bool
    branchpoint_lineage_preserved: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
