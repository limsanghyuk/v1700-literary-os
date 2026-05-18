from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Status = Literal["PASS", "WARN", "BLOCK"]


@dataclass(frozen=True)
class SymbolProbe:
    name: str
    expected_kind: str
    present: bool
    locations: list[str] = field(default_factory=list)
    branchpoints: list[str] = field(default_factory=list)
    required_for_stage112: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FallbackImpactReport:
    status: Status
    python_fallback_used: bool
    import_edges_total: int
    critical_paths_checked: list[str]
    affected_tests: dict[str, list[str]]
    manifests_checked: dict[str, bool]
    release_evidence_checked: dict[str, bool]
    orphan_critical_nodes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConceptImpactReport:
    status: Status
    provider_zero_preserved: bool
    live_provider_call_count_in_release_gate: int
    node2_raw_reveal_access: int
    reader_only_leakage: int
    internal_marker_leakage: int
    raw_manuscript_provider_leakage: int
    credential_leakage: int
    branchpoint_lineage_preserved: bool
    release_gate_integration_required: bool
    repo_doctor_integration_required: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GitNexusPreflightResult:
    stage: str
    baseline_stage: str
    title: str
    status: Status
    issues: list[str]
    repo_id: str
    index_fresh: bool
    stale_index_detected: bool
    gitnexus_sidecar_available: bool
    python_fallback_used: bool
    queried_symbols: list[dict[str, Any]]
    impact_depth_1: dict[str, Any]
    impact_depth_2: dict[str, Any]
    impact_depth_3: dict[str, Any]
    detect_changes: dict[str, Any]
    concept_impact: dict[str, Any]
    survival_matrix: dict[str, bool]
    branchpoint_trace: dict[str, list[str]]
    shape_check_pass: bool
    change_review: dict[str, Any]
    release_gate_integration: dict[str, Any]
    provider_default_calls: int = 0
    live_provider_call_count_in_release_gate: int = 0
    node2_raw_reveal_access: int = 0
    raw_manuscript_provider_leakage: int = 0
    credential_leakage: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

