from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.multiwork_preflight import run_multiwork_preflight


def run_stage127(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_multiwork_preflight(root)
    manifest = {
        "stage": "127",
        "baseline_stage": "126",
        "title": "MultiWork Preflight & Isolation Audit",
        "status": report["status"],
        "preflight_report": "release/current/stage127_multiwork_preflight_report.json",
        "release_gate_report": "release/current/stage127_release_gate_report.json",
        "evidence_pack": "release/current/stage127_multiwork_preflight_pack/",
        "direct_v571_merge_performed": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage128 SharedWorld / SharedCharacter Read-Only Absorption",
            "Stage129 MultiWorkCIM + Cross-Work Canon Governor",
            "Stage130 MultiWork Release",
            "Stage131 GIG / Gate26 Advisory Absorption",
        ],
    }
    _write_json(root / "release/current/stage127_summary.json", manifest)
    return {**report, "stage127_summary": manifest}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
