from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

ImpactRole = Literal[
    "engine",
    "gate",
    "manifest",
    "tool",
    "test",
    "release_evidence",
    "boundary",
    "export",
]
Criticality = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
ImpactEdgeType = Literal[
    "imports",
    "calls",
    "writes_evidence",
    "reads_evidence",
    "guards",
    "validates",
    "declares",
    "traces_branchpoint",
    "blocks_release",
]


@dataclass(frozen=True)
class ImpactNode:
    node_id: str
    path: str
    symbol: str
    stage_origin: str
    role: ImpactRole
    criticality: Criticality

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ImpactEdge:
    source_node_id: str
    target_node_id: str
    edge_type: ImpactEdgeType
    confidence: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ImpactReport:
    stage: str
    baseline_stage: str
    nodes_total: int
    edges_total: int
    critical_nodes_total: int
    orphan_nodes: list[str]
    broken_edges: list[str]
    stale_manifests: list[str]
    untraced_new_logic: list[str]
    branchpoint_survival_status: str
    release_blockers: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
