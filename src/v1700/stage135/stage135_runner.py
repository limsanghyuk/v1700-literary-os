from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.learning_quality_gate import run_stage135_learning_quality_gate


def run_stage135(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage135_learning_quality_gate(root)
    summary = {
        "stage": "135",
        "baseline_stage": "134",
        "title": "LearningQualityGate & Candidate Registry",
        "status": report["status"],
        "main_report": "release/current/stage135_learning_quality_gate_report.json",
        "release_gate_report": "release/current/stage135_release_gate_report.json",
        "evidence_pack": "release/current/stage135_learning_quality_gate_pack/",
        "mode": report.get("mode"),
        "learning_candidate_only": report.get("learning_candidate_only"),
        "candidate_count": report.get("candidate_count"),
        "review_only_count": report.get("review_only_count"),
        "learning_allowed_count": report.get("learning_allowed_count"),
        "training_triggered_count": report.get("training_triggered_count"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage136 SchemaRegistry",
            "Stage137 MigrationManager",
            "Stage138 LOSDB Storage Contracts",
            "Stage139 Corpus Governance Pipeline",
            "Stage140 Production Release Automation Closure",
        ],
    }
    _write_json(root / "release/current/stage135_summary.json", summary)
    return {**report, "stage135_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
