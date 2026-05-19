from __future__ import annotations

from typing import Any

from .contracts import MultiWorkReleaseSeal


def seal_multiwork_release(matrix: dict[str, Any], surface: dict[str, Any], preflight: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    if matrix.get("status") != "pass":
        issues.append("release_matrix_blocked")
    if surface.get("status") != "pass":
        issues.append("operational_surface_blocked")
    if preflight.get("status") != "PASS":
        issues.append("gitnexus_preflight_blocked")
    matrix_data = matrix.get("matrix", {})
    seal = MultiWorkReleaseSeal(
        status="pass" if not issues else "blocked",
        stage="130",
        baseline_stage="129",
        release_authority="Stage130 MultiWork Release Gate",
        stage127_to_stage129_evidence_preserved=matrix_data.get("evidence_complete") is True,
        multiwork_release_authorized=not issues,
        stage131_gig_advisory_deferred=surface.get("stage131_gig_advisory_deferred") is True,
        provider_zero_preserved=matrix_data.get("provider_default_calls") == 0,
        node2_boundary_preserved=matrix_data.get("node2_raw_reveal_access") == 0,
        raw_manuscript_boundary_preserved=matrix_data.get("raw_manuscript_cross_project_leakage") == 0,
        branchpoint_lineage_preserved=all(preflight.get("survival_matrix", {}).values()),
    )
    return {"status": seal.status, "issues": issues, "seal": seal.to_dict()}
