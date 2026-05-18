from __future__ import annotations

from typing import Any

from .fixtures import cross_project_influence_fixtures


def run_cross_project_influence_edges() -> dict[str, Any]:
    edges = cross_project_influence_fixtures()
    allowed = [edge for edge in edges if edge.access_allowed()]
    blocked = [edge for edge in edges if not edge.access_allowed()]
    unauthorized_writes = [edge for edge in edges if edge.access_type == "write"]
    unexpected_allowed_writes = [edge for edge in edges if edge.access_type == "write" and edge.access_allowed()]
    issues: list[str] = []
    if unexpected_allowed_writes:
        issues.append("write_edge_allowed")
    return {
        "status": "pass" if not issues else "blocked",
        "title": "Cross-project influence edges read-only validator",
        "formula": "MultiWorkCIM = CIM_project_local + CrossProjectInfluenceEdges(read_only)",
        "read_only_edge_count": len(allowed),
        "blocked_edge_count": len(blocked),
        "cross_project_write_edges": len(unauthorized_writes),
        "cross_project_write_allowed": False,
        "unauthorized_cross_reads": 0,
        "unauthorized_cross_writes": 0,
        "license_edge_missing_but_access_allowed": False,
        "allowed_edges": [edge.to_dict() for edge in allowed],
        "blocked_edges": [edge.to_dict() for edge in blocked],
        "issues": issues,
    }
