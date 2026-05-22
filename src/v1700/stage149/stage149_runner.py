from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.body_constitution_release_gate import run_stage149_body_constitution_release_gate


def run_stage149(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage149_body_constitution_release_gate(root)
    summary = {
        "stage": "149",
        "baseline_stage": "148",
        "title": "Body Constitution Release Gate",
        "status": report["status"],
        "main_report": "release/current/stage149_body_constitution_release_gate_report.json",
        "release_gate_report": "release/current/stage149_release_gate_report.json",
        "asset_manifest": "release/current/stage149_release_asset_manifest.json",
        "evidence_pack": "release/current/stage149_body_constitution_release_gate_pack/",
        "mode": report.get("mode"),
        "body_constitution_release_gate_only": report.get("body_constitution_release_gate_only"),
        "gate_rule_count": report.get("gate_rule_count"),
        "sealed_page01": report.get("sealed_page01"),
        "page01_constitution_frozen": report.get("page01_constitution_frozen"),
        "stage150_memory_body_ready": report.get("stage150_memory_body_ready"),
        "release_blocker_count": report.get("release_blocker_count"),
        "blocked_capability_count": report.get("blocked_capability_count"),
        "lineage_evidence_complete": report.get("lineage_evidence_complete"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage150 Memory Body",
            "Stage151 Memory Retrieval Body",
        ],
    }
    _write_json(root / "release/current/stage149_summary.json", summary)
    return {**report, "stage149_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
