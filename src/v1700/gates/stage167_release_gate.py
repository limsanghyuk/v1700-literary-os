from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage166_release_gate import run_stage166_release_gate
from v1700.stage167 import run_stage167

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage167_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage167":
        existing = _load_report(root, "stage167_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage167(root)
    parts = stage.get("parts", {})
    readiness = parts.get("page05_readiness_matrix", {})
    contracts = parts.get("evaluation_contract_catalog", {})
    rubrics = parts.get("evaluation_rubric_catalog", {})
    boundary = parts.get("evaluation_boundary_policy", {})
    authority = parts.get("evaluation_authority_policy", {})
    criteria = parts.get("stage168_entry_criteria", {})

    checks = {
        "stage166_baseline_gate_pass": _check(_stage166_ready(baseline)),
        "stage167_report_pass": _check(stage.get("status") == "pass"),
        "evaluation_contract_mode_pass": _check(stage.get("evaluation_contract_only") is True and stage.get("mode") == "EVALUATION_CONTRACT_LOCAL_ONLY"),
        "page05_readiness_pass": _check(readiness.get("status") == "pass" and readiness.get("check_count", 0) >= 7),
        "evaluation_contract_catalog_pass": _check(contracts.get("status") == "pass" and contracts.get("contract_count", 0) >= 12),
        "evaluation_rubric_catalog_pass": _check(rubrics.get("status") == "pass" and rubrics.get("weight_sum_valid") is True),
        "thresholds_explicit_pass": _check(stage.get("thresholds_explicit") is True and stage.get("boundary_override_defined") is True),
        "evaluation_boundary_policy_pass": _check(boundary.get("status") == "pass" and boundary.get("boundary_criteria_non_overridable") is True),
        "evaluation_authority_policy_pass": _check(authority.get("status") == "pass" and stage.get("provider_evaluation_enabled") is False),
        "stage168_entry_criteria_pass": _check(criteria.get("status") == "pass" and stage.get("stage168_packet_store_ready") is True),
        "provider_evaluation_disabled": _check(stage.get("provider_evaluation_enabled") is False and stage.get("provider_default_calls") == 0),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("runtime_execution_count") == 0),
        "write_operations_blocked": _check(stage.get("evaluation_write_enabled") is False and stage.get("write_operation_count") == 0),
        "memory_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("cross_project_write_enabled") is False),
        "canon_mutation_blocked": _check(stage.get("canon_mutation_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False and stage.get("auto_repair_apply_enabled") is False),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "167",
        "baseline_stage": "166",
        "title": "Evaluation Contract",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage167": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "provider_evaluation_enabled": False,
        "evaluation_write_enabled": False,
        "memory_write_enabled": False,
        "cross_project_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage167_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage167":
        report = _load_report(root, "stage166_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage166_release_gate(root)


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_report(root: Path, name: str) -> dict[str, Any] | None:
    path = root / "release/current" / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "mode",
        "evaluation_contract_only",
        "stage166_page04_seal_inherited",
        "stage168_packet_store_ready",
        "contract_count",
        "subject_count",
        "rubric_count",
        "metric_count",
        "rubric_weight_total",
        "rubric_weights_valid",
        "thresholds_explicit",
        "boundary_override_defined",
        "authority_policy_locked",
        "provider_evaluation_enabled",
        "evaluation_write_enabled",
        "memory_write_enabled",
        "cross_project_write_enabled",
        "canon_mutation_enabled",
        "runtime_training_enabled",
        "auto_repair_apply_enabled",
        "provider_default_calls",
        "node2_raw_reveal_access",
        "boundary_violation_count",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _stage166_ready(report: dict[str, Any]) -> bool:
    if report.get("status") == "pass":
        return True
    historical = report.get("stage166", {})
    return historical.get("status") == "pass" and historical.get("page04_sealed") is True


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage167_release_gate_report.json"}
    return all((root / rel).exists() or rel in generated for rel in [
        "docs/stages/stage167.md",
        "docs/proposals/stage167_evaluation_contract_proposal.md",
        "docs/architecture/stage167_evaluation_contract_blueprint.md",
        "docs/development/stage167_developer_handoff.md",
        "docs/proposals/page05_evaluation_body_proposal.md",
        "docs/architecture/page05_evaluation_body_blueprint.md",
        "docs/development/page05_developer_handoff.md",
        "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        "docs/workflow/PREFLIGHT_GUIDE_v1.1_STAGE160.md",
        "docs/workflow/BRANCH_STRATEGY.md",
        "manifests/stage167_manifest.json",
        "manifests/stage167_evaluation_contract_manifest.json",
        "manifests/stage167_branchpoint_trace_manifest.json",
        "manifests/live_core_stage167_overlay.json",
        "release/current/stage167_release_asset_manifest.json",
        "release/current/stage167_evaluation_contract_report.json",
        "release/current/stage167_release_gate_report.json",
        "release/current/stage167_evaluation_contract_pack/page05_readiness_matrix.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_contract_catalog.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_rubric_catalog.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_boundary_policy.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_authority_policy.json",
        "release/current/stage167_evaluation_contract_pack/stage168_entry_criteria.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage167", "run_stage167_evaluation_contract.py", "run_stage167_release_gate.py"])
