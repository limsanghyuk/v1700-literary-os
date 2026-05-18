from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.multiwork_cim_governor import run_stage129_multiwork_cim_governor


def run_stage129(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage129_multiwork_cim_governor(root)
    summary = {
        "stage": "129",
        "baseline_stage": "128",
        "title": "MultiWorkCIM + Cross-Work Canon Governor",
        "status": report["status"],
        "main_report": "release/current/stage129_multiwork_cim_governor_report.json",
        "release_gate_report": "release/current/stage129_release_gate_report.json",
        "evidence_pack": "release/current/stage129_multiwork_cim_governor_pack/",
        "project_local_cim_preserved": True,
        "cross_project_influence_write": 0,
        "cross_work_canon_merge_allowed": False,
        "canon_auto_resolution_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage130 MultiWork Release",
            "Stage131 GIG / Gate26 Advisory Absorption",
            "Stage132 Contradiction Classifier + Mystery Exemption",
        ],
    }
    _write_json(root / "release/current/stage129_summary.json", summary)
    return {**report, "stage129_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
