from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.node_boundary_constitution import run_stage148_node_boundary_constitution


def run_stage148(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage148_node_boundary_constitution(root)
    summary = {
        "stage": "148",
        "baseline_stage": "147",
        "title": "Node Boundary Constitution",
        "status": report["status"],
        "main_report": "release/current/stage148_node_boundary_constitution_report.json",
        "release_gate_report": "release/current/stage148_release_gate_report.json",
        "asset_manifest": "release/current/stage148_release_asset_manifest.json",
        "evidence_pack": "release/current/stage148_node_boundary_constitution_pack/",
        "mode": report.get("mode"),
        "node_boundary_constitution_only": report.get("node_boundary_constitution_only"),
        "authority_rule_count": report.get("authority_rule_count"),
        "route_count": report.get("route_count"),
        "projection_rule_count": report.get("projection_rule_count"),
        "node2_surface_only_enforced": report.get("node2_surface_only_enforced"),
        "node3_critic_scope_defined": report.get("node3_critic_scope_defined"),
        "stage149_gate_ready": report.get("stage149_gate_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage149 Body Constitution Release Gate",
            "Stage150 Memory Body",
        ],
    }
    _write_json(root / "release/current/stage148_summary.json", summary)
    return {**report, "stage148_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
