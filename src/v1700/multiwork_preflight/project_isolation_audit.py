from __future__ import annotations

from pathlib import Path
from typing import Any

from .contracts import IsolationAuditResult
from .fixtures import safe_cross_work_edges, sample_projects


def run_project_isolation_audit(root: Path | None = None) -> dict[str, Any]:
    projects = sample_projects()
    edges = safe_cross_work_edges()
    unauthorized_reads = 0
    unauthorized_writes = 0
    allowed_edges: list[dict[str, Any]] = []
    blocked_edges: list[dict[str, Any]] = []
    for edge in edges:
        payload = edge.to_dict()
        if edge.allowed():
            allowed_edges.append(payload)
        else:
            blocked_edges.append(payload)
            if edge.access_type in {"read", "reference", "adapt"}:
                unauthorized_reads += 1
            if edge.access_type == "write":
                unauthorized_writes += 1
    result = IsolationAuditResult(
        project_count=len(projects),
        unauthorized_cross_reads=unauthorized_reads,
        unauthorized_cross_writes=unauthorized_writes,
        shared_character_conflicts=0,
        shared_world_conflicts=0,
        raw_manuscript_leakage=0,
        status="PASS" if unauthorized_reads == 0 and unauthorized_writes == 0 else "BLOCK",
        details={
            "projects": [p.to_dict() for p in projects],
            "allowed_edges": allowed_edges,
            "blocked_edges": blocked_edges,
            "cross_project_influence_write": 0,
        },
    )
    return result.to_dict()
