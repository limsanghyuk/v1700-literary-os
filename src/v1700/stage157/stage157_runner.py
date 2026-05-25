from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.plan_graph_builder import run_stage157_deterministic_plan_graph_builder


def run_stage157(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage157_deterministic_plan_graph_builder(root)
    summary = {
        "stage": "157",
        "baseline_stage": "156",
        "title": "Deterministic Plan Graph Builder",
        "status": report["status"],
        "main_report": "release/current/stage157_deterministic_plan_graph_builder_report.json",
        "release_gate_report": "release/current/stage157_release_gate_report.json",
        "asset_manifest": "release/current/stage157_release_asset_manifest.json",
        "evidence_pack": "release/current/stage157_deterministic_plan_graph_builder_pack/",
        "mode": report.get("mode"),
        "node_count": report.get("node_count"),
        "edge_count": report.get("edge_count"),
        "critical_path_length": report.get("critical_path_length"),
        "graph_checksum": report.get("graph_checksum"),
        "stage158_dependency_conflict_preflight_ready": report.get("stage158_dependency_conflict_preflight_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "runtime_execution_enabled": False,
        "graph_write_enabled": False,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": ["Stage158 Dependency and Conflict Preflight"],
    }
    _write_json(root / "release/current/stage157_summary.json", summary)
    return {**report, "stage157_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
