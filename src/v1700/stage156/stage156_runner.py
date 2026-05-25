from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.local_execution_packet_store import run_stage156_local_execution_packet_store


def run_stage156(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage156_local_execution_packet_store(root)
    summary = {
        "stage": "156",
        "baseline_stage": "155",
        "title": "Local Execution Packet Store",
        "status": report["status"],
        "main_report": "release/current/stage156_local_execution_packet_store_report.json",
        "release_gate_report": "release/current/stage156_release_gate_report.json",
        "asset_manifest": "release/current/stage156_release_asset_manifest.json",
        "evidence_pack": "release/current/stage156_local_execution_packet_store_pack/",
        "mode": report.get("mode"),
        "packet_count": report.get("packet_count"),
        "checksum_count": report.get("checksum_count"),
        "page03_execution_contract_inherited": report.get("page03_execution_contract_inherited"),
        "stage157_plan_graph_builder_ready": report.get("stage157_plan_graph_builder_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "runtime_execution_enabled": False,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": ["Stage157 Deterministic Plan Graph Builder"],
    }
    _write_json(root / "release/current/stage156_summary.json", summary)
    return {**report, "stage156_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
