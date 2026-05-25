from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.dependency_conflict_preflight import run_stage158_dependency_conflict_preflight


def run_stage158(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage158_dependency_conflict_preflight(root)
    summary = {
        "stage": "158",
        "baseline_stage": "157",
        "title": "Dependency and Conflict Preflight",
        "status": report["status"],
        "main_report": "release/current/stage158_dependency_conflict_preflight_report.json",
        "release_gate_report": "release/current/stage158_release_gate_report.json",
        "asset_manifest": "release/current/stage158_release_asset_manifest.json",
        "evidence_pack": "release/current/stage158_dependency_conflict_preflight_pack/",
        "mode": report.get("mode"),
        "packet_count": report.get("packet_count"),
        "dependency_count": report.get("dependency_count"),
        "conflict_count": report.get("conflict_count"),
        "boundary_violation_count": report.get("boundary_violation_count"),
        "preflight_checksum": report.get("preflight_checksum"),
        "stage159_execution_dry_run_trace_ready": report.get("stage159_execution_dry_run_trace_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "runtime_execution_enabled": False,
        "preflight_write_enabled": False,
        "graph_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": ["Stage159 Execution Dry-Run Trace"],
    }
    _write_json(root / "release/current/stage158_summary.json", summary)
    return {**report, "stage158_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
