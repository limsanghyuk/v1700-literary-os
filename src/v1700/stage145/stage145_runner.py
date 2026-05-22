from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.body_constitution import run_stage145_body_constitution


def run_stage145(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage145_body_constitution(root)
    summary = {
        "stage": "145",
        "baseline_stage": "144",
        "title": "Body Constitution",
        "status": report["status"],
        "main_report": "release/current/stage145_body_constitution_report.json",
        "release_gate_report": "release/current/stage145_release_gate_report.json",
        "asset_manifest": "release/current/stage145_release_asset_manifest.json",
        "evidence_pack": "release/current/stage145_body_constitution_pack/",
        "mode": report.get("mode"),
        "body_constitution_only": report.get("body_constitution_only"),
        "formula_policy": report.get("formula_policy"),
        "formula_policy_complete": report.get("formula_policy_complete"),
        "body_layer_count": report.get("body_layer_count"),
        "stage150_memory_body_ready": report.get("stage150_memory_body_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage146 Narrative State Contract",
            "Stage147 Project Manifest Body",
            "Stage148 Node Boundary Constitution",
            "Stage149 Body Constitution Release Gate",
        ],
    }
    _write_json(root / "release/current/stage145_summary.json", summary)
    return {**report, "stage145_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
