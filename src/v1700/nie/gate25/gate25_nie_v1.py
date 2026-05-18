from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.gate25.contracts import Gate25Contract


_STAGE_TO_COMPONENT = {
    "stage112": "gitnexus_preflight",
    "stage113": "physics_reward_bridge",
    "stage114": "adaptive_momentum_weights",
    "stage115": "character_influence_matrix",
    "stage116": "domain_specific_rag_fusion",
    "stage117": "narrative_tension_curve",
    "stage118": "nil_orchestrator",
    "stage119": "nie_adversarial_regression",
}


def build_gate25_nie_v1_report(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[4]
    contract = Gate25Contract().to_dict()
    stage_reports: dict[str, dict[str, Any]] = {}
    issues: list[str] = []
    component_matrix: dict[str, dict[str, Any]] = {}

    for rel in contract["required_stage_reports"]:
        path = root / rel
        report = _read_json(path)
        key = path.stem.replace("_release_gate_report", "")
        stage_reports[key] = _compact_report(report, rel)
        component = _STAGE_TO_COMPONENT.get(key, key)
        status = report.get("status")
        if status != "pass":
            issues.append(f"{key}_release_gate_not_pass")
        component_matrix[component] = {
            "stage": key,
            "report_path": rel,
            "status": status or "missing",
            "issues": report.get("issues", ["missing_report"]),
            "provider_zero": _count_zero(report, "provider_default_calls") and _count_zero(report, "live_provider_call_count_in_release_gate"),
            "node2_boundary": _count_zero(report, "node2_raw_reveal_access"),
            "raw_manuscript_leakage_zero": _count_zero(report, "raw_manuscript_provider_leakage"),
            "credential_leakage_zero": _count_zero(report, "credential_leakage"),
            "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved") is not False,
        }

    observed = set(component_matrix)
    required = set(contract["required_components"])
    missing_components = sorted(required - observed)
    if missing_components:
        issues.append("missing_components:" + ",".join(missing_components))

    stage119 = stage_reports.get("stage119", {})
    adv_summary = _read_json(root / "release/current/stage119_nie_adversarial_regression_report.json")
    adv = adv_summary.get("adversarial_regression", {})
    if adv.get("unexpected_pass_count") != 0:
        issues.append("stage119_unexpected_pass_count_nonzero")
    if adv.get("unexpected_block_count") != 0:
        issues.append("stage119_unexpected_block_count_nonzero")
    if int(adv.get("adversarial_cases_total", 0) or 0) < 12:
        issues.append("stage119_adversarial_case_count_below_gate25_contract")

    nil_report = _read_json(root / "release/current/stage118_nil_orchestrator_report.json")
    nil = nil_report.get("nil_orchestrator", {})
    if nil.get("convergence", {}).get("loop_closure_status") != "pass":
        issues.append("nil_loop_closure_not_pass")
    observed_nil_components = {row.get("name") for row in nil.get("components", [])}
    # Stage118 names are the component names emitted by the NIL orchestrator.
    # Structural balance is represented inside the character_influence_matrix
    # component summary, because Stage115 computes the CIM and triangle tension
    # together as one release unit.
    required_nil_components = {
        "character_influence_matrix",
        "adaptive_momentum_weights",
        "reward_bridge",
        "domain_rag_fusion",
        "narrative_tension_curve",
    }
    if not required_nil_components.issubset(observed_nil_components):
        missing = sorted(required_nil_components - observed_nil_components)
        issues.append("nil_component_coverage_missing:" + ",".join(missing))

    invariant_counts = _aggregate_invariant_counts(stage_reports)
    if any(int(value or 0) != 0 for value in invariant_counts.values()):
        issues.append("runtime_invariant_count_nonzero")

    status = "pass" if not issues else "blocked"
    result = {
        "stage": "120",
        "baseline_stage": "119",
        "title": "Gate25 NIE v1.0 Release",
        "status": status,
        "issues": issues,
        "release_contract": contract,
        "component_matrix": component_matrix,
        "stage_reports": stage_reports,
        "gate25_checks": {
            "gitnexus_preflight_pass": _component_pass(component_matrix, "gitnexus_preflight"),
            "mae_reward_contract_pass": _component_pass(component_matrix, "physics_reward_bridge"),
            "physics_reward_bridge_no_llm_pass": invariant_counts.get("physics_reward_bridge_llm_call_count", 0) == 0,
            "amw_alpha_bounds_pass": _component_pass(component_matrix, "adaptive_momentum_weights"),
            "amw_drift_guard_pass": _component_pass(component_matrix, "adaptive_momentum_weights"),
            "cim_asymmetric_matrix_pass": _component_pass(component_matrix, "character_influence_matrix"),
            "structural_balance_pass": _component_pass(component_matrix, "character_influence_matrix"),
            "domain_rag_classifier_pass": _component_pass(component_matrix, "domain_specific_rag_fusion"),
            "narrative_tension_curve_pass": _component_pass(component_matrix, "narrative_tension_curve"),
            "nil_orchestrator_report_pass": _component_pass(component_matrix, "nil_orchestrator") and "nil_loop_closure_not_pass" not in issues,
            "nie_adversarial_pack_pass": _component_pass(component_matrix, "nie_adversarial_regression") and adv.get("unexpected_pass_count") == 0,
            "provider_zero_pass": invariant_counts.get("provider_default_calls", 0) == 0 and invariant_counts.get("live_provider_call_count_in_release_gate", 0) == 0,
            "node2_boundary_pass": invariant_counts.get("node2_raw_reveal_access", 0) == 0,
            "raw_manuscript_leakage_zero_pass": invariant_counts.get("raw_manuscript_provider_leakage", 0) == 0,
            "credential_leakage_zero_pass": invariant_counts.get("credential_leakage", 0) == 0,
        },
        "invariant_counts": invariant_counts,
        "provider_default_calls": invariant_counts.get("provider_default_calls", 0),
        "live_provider_call_count_in_release_gate": invariant_counts.get("live_provider_call_count_in_release_gate", 0),
        "embedding_provider_call_count": invariant_counts.get("embedding_provider_call_count", 0),
        "query_classifier_llm_call_count": invariant_counts.get("query_classifier_llm_call_count", 0),
        "physics_reward_bridge_llm_call_count": invariant_counts.get("physics_reward_bridge_llm_call_count", 0),
        "mae_live_provider_call_count": invariant_counts.get("mae_live_provider_call_count", 0),
        "node2_raw_reveal_access": invariant_counts.get("node2_raw_reveal_access", 0),
        "raw_manuscript_provider_leakage": invariant_counts.get("raw_manuscript_provider_leakage", 0),
        "credential_leakage": invariant_counts.get("credential_leakage", 0),
        "branchpoint_lineage_preserved": not issues,
    }
    _write_pack(root, result, component_matrix)
    return result


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "missing", "issues": ["missing:" + path.as_posix()]}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "blocked", "issues": [f"invalid_json:{path.as_posix()}:{exc}"]}


