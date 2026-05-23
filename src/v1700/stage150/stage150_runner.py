from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.memory_body_contract import run_stage150_memory_contract


def run_stage150(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage150_memory_contract(root)
    summary = {
        "stage": "150",
        "baseline_stage": "149",
        "title": "Memory Contract",
        "status": report["status"],
        "main_report": "release/current/stage150_memory_contract_report.json",
        "release_gate_report": "release/current/stage150_release_gate_report.json",
        "asset_manifest": "release/current/stage150_release_asset_manifest.json",
        "evidence_pack": "release/current/stage150_memory_contract_pack/",
        "mode": report.get("mode"),
        "memory_contract_only": report.get("memory_contract_only"),
        "contract_count": report.get("contract_count"),
        "boundary_rule_count": report.get("boundary_rule_count"),
        "write_policy_rule_count": report.get("write_policy_rule_count"),
        "node2_projection_rule_count": report.get("node2_projection_rule_count"),
        "stage151_local_read_only_memory_store_ready": report.get("stage151_local_read_only_memory_store_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": [
            "Stage151 Local Read-Only Memory Store",
            "Stage152 Memory Query Interface",
        ],
    }
    _write_json(root / "release/current/stage150_summary.json", summary)
    return {**report, "stage150_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
