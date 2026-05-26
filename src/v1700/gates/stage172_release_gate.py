from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage171_release_gate import run_stage171_release_gate
from v1700.page05_release_seal import run_stage172_page05_release_seal


def run_stage172_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    baseline = _baseline_gate(root)
    stage = run_stage172_page05_release_seal(root)
    checks = {
        "baseline_stage171_gate_pass": _check(baseline.get("status") == "pass"),
        "page05_release_seal_pass": _check(stage.get("status") == "pass" and stage.get("page05_sealed") is True),
        "page05_stage_count_pass": _check(stage.get("page05_total_stage_count") == 6),
        "stage173_ready_pass": _check(stage.get("stage173_governance_contract_ready") is True),
        "quality_channel_pass": _check(stage.get("quality_channel_pass") is True),
        "continuity_channel_pass": _check(stage.get("continuity_channel_pass") is True),
        "regression_channel_pass": _check(stage.get("regression_channel_pass") is True),
        "boundary_channel_pass": _check(stage.get("boundary_channel_pass") is True),
        "determinism_channel_pass": _check(stage.get("determinism_channel_pass") is True),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("provider_generation_count") == 0),
        "write_zero_pass": _check(stage.get("write_operation_count") == 0 and stage.get("evaluation_write_enabled") is False and stage.get("memory_write_enabled") is False),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "training_mutation_disabled_pass": _check(stage.get("runtime_training_enabled") is False and stage.get("canon_mutation_enabled") is False and stage.get("auto_repair_apply_enabled") is False),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "preflight_execution_report_pass": _check(_preflight_execution_report_ok(root)),
        "package_comparison_report_pass": _check(_package_comparison_report_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "172",
        "baseline_stage": "171",
        "title": "Page05 Release Seal",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage172": _compact(stage),
        "page05_sealed": stage.get("page05_sealed") is True and not issues,
        "stage173_governance_contract_ready": stage.get("stage173_governance_contract_ready") is True and not issues,
        "quality_channel_pass": stage.get("quality_channel_pass") is True and not issues,
        "continuity_channel_pass": stage.get("continuity_channel_pass") is True and not issues,
        "regression_channel_pass": stage.get("regression_channel_pass") is True and not issues,
        "boundary_channel_pass": stage.get("boundary_channel_pass") is True and not issues,
        "determinism_channel_pass": stage.get("determinism_channel_pass") is True and not issues,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
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
        "canon_mutation_enabled": False,
        "runtime_training_enabled": False,
        "auto_repair_apply_enabled": False,
        "provider_generation_enabled": False,
        "generation_runtime_enabled": False,
        "runtime_execution_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage172_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage172":
        report = _load_report(root, "stage171_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage171_release_gate(root)


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
        "status", "stage", "baseline_stage", "title", "issues", "mode", "page05_sealed", "page05_total_stage_count", "page05_release_checksum", "stage173_governance_contract_ready", "quality_channel_pass", "continuity_channel_pass", "regression_channel_pass", "boundary_channel_pass", "determinism_channel_pass", "provider_evaluation_enabled", "evaluation_write_enabled", "memory_write_enabled", "cross_project_write_enabled", "canon_mutation_enabled", "runtime_training_enabled", "auto_repair_apply_enabled", "provider_default_calls", "live_provider_call_count_in_release_gate", "provider_generation_count", "runtime_execution_count", "write_operation_count", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved"
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage172_release_gate_report.json"}
    required = [
        "docs/stages/stage172.md",
        "docs/proposals/stage172_page05_release_seal_proposal.md",
        "docs/architecture/stage172_page05_release_seal_blueprint.md",
        "docs/development/stage172_developer_handoff.md",
        "docs/proposals/page05_evaluation_body_proposal.md",
        "docs/architecture/page05_evaluation_body_blueprint.md",
        "docs/development/page05_developer_handoff.md",
        "manifests/stage172_manifest.json",
        "manifests/stage172_page05_release_seal_manifest.json",
        "manifests/stage172_branchpoint_trace_manifest.json",
        "manifests/live_core_stage172_overlay.json",
        "release/current/stage172_release_asset_manifest.json",
        "release/current/stage172_page05_release_seal_report.json",
        "release/current/stage172_release_gate_report.json",
        "release/current/stage172_preflight_execution_report.json",
        "release/current/stage172_package_comparison_report.json",
        "release/current/stage172_page05_release_seal_pack/page05_stage_chain.json",
        "release/current/stage172_page05_release_seal_pack/page05_release_seal_matrix.json",
        "release/current/stage172_page05_release_seal_pack/page05_artifact_index.json",
        "release/current/stage172_page05_release_seal_pack/page05_invariant_freeze.json",
        "release/current/stage172_page05_release_seal_pack/page05_evaluation_evidence_matrix.json",
        "release/current/stage172_page05_release_seal_pack/page05_transition_criteria.json",
        "release/current/stage172_page05_release_seal_pack/page05_release_seal.json",
        "release/current/stage172_page05_release_seal_pack/regression_snapshot.json",
    ]
    return all((root / rel).exists() or rel in generated for rel in required)


def _preflight_execution_report_ok(root: Path) -> bool:
    report = _load_report(root, "stage172_preflight_execution_report.json")
    if not isinstance(report, dict):
        return False
    required = {
        "stage": "stage172",
        "status": "pass",
        "preflight_guide_read": True,
        "mandatory_predevelopment_check_result": "pass",
        "expected_next_stage": "stage173",
    }
    if any(report.get(key) != value for key, value in required.items()):
        return False
    if not report.get("baseline_package") or not report.get("baseline_package_sha256"):
        return False
    gitnexus = report.get("gitnexus")
    return isinstance(gitnexus, dict) and bool(gitnexus.get("status"))


def _package_comparison_report_ok(root: Path) -> bool:
    report = _load_report(root, "stage172_package_comparison_report.json")
    if not isinstance(report, dict):
        return False
    required = {
        "stage": "stage172",
        "status": "pass",
        "raw_sha256sums_check": "pass",
        "zip_reextract_check": "pass",
        "forbidden_cache_entries": 0,
    }
    if any(report.get(key) != value for key, value in required.items()):
        return False
    for key in ("previous_package_name", "previous_package_sha256", "new_package_name", "new_package_sha256_sidecar"):
        if not report.get(key):
            return False
    if report.get("new_package_sha256") in (None, "SEE_RELEASE_SIDECAR"):
        return False
    if report.get("new_package_sha256") != "external_sidecar_authoritative":
        # The final ZIP digest is self-referential if embedded before packaging;
        # the sidecar is the authoritative final digest.
        return False
    return True


def _procedure_alignment_ok(root: Path) -> bool:
    if _active_version(root) != "stage172":
        return True
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage172", "run_stage172_page05_release_seal.py", "run_stage172_release_gate.py"])
