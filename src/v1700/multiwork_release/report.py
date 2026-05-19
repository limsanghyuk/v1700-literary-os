from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .gitnexus_preflight import run_stage130_gitnexus_preflight
from .operational_surface import build_multiwork_operational_surface
from .release_matrix import build_stage130_release_matrix
from .release_seal import seal_multiwork_release


def run_stage130_multiwork_release(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage130_multiwork_release_pack"
    pack.mkdir(parents=True, exist_ok=True)
    matrix = build_stage130_release_matrix(root)
    surface = build_multiwork_operational_surface()
    preflight = run_stage130_gitnexus_preflight(root)
    seal = seal_multiwork_release(matrix, surface, preflight)
    parts = {
        "release_matrix": matrix,
        "operational_surface": surface,
        "gitnexus_preflight": preflight,
        "release_seal": seal,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}_report.json", payload)
    issues: list[str] = []
    for key, payload in parts.items():
        ok_status = "PASS" if key == "gitnexus_preflight" else "pass"
        if payload.get("status") != ok_status:
            issues.append(f"{key}_blocked")
    result = {
        "stage": "130",
        "baseline_stage": "129",
        "title": "MultiWork Release",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "multiwork_release_authorized": seal.get("seal", {}).get("multiwork_release_authorized", False),
        "multiwork_release_mode": surface.get("multiwork_release_mode"),
        "stage127_to_stage129_evidence_preserved": seal.get("seal", {}).get("stage127_to_stage129_evidence_preserved", False),
        "stage127_preflight_pass": matrix.get("matrix", {}).get("stage127_preflight_pass", False),
        "stage128_read_only_absorption_pass": matrix.get("matrix", {}).get("stage128_read_only_absorption_pass", False),
        "stage129_cim_governor_pass": matrix.get("matrix", {}).get("stage129_cim_governor_pass", False),
        "direct_v571_merge_detected": matrix.get("matrix", {}).get("direct_v571_merge_detected", True),
        "cross_project_write_allowed": False,
        "unauthorized_cross_reads": matrix.get("matrix", {}).get("unauthorized_cross_reads", 0),
        "unauthorized_cross_writes": matrix.get("matrix", {}).get("unauthorized_cross_writes", 0),
        "raw_manuscript_cross_project_leakage": matrix.get("matrix", {}).get("raw_manuscript_cross_project_leakage", 0),
        "raw_manuscript_provider_leakage": 0,
        "full_text_exported": False,
        "canon_auto_resolution_count": matrix.get("matrix", {}).get("canon_auto_resolution_count", 0),
        "shared_world_source_of_truth_promoted": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": seal.get("seal", {}).get("branchpoint_lineage_preserved", False),
        "python_fallback_used": preflight.get("python_fallback_used", False),
        "stage131_gig_advisory_required": True,
        "gate26_hard_block_enabled": False,
        "parts": parts,
    }
    _write_json(root / "release/current/stage130_multiwork_release_report.json", result)
    _write_json(pack / "stage130_summary.json", _summary(result))
    return result


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "stage", "baseline_stage", "title", "status", "issues", "multiwork_release_authorized",
        "stage127_to_stage129_evidence_preserved", "cross_project_write_allowed",
        "unauthorized_cross_reads", "unauthorized_cross_writes", "raw_manuscript_cross_project_leakage",
        "canon_auto_resolution_count", "provider_default_calls", "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access", "branchpoint_lineage_preserved", "stage131_gig_advisory_required",
    ]
    return {key: result.get(key) for key in keys}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
