from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.schema_registry import run_stage136_schema_registry


def run_stage136(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage136_schema_registry(root)
    summary = {
        "stage": "136",
        "baseline_stage": "135",
        "title": "SchemaRegistry",
        "status": report["status"],
        "main_report": "release/current/stage136_schema_registry_report.json",
        "release_gate_report": "release/current/stage136_release_gate_report.json",
        "evidence_pack": "release/current/stage136_schema_registry_pack/",
        "mode": report.get("mode"),
        "schema_registry_only": report.get("schema_registry_only"),
        "schema_count": report.get("schema_count"),
        "binding_count": report.get("binding_count"),
        "migration_ready_count": report.get("migration_ready_count"),
        "storage_contract_ready_count": report.get("storage_contract_ready_count"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage137 MigrationManager",
            "Stage138 LOSDB Storage Contracts",
            "Stage139 Corpus Governance Pipeline",
            "Stage140 Production Release Automation Closure",
        ],
    }
    _write_json(root / "release/current/stage136_summary.json", summary)
    return {**report, "stage136_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
