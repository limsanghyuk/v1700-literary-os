from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.shared_readonly_absorption import run_stage128_read_only_absorption


def run_stage128(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage128_read_only_absorption(root)
    summary = {
        "stage": "128",
        "baseline_stage": "127",
        "title": "SharedWorld / SharedCharacter Read-Only Absorption",
        "status": report["status"],
        "read_only_absorption_report": "release/current/stage128_read_only_absorption_report.json",
        "release_gate_report": "release/current/stage128_release_gate_report.json",
        "evidence_pack": "release/current/stage128_read_only_absorption_pack/",
        "shared_character_db_write_enabled": False,
        "shared_world_db_write_enabled": False,
        "shared_world_source_of_truth_promotion_allowed": False,
        "cross_project_write": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage129 MultiWorkCIM + Cross-Work Canon Governor",
            "Stage130 MultiWork Release",
            "Stage131 GIG / Gate26 Advisory Absorption",
        ],
    }
    _write_json(root / "release/current/stage128_summary.json", summary)
    return {**report, "stage128_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
