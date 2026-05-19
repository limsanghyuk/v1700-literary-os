from __future__ import annotations

from typing import Any

from .contracts import MultiWorkOperationalSurface


def build_multiwork_operational_surface() -> dict[str, Any]:
    surface = MultiWorkOperationalSurface(
        release_id="V1700_STAGE130_MULTIWORK_RELEASE",
        mode="MULTIWORK_RELEASE_READ_ONLY_AUTHORITY",
        enabled_surfaces=(
            "project_isolation_audit",
            "shared_character_read_only_adapter",
            "shared_world_read_only_adapter",
            "project_local_cim",
            "cross_project_influence_edges_read_only",
            "cross_work_canon_governor",
            "multiwork_release_gate_authority",
        ),
        blocked_surfaces=(
            "cross_project_write",
            "raw_manuscript_sharing",
            "direct_v571_trunk_merge",
            "canon_auto_resolution",
            "shared_world_source_of_truth_promotion",
            "gate26_hard_block",
            "active_learning_runtime_mutation",
        ),
        next_stage="Stage131 — GIG / Gate26 Advisory Absorption",
    )
    return {
        "status": "pass",
        "operational_surface": surface.to_dict(),
        "multiwork_release_mode": surface.mode,
        "cross_project_write_allowed": False,
        "raw_manuscript_sharing_allowed": False,
        "stage131_gig_advisory_deferred": True,
    }
