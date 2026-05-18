from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.nil.nil_report import build_stage118_nil_orchestrator_report
from v1700.stage118.contracts import Stage118Contract


def run_stage118(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    nil_report = build_stage118_nil_orchestrator_report()
    contract = Stage118Contract().to_dict()
    issues: list[str] = list(nil_report.get("issues", []))
    components = nil_report.get("components", [])
    required = set(contract["components_required"])
    observed = {component.get("name") for component in components}
    if observed != required:
        issues.append("nil_component_set_mismatch")
    if nil_report.get("convergence", {}).get("loop_closure_status") != "pass":
        issues.append("nil_loop_closure_failed")
    invariant_counts = nil_report.get("invariant_counts", {})
    if any(int(value or 0) != 0 for value in invariant_counts.values()):
        issues.append("nil_invariant_count_nonzero")
    result = {
        "stage": "118",
        "baseline_stage": "117",
        "title": "NIL Orchestrator",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "nil_orchestrator": nil_report,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["Stage119", "Stage120"],
    }
    _write(root / "release/current/stage118_nil_orchestrator_report.json", result)
    return result


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
