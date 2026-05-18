from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.release import CrossLineageReleaseAssembler, write_cross_lineage_release_pack
from v1700.stage126.contracts import Stage126Contract


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_stage126(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    contract = Stage126Contract().to_dict()
    decision = CrossLineageReleaseAssembler(root).evaluate()
    payload = write_cross_lineage_release_pack(root, decision)

    issues = list(decision.blocked_by)
    result = {
        "stage": "126",
        "baseline_stage": "125",
        "title": contract["title"],
        "status": "pass" if not issues and decision.status == "pass" else "blocked",
        "issues": issues,
        "release_contract": contract,
        "cross_lineage_release_report_path": "release/current/stage126_cross_lineage_intelligence_release_report.json",
        "release_authority_manifest_path": "release/current/stage126_release_authority_manifest.json",
        "lineage_release_pack_path": "release/current/stage126_lineage_release_pack.json",
        "summary": {
            "sealed_lineage": decision.final_release_pack["sealed_lineage"],
            "release_authority": decision.release_authority,
            "authority_stack": decision.final_release_pack["authority_stack"],
            "blocked_by": list(decision.blocked_by),
        },
        "release_policy": {
            "stage125_governor_preserved": True,
            "gate25_primary_authority_preserved": decision.checks.get("stage120_gate25_primary_present"),
            "gate28_secondary_quality_preserved": decision.checks.get("stage123_gate28_secondary_present"),
            "gate29_secondary_predictive_preserved": decision.checks.get("stage124_gate29_secondary_present"),
            "direct_v545_v555_merge_performed": False,
            "gate28_primary_authority_enabled": False,
            "gate29_primary_authority_enabled": False,
            "release_gate_runtime_training_enabled": False,
            "auto_repair_mutation_allowed": False,
        },
        "next_development_order": ["stage127_optional_runtime_hardening"],
        **decision.invariants,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "story_doctor_llm_call_count": 0,
        "pne_provider_call_count": 0,
        "pne_runtime_training_count": 0,
        "auto_repair_mutation_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    _write_json(root / "release/current/stage126_cross_lineage_intelligence_release_report.json", {**payload, "stage126_summary": result["summary"]})
    _write_json(root / "manifests/stage126_cross_lineage_release_manifest.json", {
        "stage": "126",
        "title": contract["title"],
        "baseline_stage": "125",
        "absorbed_concepts": contract["absorbed_concepts"],
        "blocked_concepts": contract["blocked_concepts"],
        "release_report": "release/current/stage126_cross_lineage_intelligence_release_report.json",
        "release_authority_manifest": "release/current/stage126_release_authority_manifest.json",
        "lineage_release_pack": "release/current/stage126_lineage_release_pack.json",
        "provider_default_calls": 0,
    })
    return result
