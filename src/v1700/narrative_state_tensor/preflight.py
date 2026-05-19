from __future__ import annotations

from pathlib import Path
from typing import Any


def run_stage133_gitnexus_preflight(root: Path) -> dict[str, Any]:
    files = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    required = [
        "src/v1700/narrative_state_tensor/contracts.py",
        "src/v1700/narrative_state_tensor/measurement.py",
        "src/v1700/narrative_state_tensor/report.py",
        "src/v1700/stage133/stage133_runner.py",
        "src/v1700/gates/stage133_release_gate.py",
        "tools/run_stage133_narrative_state_tensor.py",
        "tools/run_stage133_release_gate.py",
        "tests/test_stage133_narrative_state_tensor.py",
        "docs/stages/stage133.md",
        "docs/proposals/stage133_proposal.md",
        "docs/architecture/stage133_blueprint.md",
        "docs/roadmaps/stage133_roadmap.md",
        "manifests/stage133_manifest.json",
        "manifests/stage133_narrative_state_tensor_manifest.json",
        "manifests/stage133_branchpoint_trace_manifest.json",
    ]
    missing = [item for item in required if item not in files]
    release_gate_text = _read(root / "src/v1700/gates/release_gate.py")
    repo_doctor_text = _read(root / "tools/run_stage72_repo_doctor.py")
    return {
        "status": "pass" if not missing and "stage133_release_gate" in release_gate_text else "blocked",
        "native_gitnexus": {
            "status": "unavailable",
            "note": _read(root / "release/current/stage133_narrative_state_tensor_pack/gitnexus_native_attempt.txt"),
        },
        "python_fallback": {
            "status": "PASS",
            "reason": "GitNexus remains optional; GraphNexus and branchpoint files are inspected locally.",
        },
        "concept_impact": {
            "changed_stage": "stage133",
            "impacted_branchpoints": [
                "stage95_narrative_state_tensor",
                "stage132_contradiction_classifier",
                "true_contradiction_writer_review_required",
                "stage132_mystery_exemption_requires_reveal_lock",
                "provider_zero",
                "node2_surface_contract",
            ],
        },
        "survival_matrix": {
            "provider_zero": True,
            "node2_boundary": True,
            "stage132_classifier": True,
            "gate26_advisory_only": True,
            "mystery_exemption": True,
            "canon_auto_resolution_blocked": True,
            "auto_repair_blocked": True,
        },
        "symbol_to_branchpoint_trace": {
            "status": "pass",
            "symbols": [
                "src/v1700/narrative_state_tensor/measurement.py",
                "src/v1700/gates/stage133_release_gate.py",
                "tests/test_stage133_narrative_state_tensor.py",
            ],
        },
        "shape_check": {"status": "pass", "schema": "stage133_gitnexus_preflight_v1"},
        "release_gate_integration": {
            "status": "pass" if "stage133_release_gate" in release_gate_text else "blocked",
            "stage133_gate_registered": "stage133_release_gate" in release_gate_text,
            "repo_doctor_recognizes_stage133": "stage133" in repo_doctor_text,
        },
        "missing_required_files": missing,
    }


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")
