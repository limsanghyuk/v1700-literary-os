from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SymbolTraceEntry:
    branchpoint_id: str
    priority: str
    concept: str
    runtime_status: str
    code_symbols: tuple[str, ...]
    evidence_files: tuple[str, ...]
    tests: tuple[str, ...]
    gates: tuple[str, ...]
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "branchpoint_id": self.branchpoint_id,
            "priority": self.priority,
            "concept": self.concept,
            "runtime_status": self.runtime_status,
            "code_symbols": list(self.code_symbols),
            "evidence_files": list(self.evidence_files),
            "tests": list(self.tests),
            "gates": list(self.gates),
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class IndexQualityThresholds:
    min_files: int = 300
    min_nodes: int = 3000
    min_edges: int = 5000
    min_clusters: int = 30
    min_flows: int = 100
    min_p0_coverage: float = 1.0
    min_p1_coverage: float = 0.8

    def to_dict(self) -> dict[str, Any]:
        return {
            "min_files": self.min_files,
            "min_nodes": self.min_nodes,
            "min_edges": self.min_edges,
            "min_clusters": self.min_clusters,
            "min_flows": self.min_flows,
            "min_p0_coverage": self.min_p0_coverage,
            "min_p1_coverage": self.min_p1_coverage,
        }


@dataclass(frozen=True)
class IndexQualityMetrics:
    files: int
    nodes: int
    edges: int
    clusters: int
    flows: int
    embeddings: int

    def ratios(self) -> dict[str, float]:
        files = max(self.files, 1)
        nodes = max(self.nodes, 1)
        return {
            "nodes_per_file": round(self.nodes / files, 3),
            "edges_per_node": round(self.edges / nodes, 3),
            "clusters_per_100_files": round((self.clusters / files) * 100, 3),
            "flows_per_100_files": round((self.flows / files) * 100, 3),
        }

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "files": self.files,
            "nodes": self.nodes,
            "edges": self.edges,
            "clusters": self.clusters,
            "flows": self.flows,
            "embeddings": self.embeddings,
        }
        payload.update(self.ratios())
        return payload

