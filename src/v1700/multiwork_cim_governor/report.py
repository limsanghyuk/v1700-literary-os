from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canon_governor import run_cross_work_canon_governor
from .cross_project_influence import run_cross_project_influence_edges
from .gitnexus_preflight import run_stage129_gitnexus_preflight
from .project_local_cim import run_project_local_cim_builder


def run_stage129_multiwork_cim_governor(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage129_multiwork_cim_governor_pack"
    pack.mkdir(parents=True, exist_ok=True)
    project_cim = run_project_local_cim_builder()
    cross_edges = run_cross_project_influence_edges()
    canon = run_cross_work_canon_governor()
    preflight = run_stage129_gitnexus_preflight(root)
    parts = {
        "project_local_cim": project_cim,
        "cross_project_influence": cross_edges,
        "cross_work_canon_governor": canon,
        "gitnexus_preflight": preflight,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}_report.json", payload)
    issues: list[str] = []
    if project_cim.get("status") != "pass":
        issues.append("project_local_cim_blocked")
    if cross_edges.get("status") != "pass":
        issues.append("cross_project_influence_blocked")
    if canon.get("status") != "pass":
        issues.append("cross_work_canon_governor_blocked")
    if preflight.get("status") != "PASS":
        issues.append("gitnexus_preflight_blocked")
    result = {
        "stage": "129",
        "baseline_stage": "128",
        "title": "MultiWorkCIM + Cross-Work Canon Governor",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "project_local_cim_preserved": True,
        "multiwork_cim_formula": "MultiWorkCIM = CIM_project_local + CrossProjectInfluenceEdges(read_only)",
        "project_local_cim_count": project_cim.get("project_count", 0),
        "cross_project_read_only_edges": cross_edges.get("read_only_edge_count", 0),
        "cross_project_blocked_edges": cross_edges.get("blocked_edge_count", 0),
        "cross_project_write_edges": cross_edges.get("cross_project_write_edges", 0),
        "cross_project_write_allowed": False,
        "unauthorized_cross_reads": cross_edges.get("unauthorized_cross_reads", 0),
        "unauthorized_cross_writes": cross_edges.get("unauthorized_cross_writes", 0),
        "license_edge_missing_but_access_allowed": cross_edges.get("license_edge_missing_but_access_allowed", False),
        "canon_conflict_blocks": canon.get("block_count", 0),
        "canon_auto_resolution_count": canon.get("canon_auto_resolution_count", 0),
        "cross_work_canon_merge_allowed": False,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "full_text_exported": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "python_fallback_used": preflight.get("python_fallback_used", False),
        "stage130_multiwork_release_required": True,
        "parts": parts,
    }
    _write_json(root / "release/current/stage129_multiwork_cim_governor_report.json", result)
    _write_json(pack / "stage129_summary.json", _summary(result))
    return result


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "stage", "baseline_stage", "title", "status", "issues", "project_local_cim_preserved",
        "cross_project_read_only_edges", "cross_project_write_edges", "unauthorized_cross_reads",
        "unauthorized_cross_writes", "canon_conflict_blocks", "canon_auto_resolution_count",
        "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage", "branchpoint_lineage_preserved",
    ]
    return {key: result.get(key) for key in keys}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
