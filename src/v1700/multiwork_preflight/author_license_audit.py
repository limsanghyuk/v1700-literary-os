from __future__ import annotations

from typing import Any

from .fixtures import blocked_probe_edges, safe_cross_work_edges


def run_author_license_audit() -> dict[str, Any]:
    safe = [edge.to_dict() for edge in safe_cross_work_edges()]
    blocked = [edge.to_dict() for edge in blocked_probe_edges()]
    missing_license_allowed = [edge for edge in blocked if not edge["license_edge_exists"] and edge["access_allowed"]]
    write_allowed = [edge for edge in blocked + safe if edge["access_type"] == "write" and edge["access_allowed"]]
    return {
        "status": "pass" if not missing_license_allowed and not write_allowed else "blocked",
        "access_formula": "license_edge_exists AND isolation_policy_allows AND resource_scope_permits AND author_approval_valid",
        "safe_edges": safe,
        "blocked_probe_edges": blocked,
        "license_edge_missing_but_access_allowed": bool(missing_license_allowed),
        "cross_project_write_allowed": bool(write_allowed),
        "author_approval_required": True,
    }
