from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.longform_benchmark_pack import run_stage142_longform_benchmark_pack


def run_stage142(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage142_longform_benchmark_pack(root)
    summary = {
        "stage": "142",
        "baseline_stage": "141",
        "title": "Longform Benchmark Pack",
        "status": report["status"],
        "main_report": "release/current/stage142_longform_benchmark_pack_report.json",
        "release_gate_report": "release/current/stage142_release_gate_report.json",
        "asset_manifest": "release/current/stage142_release_asset_manifest.json",
        "evidence_pack": "release/current/stage142_longform_benchmark_pack/",
        "mode": report.get("mode"),
        "longform_benchmark_pack_only": report.get("longform_benchmark_pack_only"),
        "benchmark_case_count": report.get("benchmark_case_count"),
        "rendered_scene_count": report.get("rendered_scene_count"),
        "critic_gate_pass_count": report.get("critic_gate_pass_count"),
        "benchmark_scoreboard_status": report.get("benchmark_scoreboard_status"),
        "stage143_user_docs_ready": report.get("stage143_user_docs_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage143 User CLI/API Minimum Docs",
            "Stage144 Split CI Runtime Strategy",
            "Stage145 Release Surface Consolidation",
        ],
    }
    _write_json(root / "release/current/stage142_summary.json", summary)
    return {**report, "stage142_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
