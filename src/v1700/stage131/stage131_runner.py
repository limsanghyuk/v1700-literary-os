from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gig_advisory import run_stage131_gig_advisory


def run_stage131(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage131_gig_advisory(root)
    summary = {
        "stage": "131",
        "baseline_stage": "130",
        "title": "GIG / Gate26 Advisory Absorption",
        "status": report["status"],
        "main_report": "release/current/stage131_gig_advisory_report.json",
        "release_gate_report": "release/current/stage131_release_gate_report.json",
        "evidence_pack": "release/current/stage131_gig_advisory_pack/",
        "advisory_mode": report.get("advisory_mode"),
        "gate26_hard_block_enabled": False,
        "writer_approval_guard": report.get("writer_approval_guard", False),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
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
    _write_json(root / "release/current/stage131_summary.json", summary)
    return {**report, "stage131_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
