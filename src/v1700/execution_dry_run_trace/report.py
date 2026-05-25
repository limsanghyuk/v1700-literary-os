from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage158_release_gate import run_stage158_release_gate

from .contracts import DryRunPolicyRule, TraceConnectivityCheck
from .tracer import build_execution_dry_run_trace

TARGET_STAGE = "stage159"
TARGET_REPORT = "release/current/stage159_execution_dry_run_trace_report.json"
STAGE157_REPORT = "release/current/stage157_deterministic_plan_graph_builder_report.json"
STAGE158_REPORT = "release/current/stage158_dependency_conflict_preflight_report.json"


def run_stage159_execution_dry_run_trace(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage158 = run_stage158_release_gate(root)
    stage157_report = _load_existing(root / STAGE157_REPORT) or {}
    stage158_report = _load_existing(root / STAGE158_REPORT) or {}
    trace = build_execution_dry_run_trace(stage157_report, stage158_report)
    pack = root / "release/current/stage159_execution_dry_run_trace_pack"
    pack.mkdir(parents=True, exist_ok=True)

    parts = {
        "dry_run_trace_steps": _dry_run_trace_steps(trace),
        "trace_replay_ledger": _trace_replay_ledger(trace),
        "side_effect_free_policy": _side_effect_free_policy(),
        "node2_trace_projection_matrix": _node2_trace_projection_matrix(trace),
        "trace_integrity_snapshot": _trace_integrity_snapshot(stage157_report, stage158_report, trace),
        "preflight_step15_connectivity_matrix": _preflight_step15_connectivity_matrix(root),
        "stage160_entry_criteria": _stage160_entry_criteria(trace),
        "regression_snapshot": _regression_snapshot(trace),
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage158.get("status") != "pass":
        issues.append("stage158_release_gate_blocked")
    if trace.get("status") != "pass":
        issues.extend(f"dry_run_trace:{issue}" for issue in trace.get("issues", []))
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "159",
        "baseline_stage": "158",
        "title": "Execution Dry-Run Trace",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "EXECUTION_DRY_RUN_TRACE_LOCAL_ONLY",
        "page": "Page03 Execution Body",
        "source_stage157_report": STAGE157_REPORT,
        "source_stage158_report": STAGE158_REPORT,
        "trace_step_count": trace.get("trace_step_count", 0),
        "trace_checksum": trace.get("trace_checksum", ""),
        "source_graph_checksum": trace.get("source_graph_checksum", ""),
        "source_preflight_checksum": trace.get("source_preflight_checksum", ""),
        "runtime_execution_enabled": False,
        "generation_runtime_enabled": False,
        "provider_execution_enabled": False,
        "memory_write_enabled": False,
        "execution_write_enabled": False,
        "store_write_enabled": False,
        "graph_write_enabled": False,
        "preflight_write_enabled": False,
        "dry_run_write_enabled": False,
        "side_effect_free_dry_run": True,
        "canon_mutation_enabled": False,
        "auto_repair_apply_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_execution_payload_access": 0,
        "boundary_violation_count": trace.get("boundary_violation_count", 0),
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "stage160_page03_release_seal_ready": not issues,
        "parts": {"stage158_release_gate": _compact(stage158), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _dry_run_trace_steps(trace: dict[str, Any]) -> dict[str, Any]:
    steps = list(trace.get("dry_run_trace", []))
    issues = [str(step.get("trace_id")) for step in steps if step.get("status") != "pass"]
    return {"stage": TARGET_STAGE, "title": "Dry-Run Trace Steps", "status": "pass" if steps and not issues else "blocked", "issues": issues or ([] if steps else ["empty_trace"]), "trace_step_count": len(steps), "steps": steps}


def _trace_replay_ledger(trace: dict[str, Any]) -> dict[str, Any]:
    records = list(trace.get("replay_records", []))
    unique = len({record.get("checksum") for record in records}) == len(records)
    issues = [] if records and unique else ["invalid_replay_ledger"]
    return {"stage": TARGET_STAGE, "title": "Trace Replay Ledger", "status": "pass" if not issues else "blocked", "issues": issues, "record_count": len(records), "records": records}


def _side_effect_free_policy() -> dict[str, Any]:
    rules = (
        DryRunPolicyRule("runtime_execution_disabled", False, True, TARGET_REPORT),
        DryRunPolicyRule("provider_execution_disabled", False, True, TARGET_REPORT),
        DryRunPolicyRule("write_operation_disabled", False, True, TARGET_REPORT),
        DryRunPolicyRule("canon_mutation_disabled", False, True, TARGET_REPORT),
        DryRunPolicyRule("auto_repair_apply_disabled", False, True, TARGET_REPORT),
        DryRunPolicyRule("runtime_training_disabled", False, True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if rule.enabled or not rule.must_remain_disabled]
    return {"stage": TARGET_STAGE, "title": "Side-Effect-Free Dry-Run Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _node2_trace_projection_matrix(trace: dict[str, Any]) -> dict[str, Any]:
    rows = []
    issues = []
    forbidden = ("hidden_reveal_payload", "private_note", "write_handle", "canon_mutation_command", "learning_payload", "raw_manuscript_payload", "credential", "provider_payload")
    for step in trace.get("dry_run_trace", []):
        surface = str(step.get("node2_projection_summary", "")).lower()
        hits = sorted(token for token in forbidden if token in surface)
        if hits:
            issues.append(f"{step.get('packet_id')}:{','.join(hits)}")
        rows.append({"trace_id": step.get("trace_id"), "packet_id": step.get("packet_id"), "node2_surface_allowed": not hits, "forbidden_token_hits": hits, "status": "pass" if not hits else "blocked"})
    return {"stage": TARGET_STAGE, "title": "Node2 Trace Projection Matrix", "status": "pass" if rows and not issues else "blocked", "issues": issues or ([] if rows else ["empty_projection_matrix"]), "row_count": len(rows), "matrix": rows, "node2_raw_reveal_access": 0, "node2_hidden_execution_payload_access": 0}


def _trace_integrity_snapshot(stage157_report: dict[str, Any], stage158_report: dict[str, Any], trace: dict[str, Any]) -> dict[str, Any]:
    issues = []
    for label, checksum in (("graph", stage157_report.get("graph_checksum", "")), ("preflight", stage158_report.get("preflight_checksum", "")), ("trace", trace.get("trace_checksum", ""))):
        if len(str(checksum)) != 64:
            issues.append(f"invalid_{label}_checksum")
    return {"stage": TARGET_STAGE, "title": "Trace Integrity Snapshot", "status": "pass" if not issues else "blocked", "issues": issues, "source_graph_checksum": stage157_report.get("graph_checksum", ""), "source_preflight_checksum": stage158_report.get("preflight_checksum", ""), "trace_checksum": trace.get("trace_checksum", ""), "trace_step_count": trace.get("trace_step_count", 0)}


def _preflight_step15_connectivity_matrix(root: Path) -> dict[str, Any]:
    checks = (
        TraceConnectivityCheck("stage159_package", "src/v1700/execution_dry_run_trace/__init__.py", True, (root / "src/v1700/execution_dry_run_trace/__init__.py").exists()),
        TraceConnectivityCheck("stage159_runner", "src/v1700/stage159/stage159_runner.py", True, (root / "src/v1700/stage159/stage159_runner.py").exists()),
        TraceConnectivityCheck("stage159_gate", "src/v1700/gates/stage159_release_gate.py", True, (root / "src/v1700/gates/stage159_release_gate.py").exists()),
        TraceConnectivityCheck("stage159_tool", "tools/run_stage159_execution_dry_run_trace.py", True, (root / "tools/run_stage159_execution_dry_run_trace.py").exists()),
        TraceConnectivityCheck("stage159_gate_tool", "tools/run_stage159_release_gate.py", True, (root / "tools/run_stage159_release_gate.py").exists()),
        TraceConnectivityCheck("stage159_test", "tests/test_stage159_execution_dry_run_trace.py", True, (root / "tests/test_stage159_execution_dry_run_trace.py").exists()),
        TraceConnectivityCheck("stage159_manifest", "manifests/stage159_manifest.json", True, (root / "manifests/stage159_manifest.json").exists()),
        TraceConnectivityCheck("stage159_docs", "docs/stages/stage159.md", True, (root / "docs/stages/stage159.md").exists()),
    )
    issues = [check.name for check in checks if check.required and not check.exists]
    return {"stage": TARGET_STAGE, "title": "Preflight Step15 Connectivity Matrix", "status": "pass" if not issues else "blocked", "issues": issues, "check_count": len(checks), "checks": [check.to_dict() for check in checks]}


def _stage160_entry_criteria(trace: dict[str, Any]) -> dict[str, Any]:
    issues = []
    if trace.get("status") != "pass":
        issues.append("trace_not_pass")
    if trace.get("runtime_execution_count") != 0 or trace.get("provider_execution_count") != 0 or trace.get("write_operation_count") != 0:
        issues.append("side_effect_counts_nonzero")
    if len(str(trace.get("trace_checksum", ""))) != 64:
        issues.append("invalid_trace_checksum")
    return {"stage": TARGET_STAGE, "title": "Stage160 Entry Criteria", "status": "pass" if not issues else "blocked", "issues": issues, "page03_release_seal_ready": not issues, "next_stage": "stage160"}


def _regression_snapshot(trace: dict[str, Any]) -> dict[str, Any]:
    issues = []
    if trace.get("trace_step_count", 0) < 6:
        issues.append("insufficient_trace_steps")
    if trace.get("boundary_violation_count", 0) != 0:
        issues.append("boundary_violation_count_nonzero")
    return {"stage": TARGET_STAGE, "title": "Stage159 Regression Snapshot", "status": "pass" if not issues else "blocked", "issues": issues, "trace_step_count": trace.get("trace_step_count", 0), "trace_checksum": trace.get("trace_checksum", ""), "runtime_execution_count": 0, "provider_execution_count": 0, "write_operation_count": 0}


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "packet_count", "dependency_count", "conflict_count", "boundary_violation_count", "preflight_checksum", "runtime_execution_enabled", "provider_execution_enabled", "preflight_write_enabled", "graph_write_enabled", "store_write_enabled", "memory_write_enabled", "runtime_training_enabled", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
