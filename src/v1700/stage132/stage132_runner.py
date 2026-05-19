from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.contradiction_classifier import run_stage132_contradiction_classifier


def run_stage132(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage132_contradiction_classifier(root)
    summary = {
        "stage": "132",
        "baseline_stage": "131",
        "title": "Contradiction Classifier + Mystery Exemption",
        "status": report["status"],
        "main_report": "release/current/stage132_contradiction_classifier_report.json",
        "release_gate_report": "release/current/stage132_release_gate_report.json",
        "evidence_pack": "release/current/stage132_contradiction_classifier_pack/",
        "classifier_mode": report.get("classifier_mode"),
        "mystery_exemption_requires_reveal_lock": report.get("mystery_exemption_requires_reveal_lock"),
        "gate26_hard_block_enabled": False,
        "writer_approval_guard": report.get("writer_approval_guard", False),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
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
    _write_json(root / "release/current/stage132_summary.json", summary)
    return {**report, "stage132_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
