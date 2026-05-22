from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.project_manifest_body import run_stage147_project_manifest_body


def run_stage147(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage147_project_manifest_body(root)
    summary = {
        "stage": "147",
        "baseline_stage": "146",
        "title": "Project Manifest Body",
        "status": report["status"],
        "main_report": "release/current/stage147_project_manifest_body_report.json",
        "release_gate_report": "release/current/stage147_release_gate_report.json",
        "asset_manifest": "release/current/stage147_release_asset_manifest.json",
        "evidence_pack": "release/current/stage147_project_manifest_body_pack/",
        "mode": report.get("mode"),
        "project_manifest_body_only": report.get("project_manifest_body_only"),
        "manifest_section_count": report.get("manifest_section_count"),
        "canonical_packet_count": report.get("canonical_packet_count"),
        "state_binding_count": report.get("state_binding_count"),
        "policy_boundary_complete": report.get("policy_boundary_complete"),
        "load_order_complete": report.get("load_order_complete"),
        "node_boundary_constitution_ready": report.get("node_boundary_constitution_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage148 Node Boundary Constitution",
            "Stage149 Body Constitution Release Gate",
            "Stage150 Memory Body",
        ],
    }
    _write_json(root / "release/current/stage147_summary.json", summary)
    return {**report, "stage147_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
