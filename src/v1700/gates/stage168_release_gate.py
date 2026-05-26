from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage167_release_gate import run_stage167_release_gate
from v1700.stage168 import run_stage168

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage168_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage168":
        existing = _load_report(root, "stage168_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage168(root)
    parts = stage.get("parts", {})
    catalog = parts.get("evaluation_packet_store_catalog", {})
    schema = parts.get("evaluation_packet_schema_validation", {})
    checksum = parts.get("evaluation_packet_checksum_index", {})
    duplicate = parts.get("evaluation_packet_duplicate_detector", {})
    policy = parts.get("read_only_evaluation_access_policy", {})
    subject_resolver = parts.get("evaluation_subject_resolver", {})
    stage166_resolver = parts.get("stage166_evidence_resolver", {})
    node2 = parts.get("node2_evaluation_packet_projection_matrix", {})
    load_order = parts.get("deterministic_load_order", {})
    regression = parts.get("regression_snapshot", {})

    checks = {
        "stage167_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage168_report_pass": _check(stage.get("status") == "pass"),
        "evaluation_packet_store_mode_pass": _check(stage.get("mode") == "LOCAL_EVALUATION_PACKET_STORE_READ_ONLY" and stage.get("packet_store_read_only") is True),
        "evaluation_packet_catalog_pass": _check(catalog.get("status") == "pass" and stage.get("evaluation_packet_count", 0) >= 6),
        "evaluation_packet_schema_validation_pass": _check(schema.get("status") == "pass"),
        "evaluation_packet_checksum_index_pass": _check(checksum.get("status") == "pass" and stage.get("checksum_count", 0) >= 6),
        "evaluation_packet_duplicate_detector_pass": _check(duplicate.get("status") == "pass" and duplicate.get("duplicate_count", 0) == 0),
        "read_only_evaluation_access_policy_pass": _check(policy.get("status") == "pass" and stage.get("evaluation_write_enabled") is False),
        "evaluation_subject_resolver_pass": _check(subject_resolver.get("status") == "pass"),
        "stage166_evidence_resolver_pass": _check(stage166_resolver.get("status") == "pass" and stage.get("stage166_refs_resolvable") is True),
        "node2_evaluation_projection_pass": _check(node2.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "deterministic_load_order_pass": _check(load_order.get("status") == "pass" and stage.get("load_order_deterministic") is True),
        "regression_snapshot_pass": _check(regression.get("status") == "pass"),
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
        "stage": "168",
        "baseline_stage": "167",
        "title": "Local Evaluation Packet Store",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage168": _compact(stage),
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
    out = root / "release/current/stage168_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage168":
        report = _load_report(root, "stage167_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage167_release_gate(root)


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
        "evaluation_packet_count",
        "checksum_count",
        "packet_store_read_only",
        "evaluation_packet_store_enabled",
        "stage167_contract_inherited",
        "stage166_refs_resolvable",
        "load_order_deterministic",
        "stage169_evaluator_ready",
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


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage168_release_gate_report.json"}
    return all((root / rel).exists() or rel in generated for rel in [
        "docs/stages/stage168.md",
        "docs/proposals/stage168_local_evaluation_packet_store_proposal.md",
        "docs/architecture/stage168_local_evaluation_packet_store_blueprint.md",
        "docs/development/stage168_developer_handoff.md",
        "docs/proposals/page05_evaluation_body_proposal.md",
        "docs/architecture/page05_evaluation_body_blueprint.md",
        "docs/development/page05_developer_handoff.md",
        "docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md",
        "docs/workflow/PREFLIGHT_GUIDE_v1.1_STAGE160.md",
        "docs/workflow/BRANCH_STRATEGY.md",
        "manifests/stage168_manifest.json",
        "manifests/stage168_local_evaluation_packet_store_manifest.json",
        "manifests/stage168_branchpoint_trace_manifest.json",
        "manifests/live_core_stage168_overlay.json",
        "release/current/stage168_release_asset_manifest.json",
        "release/current/stage168_local_evaluation_packet_store_report.json",
        "release/current/stage168_release_gate_report.json",
        "release/current/stage168_local_evaluation_packet_store_pack/evaluation_packet_store_catalog.json",
        "release/current/stage168_local_evaluation_packet_store_pack/evaluation_packet_schema_validation.json",
        "release/current/stage168_local_evaluation_packet_store_pack/evaluation_packet_checksum_index.json",
        "release/current/stage168_local_evaluation_packet_store_pack/evaluation_packet_duplicate_detector.json",
        "release/current/stage168_local_evaluation_packet_store_pack/read_only_evaluation_access_policy.json",
        "release/current/stage168_local_evaluation_packet_store_pack/evaluation_subject_resolver.json",
        "release/current/stage168_local_evaluation_packet_store_pack/stage166_evidence_resolver.json",
        "release/current/stage168_local_evaluation_packet_store_pack/node2_evaluation_packet_projection_matrix.json",
        "release/current/stage168_local_evaluation_packet_store_pack/deterministic_load_order.json",
        "release/current/stage168_local_evaluation_packet_store_pack/regression_snapshot.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage168", "run_stage168_local_evaluation_packet_store.py", "run_stage168_release_gate.py"])

