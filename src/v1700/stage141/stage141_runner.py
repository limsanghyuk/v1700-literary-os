from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.prose_generation_e2e import run_stage141_prose_generation_e2e


def run_stage141(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage141_prose_generation_e2e(root)
    summary = {
        "stage": "141",
        "baseline_stage": "140",
        "title": "Prose Generation E2E Harness",
        "status": report["status"],
        "main_report": "release/current/stage141_prose_generation_e2e_report.json",
        "release_gate_report": "release/current/stage141_release_gate_report.json",
        "asset_manifest": "release/current/stage141_release_asset_manifest.json",
        "evidence_pack": "release/current/stage141_prose_generation_e2e_pack/",
        "mode": report.get("mode"),
        "prose_generation_e2e_only": report.get("prose_generation_e2e_only"),
        "rendered_scene_count": report.get("rendered_scene_count"),
        "critic_gate_status": report.get("critic_gate_status"),
        "benchmark_result_status": report.get("benchmark_result_status"),
        "stage142_benchmark_pack_ready": report.get("stage142_benchmark_pack_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage142 Longform Benchmark Pack",
            "Stage143 User CLI/API Minimum Docs",
            "Stage144 Split CI Runtime Strategy",
        ],
    }
    _write_json(root / "release/current/stage141_summary.json", summary)
    return {**report, "stage141_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
