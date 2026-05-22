from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.narrative_state import run_stage146_narrative_state_contract


def run_stage146(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage146_narrative_state_contract(root)
    summary = {
        "stage": "146",
        "baseline_stage": "145",
        "title": "Narrative State Contract",
        "status": report["status"],
        "main_report": "release/current/stage146_narrative_state_contract_report.json",
        "release_gate_report": "release/current/stage146_release_gate_report.json",
        "asset_manifest": "release/current/stage146_release_asset_manifest.json",
        "evidence_pack": "release/current/stage146_narrative_state_contract_pack/",
        "mode": report.get("mode"),
        "narrative_state_contract_only": report.get("narrative_state_contract_only"),
        "canonical_state_object_count": report.get("canonical_state_object_count"),
        "hierarchy_edge_count": report.get("hierarchy_edge_count"),
        "continuity_rule_count": report.get("continuity_rule_count"),
        "reveal_boundary_complete": report.get("reveal_boundary_complete"),
        "project_manifest_body_ready": report.get("project_manifest_body_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage147 Project Manifest Body",
            "Stage148 Node Boundary Constitution",
            "Stage149 Body Constitution Release Gate",
            "Stage150 Memory Body",
        ],
    }
    _write_json(root / "release/current/stage146_summary.json", summary)
    return {**report, "stage146_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
