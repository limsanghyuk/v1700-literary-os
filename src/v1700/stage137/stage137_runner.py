from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.migration_manager import run_stage137_migration_manager


def run_stage137(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage137_migration_manager(root)
    summary = {
        "stage": "137",
        "baseline_stage": "136",
        "title": "MigrationManager",
        "status": report["status"],
        "main_report": "release/current/stage137_migration_manager_report.json",
        "release_gate_report": "release/current/stage137_release_gate_report.json",
        "evidence_pack": "release/current/stage137_migration_manager_pack/",
        "mode": report.get("mode"),
        "migration_plan_only": report.get("migration_plan_only"),
        "migration_step_count": report.get("migration_step_count"),
        "covered_binding_count": report.get("covered_binding_count"),
        "approval_checkpoint_count": report.get("approval_checkpoint_count"),
        "rollback_ready_count": report.get("rollback_ready_count"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage138 LOSDB Storage Contracts",
            "Stage139 Corpus Governance Pipeline",
            "Stage140 Production Release Automation Closure",
        ],
    }
    _write_json(root / "release/current/stage137_summary.json", summary)
    return {**report, "stage137_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
