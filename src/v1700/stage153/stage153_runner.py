from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.memory_health_boundary import run_stage153_memory_health_leakage_boundary


def run_stage153(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage153_memory_health_leakage_boundary(root)
    summary = {
        "stage": "153",
        "baseline_stage": "152",
        "title": "Memory Health & Leakage Boundary",
        "status": report["status"],
        "main_report": "release/current/stage153_memory_health_leakage_boundary_report.json",
        "release_gate_report": "release/current/stage153_release_gate_report.json",
        "asset_manifest": "release/current/stage153_release_asset_manifest.json",
        "evidence_pack": "release/current/stage153_memory_health_leakage_boundary_pack/",
        "mode": report.get("mode"),
        "health_monitor_enabled": report.get("health_monitor_enabled"),
        "leakage_boundary_enabled": report.get("leakage_boundary_enabled"),
        "boundary_violation_count": report.get("boundary_violation_count"),
        "health_check_count": report.get("health_check_count"),
        "stage154_page02_release_seal_ready": report.get("stage154_page02_release_seal_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": ["Stage154 Page02 Release Seal"],
    }
    _write_json(root / "release/current/stage153_summary.json", summary)
    return {**report, "stage153_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
