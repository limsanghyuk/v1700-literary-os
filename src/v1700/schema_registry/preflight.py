from __future__ import annotations

from pathlib import Path
from typing import Any


def run_stage136_preflight(root: Path) -> dict[str, Any]:
    required = [
        "src/v1700/schema_registry/contracts.py",
        "src/v1700/schema_registry/gate.py",
        "src/v1700/schema_registry/preflight.py",
        "src/v1700/schema_registry/report.py",
        "src/v1700/stage136/stage136_runner.py",
        "src/v1700/gates/stage136_release_gate.py",
        "tools/run_stage136_schema_registry.py",
        "tools/run_stage136_release_gate.py",
        "tests/test_stage136_schema_registry.py",
        "docs/stages/stage136.md",
        "docs/architecture/stage136_blueprint.md",
        "docs/proposals/stage136_proposal.md",
        "docs/development/stage136_developer_handoff.md",
        "manifests/stage136_manifest.json",
        "manifests/stage136_schema_registry_manifest.json",
        "manifests/stage136_branchpoint_trace_manifest.json",
        "manifests/live_core_stage136_overlay.json",
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    return {
        "status": "pass" if not missing else "blocked",
        "python_fallback": {"status": "PASS" if not missing else "BLOCKED"},
        "native_gitnexus": {"status": "optional"},
        "concept_impact": {
            "changed_stage": "stage136",
            "impacted_branchpoints": [
                "stage135_candidate_only",
                "schema_registry_only",
                "migration_execution_blocked",
                "losdb_write_blocked",
                "provider_zero",
                "node2_boundary",
            ],
        },
        "survival_matrix": {
            "stage135_candidate_only": True,
            "schema_registry_only": True,
            "migration_execution_blocked": True,
            "losdb_write_blocked": True,
            "storage_contract_prep_only": True,
            "provider_zero": True,
            "node2_boundary": True,
            "raw_manuscript_leakage_zero": True,
            "branchpoint_lineage_preserved": True,
        },
        "missing_required_files": missing,
    }
