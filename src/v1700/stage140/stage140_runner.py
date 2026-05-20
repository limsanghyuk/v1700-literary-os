from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.release_integrity import run_stage140_release_integrity


def run_stage140(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage140_release_integrity(root)
    summary = {
        "stage": "140",
        "baseline_stage": "139",
        "title": "Release Integrity & Product Proof Gate",
        "status": report["status"],
        "main_report": "release/current/stage140_release_integrity_report.json",
        "release_gate_report": "release/current/stage140_release_gate_report.json",
        "evidence_pack": "release/current/stage140_release_integrity_pack/",
        "metadata_consistency_status": report.get("metadata_consistency_status"),
        "release_asset_integrity_status": report.get("release_asset_integrity_status"),
        "sample_project_contract_status": report.get("sample_project_contract_status"),
        "benchmark_contract_status": report.get("benchmark_contract_status"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage141 Prose Generation E2E Harness",
            "Stage142 Longform Benchmark Pack",
            "Stage143 User CLI/API Minimum Docs",
            "Stage144 Split CI Runtime Strategy",
        ],
    }
    _write_json(root / "release/current/stage140_summary.json", summary)
    return {**report, "stage140_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
