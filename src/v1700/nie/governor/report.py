from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.governor.contracts import GovernorDecision, Stage125Contract


def write_governor_reports(root: Path, decision: GovernorDecision) -> dict[str, Any]:
    contract = Stage125Contract().to_dict()
    payload = {
        "stage": "125",
        "baseline_stage": "124",
        "title": contract["title"],
        "status": decision.status,
        "issues": list(decision.blocked_by),
        "release_contract": contract,
        "governor_decision": decision.to_dict(),
        "gate_authority_map": {
            "Gate25": {"mode": "primary", "scope": "NIE v1.0 release authority"},
            "Gate28": {"mode": "secondary_quality", "scope": "ASD story quality/debt guard"},
            "Gate29": {"mode": "secondary_predictive", "scope": "PNE preemptive debt guard"},
        },
        "next_development_order": ["stage126"],
        **decision.invariants,
        "provider_default_calls": decision.invariants.get("provider_default_calls", 0),
        "live_provider_call_count_in_release_gate": decision.invariants.get("live_provider_call_count_in_release_gate", 0),
        "node2_raw_reveal_access": decision.invariants.get("node2_raw_reveal_access", 0),
        "raw_manuscript_provider_leakage": decision.invariants.get("raw_manuscript_provider_leakage", 0),
        "credential_leakage": decision.invariants.get("credential_leakage", 0),
        "branchpoint_lineage_preserved": decision.status == "pass",
    }
    _write_json(root / "release/current/stage125_gate25_28_29_governor_report.json", payload)
    _write_json(root / "release/current/stage125_gate_authority_map.json", payload["gate_authority_map"])
    _write_json(root / "release/current/stage125_governor_decision.json", decision.to_dict())
    _write_json(root / "manifests/stage125_gate_governor_manifest.json", {
        "stage": "125",
        "title": contract["title"],
        "baseline_stage": "124",
        "primary_authority": "Gate25",
        "secondary_authorities": ["Gate28", "Gate29"],
        "blocked_concepts": contract["blocked_concepts"],
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
    })
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
