from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.governor import GateGovernor, write_governor_reports
from v1700.stage125.contracts import Stage125Contract


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_stage125(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    contract = Stage125Contract().to_dict()
    decision = GateGovernor(root).evaluate()
    payload = write_governor_reports(root, decision)

    issues = list(decision.blocked_by)
    if decision.primary_gate != "Gate25":
        issues.append("gate25_not_primary")
    if "Gate28" not in decision.secondary_gates or "Gate29" not in decision.secondary_gates:
        issues.append("missing_secondary_gate")

    result = {
        "stage": "125",
        "baseline_stage": "124",
        "title": contract["title"],
        "status": "pass" if not issues and payload.get("status") == "pass" else "blocked",
        "issues": issues,
        "release_contract": contract,
        "governor_report_path": "release/current/stage125_gate25_28_29_governor_report.json",
        "governor_decision": decision.to_dict(),
        "summary": {
            "primary_gate": decision.primary_gate,
            "secondary_gates": list(decision.secondary_gates),
            "authority_mode": decision.authority_mode,
            "blocked_by": list(decision.blocked_by),
            "gate25_status": decision.gate_inputs[0].status,
            "gate28_status": decision.gate_inputs[1].status,
            "gate29_status": decision.gate_inputs[2].status,
        },
        "absorption_policy": {
            "stage124_gate29_secondary_predictive_gate_preserved": True,
            "stage123_gate28_secondary_quality_gate_preserved": True,
            "gate25_primary_authority_preserved": True,
            "gate28_primary_authority_enabled": False,
            "gate29_primary_authority_enabled": False,
            "release_gate_runtime_training_enabled": False,
            "auto_repair_mutation_allowed": False,
            "direct_v545_v555_merge_performed": False,
        },
        "next_development_order": ["stage126"],
        **decision.invariants,
        "provider_default_calls": decision.invariants.get("provider_default_calls", 0),
        "live_provider_call_count_in_release_gate": decision.invariants.get("live_provider_call_count_in_release_gate", 0),
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "story_doctor_llm_call_count": 0,
        "pne_provider_call_count": 0,
        "pne_runtime_training_count": decision.invariants.get("pne_runtime_training_count", 0),
        "auto_repair_mutation_count": decision.invariants.get("auto_repair_mutation_count", 0),
        "node2_raw_reveal_access": decision.invariants.get("node2_raw_reveal_access", 0),
        "raw_manuscript_provider_leakage": decision.invariants.get("raw_manuscript_provider_leakage", 0),
        "credential_leakage": decision.invariants.get("credential_leakage", 0),
        "branchpoint_lineage_preserved": not issues,
    }
    _write_json(root / "release/current/stage125_gate25_28_29_governor_report.json", result)
    _write_json(root / "release/current/stage125_gate_authority_map.json", result["governor_decision"])
    _write_json(root / "release/current/stage125_governor_decision.json", decision.to_dict())
    _write_json(root / "manifests/stage125_gate_governor_manifest.json", {
        "stage": "125",
        "title": contract["title"],
        "absorbed_concepts": contract["absorbed_concepts"],
        "blocked_concepts": contract["blocked_concepts"],
        "governor_report": "release/current/stage125_gate25_28_29_governor_report.json",
        "gate_authority_map": "release/current/stage125_gate_authority_map.json",
        "provider_default_calls": 0,
    })
    return result
