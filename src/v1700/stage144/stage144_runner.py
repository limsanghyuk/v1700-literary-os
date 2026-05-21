from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.split_ci_runtime_strategy import run_stage144_split_ci_runtime_strategy


def run_stage144(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage144_split_ci_runtime_strategy(root)
    summary = {
        "stage": "144",
        "baseline_stage": "143",
        "title": "Split CI Runtime Strategy",
        "status": report["status"],
        "main_report": "release/current/stage144_split_ci_runtime_strategy_report.json",
        "release_gate_report": "release/current/stage144_release_gate_report.json",
        "asset_manifest": "release/current/stage144_release_asset_manifest.json",
        "evidence_pack": "release/current/stage144_split_ci_runtime_strategy_pack/",
        "mode": report.get("mode"),
        "workflow_split_only": report.get("workflow_split_only"),
        "workflow_split_complete": report.get("workflow_split_complete"),
        "runtime_lane_count": report.get("runtime_lane_count"),
        "release_surface_ready": report.get("release_surface_ready"),
        "stage144_roadmap_terminal": report.get("stage144_roadmap_terminal"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Roadmap currently ends at Stage144",
            "Future stages require a new approved proposal set",
        ],
    }
    _write_json(root / "release/current/stage144_summary.json", summary)
    return {**report, "stage144_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
