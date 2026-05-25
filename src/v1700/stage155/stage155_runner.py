from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.execution_body_contract import run_stage155_execution_contract


def run_stage155(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage155_execution_contract(root)
    summary = {
        "stage": "155",
        "baseline_stage": "154",
        "title": "Execution Contract",
        "status": report["status"],
        "main_report": "release/current/stage155_execution_contract_report.json",
        "release_gate_report": "release/current/stage155_release_gate_report.json",
        "asset_manifest": "release/current/stage155_release_asset_manifest.json",
        "evidence_pack": "release/current/stage155_execution_contract_pack/",
        "mode": report.get("mode"),
        "execution_contract_only": report.get("execution_contract_only"),
        "page02_seal_inherited": report.get("page02_seal_inherited"),
        "stage156_local_execution_packet_store_ready": report.get("stage156_local_execution_packet_store_ready"),
        "contract_count": report.get("contract_count"),
        "boundary_rule_count": report.get("boundary_rule_count"),
        "write_policy_rule_count": report.get("write_policy_rule_count"),
        "node2_projection_rule_count": report.get("node2_projection_rule_count"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "runtime_execution_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": ["Stage156 Local Execution Packet Store"],
    }
    _write_json(root / "release/current/stage155_summary.json", summary)
    return {**report, "stage155_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
