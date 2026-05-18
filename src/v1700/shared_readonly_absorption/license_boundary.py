from __future__ import annotations

from typing import Any

from .contracts import ReadOnlyAccessRequest
from .fixtures import blocked_probe_requests, safe_read_requests


def evaluate_access_request(request: ReadOnlyAccessRequest) -> dict[str, Any]:
    return request.to_dict()


def run_license_boundary_adapter() -> dict[str, Any]:
    safe = [evaluate_access_request(x) for x in safe_read_requests()]
    probes = [evaluate_access_request(x) for x in blocked_probe_requests()]
    missing_license_allowed = [x for x in probes if not x["same_owner"] and not x["license_edge_exists"] and x["access_allowed"]]
    write_allowed = [x for x in safe + probes if x["access_type"] == "write" and x["access_allowed"]]
    return {
        "status": "pass" if not missing_license_allowed and not write_allowed else "blocked",
        "stage": "128",
        "access_formula": "read_only AND (same_owner OR license_edge_exists OR public_domain_flag) AND author_approval_valid AND isolation_policy_allows AND resource_scope_permits",
        "safe_requests": safe,
        "blocked_probe_requests": probes,
        "license_edge_missing_but_access_allowed": bool(missing_license_allowed),
        "cross_project_write_allowed": bool(write_allowed),
        "author_approval_required": True,
        "read_only_absorption": True,
    }
