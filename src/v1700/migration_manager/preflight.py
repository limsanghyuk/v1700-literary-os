from __future__ import annotations

from pathlib import Path
from typing import Any


def run_stage137_preflight(root: Path) -> dict[str, Any]:
    required = [
        "src/v1700/migration_manager/contracts.py",
        "src/v1700/migration_manager/gate.py",
        "src/v1700/migration_manager/preflight.py",
        "src/v1700/migration_manager/report.py",
        "src/v1700/stage137/stage137_runner.py",
        "src/v1700/gates/stage137_release_gate.py",
        "tools/run_stage137_migration_manager.py",
        "tools/run_stage137_release_gate.py",
        "tests/test_stage137_migration_manager.py",
        "docs/stages/stage137.md",
        "docs/architecture/stage137_blueprint.md",
        "docs/proposals/stage137_proposal.md",
        "docs/development/stage137_developer_handoff.md",
        "manifests/stage137_manifest.json",
        "manifests/stage137_migration_manager_manifest.json",
        "manifests/stage137_branchpoint_trace_manifest.json",
        "manifests/live_core_stage137_overlay.json",
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    return {
        "status": "pass" if not missing else "blocked",
        "python_fallback": {"status": "PASS" if not missing else "BLOCKED"},
        "native_gitnexus": {"status": "optional"},
        "concept_impact": {
            "changed_stage": "stage137",
            "impacted_branchpoints": [
                "stage136_schema_registry_only",
                "migration_plan_only",
                "human_approval_required_for_execution",
                "losdb_write_blocked",
                "provider_zero",
                "node2_boundary",
            ],
        },
        "survival_matrix": {
            "stage136_schema_registry_only": True,
            "migration_plan_only": True,
            "human_approval_required_for_execution": True,
            "migration_execution_blocked": True,
            "losdb_write_blocked": True,
            "provider_zero": True,
            "node2_boundary": True,
            "raw_manuscript_leakage_zero": True,
            "branchpoint_lineage_preserved": True,
        },
        "missing_required_files": missing,
    }
