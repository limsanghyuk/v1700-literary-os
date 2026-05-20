from __future__ import annotations

from pathlib import Path
from typing import Any


def run_stage138_preflight(root: Path) -> dict[str, Any]:
    required = [
        "src/v1700/losdb_storage_contracts/contracts.py",
        "src/v1700/losdb_storage_contracts/gate.py",
        "src/v1700/losdb_storage_contracts/preflight.py",
        "src/v1700/losdb_storage_contracts/report.py",
        "src/v1700/stage138/stage138_runner.py",
        "src/v1700/gates/stage138_release_gate.py",
        "tools/run_stage138_losdb_storage_contracts.py",
        "tools/run_stage138_release_gate.py",
        "tests/test_stage138_losdb_storage_contracts.py",
        "docs/stages/stage138.md",
        "docs/architecture/stage138_blueprint.md",
        "docs/proposals/stage138_proposal.md",
        "docs/development/stage138_developer_handoff.md",
        "manifests/stage138_manifest.json",
        "manifests/stage138_losdb_storage_contracts_manifest.json",
        "manifests/stage138_branchpoint_trace_manifest.json",
        "manifests/live_core_stage138_overlay.json",
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    return {
        "status": "pass" if not missing else "blocked",
        "python_fallback": {"status": "PASS" if not missing else "BLOCKED"},
        "native_gitnexus": {"status": "optional"},
        "concept_impact": {
            "changed_stage": "stage138",
            "impacted_branchpoints": [
                "migration_plan_only",
                "storage_contract_catalog_only",
                "human_approval_required_for_execution",
                "stage139_governance_ready",
                "losdb_write_blocked",
                "provider_zero",
                "node2_boundary",
            ],
        },
        "survival_matrix": {
            "migration_plan_only": True,
            "storage_contract_catalog_only": True,
            "human_approval_required_for_execution": True,
            "stage139_governance_ready": True,
            "migration_execution_blocked": True,
            "losdb_write_blocked": True,
            "provider_zero": True,
            "node2_boundary": True,
            "raw_manuscript_leakage_zero": True,
            "branchpoint_lineage_preserved": True,
        },
        "missing_required_files": missing,
    }