def _compact_report(report: dict[str, Any], rel: str) -> dict[str, Any]:
    keep = (
        "stage", "baseline_stage", "title", "status", "issues",
        "provider_default_calls", "live_provider_call_count_in_release_gate",
        "embedding_provider_call_count", "query_classifier_llm_call_count",
        "physics_reward_bridge_llm_call_count", "mae_live_provider_call_count",
        "node2_raw_reveal_access", "raw_manuscript_provider_leakage",
        "credential_leakage", "branchpoint_lineage_preserved",
    )
    compact = {key: report.get(key) for key in keep if key in report}
    compact["report_path"] = rel
    return compact


def _count_zero(report: dict[str, Any], key: str) -> bool:
    return int(report.get(key, 0) or 0) == 0


def _component_pass(matrix: dict[str, dict[str, Any]], name: str) -> bool:
    return matrix.get(name, {}).get("status") == "pass"


def _aggregate_invariant_counts(stage_reports: dict[str, dict[str, Any]]) -> dict[str, int]:
    keys = (
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "embedding_provider_call_count",
        "query_classifier_llm_call_count",
        "physics_reward_bridge_llm_call_count",
        "mae_live_provider_call_count",
        "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage",
        "credential_leakage",
    )
    counts = {key: 0 for key in keys}
    for report in stage_reports.values():
        for key in keys:
            counts[key] += int(report.get(key, 0) or 0)
    return counts


def _write_pack(root: Path, result: dict[str, Any], component_matrix: dict[str, Any]) -> None:
    pack = root / "release/current/stage120_nie_v1_release_pack"
    pack.mkdir(parents=True, exist_ok=True)
    (pack / "gate25_nie_v1_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (pack / "stage120_component_matrix.json").write_text(json.dumps(component_matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Stage120 Gate25 NIE v1.0 Summary",
        "",
        f"status: {result['status']}",
        f"issues: {', '.join(result['issues']) if result['issues'] else 'none'}",
        "",
        "## Components",
    ]
    for name, row in component_matrix.items():
        summary.append(f"- {name}: {row.get('status')}")
    (pack / "stage120_nie_v1_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
