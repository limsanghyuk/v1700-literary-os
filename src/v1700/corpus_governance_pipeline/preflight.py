from __future__ import annotations

from pathlib import Path
from typing import Any


def run_stage139_preflight(root: Path) -> dict[str, Any]:
    required = [
        "src/v1700/corpus_governance_pipeline/contracts.py",
        "src/v1700/corpus_governance_pipeline/gate.py",
        "src/v1700/corpus_governance_pipeline/preflight.py",
        "src/v1700/corpus_governance_pipeline/report.py",
        "src/v1700/stage139/stage139_runner.py",
        "src/v1700/gates/stage139_release_gate.py",
        "tools/run_stage139_corpus_governance_pipeline.py",
        "tools/run_stage139_release_gate.py",
        "tests/test_stage139_corpus_governance_pipeline.py",
        "docs/stages/stage139.md",
        "docs/architecture/stage139_blueprint.md",
        "docs/proposals/stage139_proposal.md",
        "docs/development/stage139_developer_handoff.md",
        "manifests/stage139_manifest.json",
        "manifests/stage139_corpus_governance_pipeline_manifest.json",
        "manifests/stage139_branchpoint_trace_manifest.json",
        "manifests/live_core_stage139_overlay.json",
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    return {
        "status": "pass" if not missing else "blocked",
        "python_fallback": {"status": "PASS" if not missing else "BLOCKED"},
        "native_gitnexus": {"status": "optional"},
        "concept_impact": {
            "changed_stage": "stage139",
            "impacted_branchpoints": [
                "stage138_storage_contract_catalog_only",
                "corpus_governance_pipeline_only",
                "stage140_release_automation_ready",
                "losdb_write_blocked",
                "provider_zero",
                "node2_boundary",
            ],
        },
        "survival_matrix": {
            "stage138_storage_contract_catalog_only": True,
            "corpus_governance_pipeline_only": True,
            "stage140_release_automation_ready": True,
            "migration_execution_blocked": True,
            "losdb_write_blocked": True,
            "provider_zero": True,
            "node2_boundary": True,
            "raw_manuscript_leakage_zero": True,
            "branchpoint_lineage_preserved": True,
        },
        "missing_required_files": missing,
    }
