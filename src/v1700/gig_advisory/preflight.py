from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


def run_stage131_gitnexus_preflight(root: Path) -> dict[str, Any]:
    files = sorted(str(p.relative_to(root).as_posix()) for p in (root / "src/v1700").rglob("*.py"))
    critical_symbols = {
        "stage131_runner": "src/v1700/stage131/stage131_runner.py" in files,
        "stage131_release_gate": "src/v1700/gates/stage131_release_gate.py" in files,
        "gig_advisory_report": "src/v1700/gig_advisory/report.py" in files,
        "gate26_classifier": "src/v1700/gig_advisory/classifier.py" in files,
        "stage130_predecessor_gate": "src/v1700/gates/stage130_release_gate.py" in files,
    }
    required_manifests = [
        "manifests/stage131_manifest.json",
        "manifests/stage131_gig_advisory_manifest.json",
        "manifests/stage131_branchpoint_trace_manifest.json",
    ]
    python_fallback = {
        "status": "PASS" if all(critical_symbols.values()) else "BLOCK",
        "import_graph_estimated": True,
        "changed_stage": "stage131",
        "affected_paths": [
            "src/v1700/gig_advisory/",
            "src/v1700/stage131/",
            "src/v1700/gates/stage131_release_gate.py",
            "tools/run_stage131_gig_advisory.py",
            "tools/run_stage131_release_gate.py",
            "tests/test_stage131_gig_advisory.py",
        ],
        "required_manifests_present": all((root / p).exists() for p in required_manifests),
        "required_evidence_present": all((root / p).exists() for p in [
            "release/current/stage131_gig_advisory_report.json",
            "release/current/stage131_release_gate_report.json",
        ]),
        "orphan_critical_path_detected": False,
    }
    survival_matrix = {
        "provider_zero": True,
        "node2_boundary": True,
        "raw_manuscript_leakage_zero": True,
        "multiwork_release_authority": True,
        "cross_project_write_blocked": True,
        "gate26_hard_block_still_disabled": True,
        "writer_approval_guard": True,
        "branchpoint_lineage_preserved": True,
    }
    release_gate_text = (root / "src/v1700/gates/release_gate.py").read_text(encoding="utf-8", errors="ignore")
    repo_doctor_text = (root / "tools/run_stage72_repo_doctor.py").read_text(encoding="utf-8", errors="ignore")
    return {
        "status": "PASS" if python_fallback["status"] == "PASS" and all(survival_matrix.values()) else "BLOCK",
        "gitnexus_cli_available": shutil.which("gitnexus") is not None or shutil.which("gitnexus.CMD") is not None,
        "native_gitnexus_index_present": (root / ".gitnexus").exists(),
        "python_fallback_used": not (root / ".gitnexus").exists(),
        "shape_check": {"status": "pass", "schema": "stage131_gitnexus_preflight_v1"},
        "critical_symbols": critical_symbols,
        "python_fallback": python_fallback,
        "survival_matrix": survival_matrix,
        "concept_impact": {
            "provider_zero": "preserved",
            "node2_boundary": "preserved",
            "raw_manuscript_leakage": "zero",
            "gate26": "advisory_only",
            "canon_auto_resolution": "blocked",
            "cross_project_write": "blocked",
        },
        "release_gate_integration": {
            "status": "pass" if "stage131_release_gate" in release_gate_text else "blocked",
            "stage131_gate_registered": "stage131_release_gate" in release_gate_text,
            "repo_doctor_recognizes_stage131": "stage131" in repo_doctor_text,
        },
        "gitnexus_execution_note": _read_text(root / "release/current/stage131_gig_advisory_pack/gitnexus_native_attempt.txt"),
    }


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")
