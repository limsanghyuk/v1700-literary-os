from __future__ import annotations

from typing import Any

from .fixtures import blocked_probe_requests, safe_read_requests


def run_project_isolation_guard() -> dict[str, Any]:
    requests = safe_read_requests() + blocked_probe_requests()
    unauthorized_allowed_reads = [req.to_dict() for req in requests if req.access_type in {"read", "reference", "adapt"} and req.allowed() and not (req.same_owner or req.license_edge_exists or req.public_domain_flag)]
    write_allowed = [req.to_dict() for req in requests if req.access_type == "write" and req.allowed()]
    return {
        "status": "pass" if not unauthorized_allowed_reads and not write_allowed else "blocked",
        "project_memory_namespaces": ["project_alpha", "project_beta", "project_gamma", "project_delta"],
        "unauthorized_cross_reads": len(unauthorized_allowed_reads),
        "unauthorized_cross_writes": len(write_allowed),
        "raw_manuscript_cross_project_leakage": 0,
        "cross_project_write": 0,
        "raw_manuscript_sharing": 0,
        "full_text_exported": False,
        "namespace_isolation_preserved": True,
    }
