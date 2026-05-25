from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage158_release_gate import run_stage158_release_gate
from v1700.stage159 import run_stage159

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage159_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage159":
        existing = _load_report(root, "stage159_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage159(root)
    parts = stage.get("parts", {})
    steps = parts.get("dry_run_trace_steps", {})
    replay = parts.get("trace_replay_ledger", {})
    policy = parts.get("side_effect_free_policy", {})
    node2 = parts.get("node2_trace_projection_matrix", {})
    integrity = parts.get("trace_integrity_snapshot", {})
    connectivity = parts.get("preflight_step15_connectivity_matrix", {})
    entry = parts.get("stage160_entry_criteria", {})
    regression = parts.get("regression_snapshot", {})

    checks = {
        "stage158_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage159_report_pass": _check(stage.get("status") == "pass"),
        "dry_run_trace_mode_pass": _check(stage.get("mode") == "EXECUTION_DRY_RUN_TRACE_LOCAL_ONLY"),
        "dry_run_trace_steps_pass": _check(steps.get("status") == "pass" and stage.get("trace_step_count", 0) >= 6),
        "trace_replay_ledger_pass": _check(replay.get("status") == "pass"),
        "side_effect_free_policy_pass": _check(policy.get("status") == "pass" and stage.get("side_effect_free_dry_run") is True),
        "node2_trace_projection_pass": _check(node2.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "trace_integrity_snapshot_pass": _check(integrity.get("status") == "pass" and len(str(stage.get("trace_checksum", ""))) == 64),
        "preflight_step15_connectivity_pass": _check(connectivity.get("status") == "pass"),
        "stage160_entry_criteria_pass": _check(entry.get("status") == "pass" and stage.get("stage160_page03_release_seal_ready") is True),
        "regression_snapshot_pass": _check(regression.get("status") == "pass"),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("generation_runtime_enabled") is False and stage.get("runtime_execution_count") == 0),
        "provider_execution_disabled": _check(stage.get("provider_execution_enabled") is False and stage.get("provider_execution_count") == 0),
        "write_operations_blocked": _check(stage.get("execution_write_enabled") is False and stage.get("dry_run_write_enabled") is False and stage.get("write_operation_count") == 0),
        "memory_store_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("store_write_enabled") is False),
        "canon_mutation_blocked": _check(stage.get("canon_mutation_enabled") is False and stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_blocked": _check(stage.get("auto_repair_apply_enabled") is False and stage.get("auto_repair_mutation_count") == 0),
        "vector_db_runtime_dependency_blocked": _check(stage.get("vector_db_runtime_dependency") is False),
        "live_provider_rag_blocked": _check(stage.get("live_provider_rag_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "159",
        "baseline_stage": "158",
        "title": "Execution Dry-Run Trace",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage159": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "runtime_execution_enabled": False,
        "dry_run_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage159_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage159":
        report = _load_report(root, "stage158_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage158_release_gate(root)


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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "trace_step_count", "trace_checksum", "stage160_page03_release_seal_ready", "runtime_execution_enabled", "generation_runtime_enabled", "provider_execution_enabled", "memory_write_enabled", "execution_write_enabled", "store_write_enabled", "graph_write_enabled", "preflight_write_enabled", "dry_run_write_enabled", "side_effect_free_dry_run", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "runtime_execution_count", "provider_execution_count", "write_operation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage159.md",
        "docs/proposals/stage159_execution_dry_run_trace_proposal.md",
        "docs/architecture/stage159_execution_dry_run_trace_blueprint.md",
        "docs/development/stage159_developer_handoff.md",
        "manifests/stage159_manifest.json",
        "manifests/stage159_execution_dry_run_trace_manifest.json",
        "manifests/stage159_branchpoint_trace_manifest.json",
        "release/current/stage159_execution_dry_run_trace_report.json",
        "release/current/stage159_release_gate_report.json",
        "release/current/stage159_execution_dry_run_trace_pack/dry_run_trace_steps.json",
        "release/current/stage159_execution_dry_run_trace_pack/trace_replay_ledger.json",
        "release/current/stage159_execution_dry_run_trace_pack/side_effect_free_policy.json",
        "release/current/stage159_execution_dry_run_trace_pack/node2_trace_projection_matrix.json",
        "release/current/stage159_execution_dry_run_trace_pack/trace_integrity_snapshot.json",
        "release/current/stage159_execution_dry_run_trace_pack/preflight_step15_connectivity_matrix.json",
        "release/current/stage159_execution_dry_run_trace_pack/stage160_entry_criteria.json",
        "release/current/stage159_execution_dry_run_trace_pack/regression_snapshot.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage159", "run_stage159_execution_dry_run_trace.py", "run_stage159_release_gate.py"])
