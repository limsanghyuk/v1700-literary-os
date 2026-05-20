from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.corpus_governance_pipeline import run_stage139_corpus_governance_pipeline


def run_stage139(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage139_corpus_governance_pipeline(root)
    summary = {
        "stage": "139",
        "baseline_stage": "138",
        "title": "Corpus Governance Pipeline",
        "status": report["status"],
        "main_report": "release/current/stage139_corpus_governance_pipeline_report.json",
        "release_gate_report": "release/current/stage139_release_gate_report.json",
        "evidence_pack": "release/current/stage139_corpus_governance_pipeline_pack/",
        "mode": report.get("mode"),
        "corpus_governance_pipeline_only": report.get("corpus_governance_pipeline_only"),
        "governance_profile_count": report.get("governance_profile_count"),
        "case_packet_count": report.get("case_packet_count"),
        "review_queue_packet_count": report.get("review_queue_packet_count"),
        "stage140_release_ready_count": report.get("stage140_release_ready_count"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage140 Production Release Automation Closure",
        ],
    }
    _write_json(root / "release/current/stage139_summary.json", summary)
    return {**report, "stage139_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
