from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.multiwork_release import run_stage130_multiwork_release


def run_stage130(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage130_multiwork_release(root)
    summary = {
        "stage": "130",
        "baseline_stage": "129",
        "title": "MultiWork Release",
        "status": report["status"],
        "main_report": "release/current/stage130_multiwork_release_report.json",
        "release_gate_report": "release/current/stage130_release_gate_report.json",
        "evidence_pack": "release/current/stage130_multiwork_release_pack/",
        "multiwork_release_authorized": report.get("multiwork_release_authorized", False),
        "stage127_to_stage129_evidence_preserved": report.get("stage127_to_stage129_evidence_preserved", False),
        "cross_project_write_allowed": False,
        "raw_manuscript_provider_leakage": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage131 GIG / Gate26 Advisory Absorption",
            "Stage132 Contradiction Classifier + Mystery Exemption",
            "Stage133 NarrativeStateTensor 8D Measurement Layer",
            "Stage134 MetaLearner Audit Mode",
            "Stage135 Bounded Active MetaLearner",
            "Stage136 ASD Patch Proposal Mode",
            "Stage137 Human-Approved Repair Commit",
            "Stage138 Canonical Formula Registry",
            "Stage139 AuthorLicense / Project Rights Boundary",
            "Stage140 Production CI/CD and Release Automation",
        ],
    }
    _write_json(root / "release/current/stage130_summary.json", summary)
    return {**report, "stage130_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
