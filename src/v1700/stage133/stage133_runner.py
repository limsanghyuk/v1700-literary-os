from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.narrative_state_tensor import run_stage133_narrative_state_tensor


def run_stage133(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage133_narrative_state_tensor(root)
    summary = {
        "stage": "133",
        "baseline_stage": "132",
        "title": "NarrativeStateTensor 8D Measurement Layer",
        "status": report["status"],
        "main_report": "release/current/stage133_narrative_state_tensor_report.json",
        "release_gate_report": "release/current/stage133_release_gate_report.json",
        "evidence_pack": "release/current/stage133_narrative_state_tensor_pack/",
        "measurement_mode": report.get("measurement_mode"),
        "dimension_count": report.get("dimension_count"),
        "tensor_case_count": report.get("tensor_case_count"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage134 MetaLearner Audit Mode",
            "Stage135 Bounded Active MetaLearner",
            "Stage136 ASD Patch Proposal Mode",
            "Stage137 Human-Approved Repair Commit",
            "Stage138 Canonical Formula Registry",
            "Stage139 AuthorLicense / Project Rights Boundary",
            "Stage140 Production CI/CD and Release Automation",
        ],
    }
    _write_json(root / "release/current/stage133_summary.json", summary)
    return {**report, "stage133_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
