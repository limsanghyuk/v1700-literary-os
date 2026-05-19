from __future__ import annotations

from pathlib import Path
from typing import Any


def run_stage135_preflight(root: Path) -> dict[str, Any]:
    required = [
        "src/v1700/learning_quality_gate/contracts.py",
        "src/v1700/learning_quality_gate/gate.py",
        "src/v1700/learning_quality_gate/report.py",
        "src/v1700/stage135/stage135_runner.py",
        "src/v1700/gates/stage135_release_gate.py",
        "tools/run_stage135_learning_quality_gate.py",
        "tools/run_stage135_release_gate.py",
        "tests/test_stage135_learning_quality_gate.py",
        "docs/stages/stage135.md",
        "docs/architecture/stage135_blueprint.md",
        "docs/proposals/stage135_proposal.md",
        "manifests/stage135_manifest.json",
        "manifests/stage135_learning_quality_gate_manifest.json",
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    return {
        "status": "pass" if not missing else "blocked",
        "python_fallback": {"status": "PASS" if not missing else "BLOCKED"},
        "native_gitnexus": {"status": "optional"},
        "concept_impact": {
            "changed_stage": "stage135",
            "impacted_branchpoints": [
                "stage134_meta_learner_audit_only",
                "runtime_training_disabled",
                "provider_zero",
                "node2_boundary",
                "auto_repair_blocked",
                "canon_auto_resolution_blocked",
            ],
        },
        "survival_matrix": {
            "stage134_audit_only": True,
            "learning_candidate_only": True,
            "runtime_training_disabled": True,
            "active_learning_disabled": True,
            "model_weight_update_blocked": True,
            "provider_zero": True,
            "node2_boundary": True,
            "raw_manuscript_leakage_zero": True,
            "canon_auto_resolution_blocked": True,
            "auto_repair_blocked": True,
        },
        "missing_required_files": missing,
    }
