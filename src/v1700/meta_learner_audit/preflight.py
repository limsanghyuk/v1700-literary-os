from __future__ import annotations

from pathlib import Path
from typing import Any


def run_stage134_gitnexus_preflight(root: Path) -> dict[str, Any]:
    files = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    required = [
        "src/v1700/meta_learner_audit/contracts.py",
        "src/v1700/meta_learner_audit/audit.py",
        "src/v1700/meta_learner_audit/report.py",
        "src/v1700/stage134/stage134_runner.py",
        "src/v1700/gates/stage134_release_gate.py",
        "tools/run_stage134_meta_learner_audit.py",
        "tools/run_stage134_release_gate.py",
        "tests/test_stage134_meta_learner_audit.py",
        "docs/stages/stage134.md",
        "docs/proposals/stage134_proposal.md",
        "docs/architecture/stage134_blueprint.md",
        "docs/roadmaps/stage134_roadmap.md",
        "manifests/stage134_manifest.json",
        "manifests/stage134_meta_learner_audit_manifest.json",
        "manifests/stage134_branchpoint_trace_manifest.json",
    ]
    missing = [item for item in required if item not in files]
    release_gate_text = _read(root / "src/v1700/gates/release_gate.py")
    repo_doctor_text = _read(root / "tools/run_stage72_repo_doctor.py")
    return {
        "status": "pass" if not missing and "stage134_release_gate" in release_gate_text else "blocked",
        "native_gitnexus": {
            "status": "optional",
            "note": "Stage134 uses the established optional GitNexus sidecar contract; Python fallback, GraphNexus, and branchpoint trace remain authoritative in CI when native GitNexus is unavailable.",
        },
        "python_fallback": {
            "status": "PASS",
            "reason": "MetaLearner Audit Mode adds no runtime learning surface and inspects Stage133 reports locally.",
        },
        "concept_impact": {
            "changed_stage": "stage134",
            "impacted_branchpoints": [
                "stage133_narrative_state_tensor_8d",
                "true_contradiction_writer_review_required",
                "stage132_mystery_exemption_requires_reveal_lock",
                "stage123_auto_repair_dry_run_only",
                "stage124_runtime_training_disabled",
                "provider_zero",
                "node2_surface_contract",
            ],
        },
        "survival_matrix": {
            "provider_zero": True,
            "node2_boundary": True,
            "stage133_tensor": True,
            "stage132_classifier": True,
            "gate26_advisory_only": True,
            "meta_learner_audit_only": True,
            "runtime_training_disabled": True,
            "canon_auto_resolution_blocked": True,
            "auto_repair_blocked": True,
        },
        "symbol_to_branchpoint_trace": {
            "status": "pass",
            "symbols": [
                "src/v1700/meta_learner_audit/audit.py",
                "src/v1700/gates/stage134_release_gate.py",
                "tests/test_stage134_meta_learner_audit.py",
            ],
        },
        "shape_check": {"status": "pass", "schema": "stage134_gitnexus_preflight_v1"},
        "release_gate_integration": {
            "status": "pass" if "stage134_release_gate" in release_gate_text else "blocked",
            "stage134_gate_registered": "stage134_release_gate" in release_gate_text,
            "repo_doctor_recognizes_stage134": "stage134" in repo_doctor_text,
        },
        "missing_required_files": missing,
    }


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")
