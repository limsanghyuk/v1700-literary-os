from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.losdb_storage_contracts import run_stage138_losdb_storage_contracts


def run_stage138(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage138_losdb_storage_contracts(root)
    summary = {
        "stage": "138",
        "baseline_stage": "137",
        "title": "LOSDB Storage Contracts",
        "status": report["status"],
        "main_report": "release/current/stage138_losdb_storage_contracts_report.json",
        "release_gate_report": "release/current/stage138_release_gate_report.json",
        "evidence_pack": "release/current/stage138_losdb_storage_contracts_pack/",
        "mode": report.get("mode"),
        "storage_contract_catalog_only": report.get("storage_contract_catalog_only"),
        "schema_contract_count": report.get("schema_contract_count"),
        "binding_route_count": report.get("binding_route_count"),
        "approval_lane_count": report.get("approval_lane_count"),
        "governance_ready_count": report.get("governance_ready_count"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage139 Corpus Governance Pipeline",
            "Stage140 Production Release Automation Closure",
        ],
    }
    _write_json(root / "release/current/stage138_summary.json", summary)
    return {**report, "stage138_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
