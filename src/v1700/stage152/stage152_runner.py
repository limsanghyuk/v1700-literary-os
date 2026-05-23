
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.memory_query_interface import run_stage152_memory_query_interface


def run_stage152(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage152_memory_query_interface(root)
    summary = {
        "stage": "152",
        "baseline_stage": "151",
        "title": "Deterministic Local Query / Ranking",
        "status": report["status"],
        "main_report": "release/current/stage152_memory_query_interface_report.json",
        "release_gate_report": "release/current/stage152_release_gate_report.json",
        "asset_manifest": "release/current/stage152_release_asset_manifest.json",
        "evidence_pack": "release/current/stage152_memory_query_interface_pack/",
        "mode": report.get("mode"),
        "query_runtime_enabled": report.get("query_runtime_enabled"),
        "ranking_runtime_enabled": report.get("ranking_runtime_enabled"),
        "query_write_enabled": report.get("query_write_enabled"),
        "candidate_count": report.get("candidate_count"),
        "stage153_memory_health_monitor_ready": report.get("stage153_memory_health_monitor_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": ["Stage153 Memory Health & Leakage Boundary", "Stage154 Page02 Release Seal"],
    }
    _write_json(root / "release/current/stage152_summary.json", summary)
    return {**report, "stage152_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
