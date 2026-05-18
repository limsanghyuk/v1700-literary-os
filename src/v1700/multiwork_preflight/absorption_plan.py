from __future__ import annotations

from .contracts import MultiWorkAbsorptionPlan


def build_multiwork_absorption_plan() -> dict:
    return MultiWorkAbsorptionPlan(
        next_stage="Stage128 — SharedWorld / SharedCharacter Read-Only Absorption",
        safe_to_absorb_read_only=True,
        blocked_modules=[
            "cross_project_write",
            "raw_manuscript_cross_project_sharing",
            "license_missing_character_reuse",
            "SharedWorldDB_as_source_of_truth",
            "MultiWorkCIM_write_edges",
            "Active_MetaLearner",
            "ASD_real_mutation",
        ],
        adapter_required=[
            "SharedCharacterReadOnlyAdapter",
            "SharedWorldReadOnlyAdapter",
            "AuthorLicenseBoundaryAdapter",
            "ProjectIsolationManagerAdapter",
            "CanonConflictReportAdapter",
        ],
        required_gates=[
            "stage128_read_only_absorption_gate",
            "cross_work_memory_isolation_gate",
            "author_license_boundary_gate",
            "canon_conflict_preflight_gate",
        ],
        required_tests=[
            "tests/test_stage128_shared_character_read_only.py",
            "tests/test_stage128_shared_world_read_only.py",
            "tests/test_stage128_cross_work_isolation.py",
        ],
        required_manifests=[
            "manifests/stage128_manifest.json",
            "manifests/stage128_read_only_absorption_manifest.json",
        ],
    ).to_dict()
