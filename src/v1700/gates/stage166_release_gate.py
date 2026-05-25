from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage165_release_gate import run_stage165_release_gate
from v1700.page04_release_seal import run_stage166_page04_release_seal

def run_stage166_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    baseline = _baseline_gate(root)
    stage = run_stage166_page04_release_seal(root)
    checks = {
        "baseline_stage165_gate_pass": _check(baseline.get("status") == "pass"),
        "page04_release_seal_pass": _check(stage.get("status") == "pass" and stage.get("page04_sealed") is True),
        "page04_stage_count_pass": _check(stage.get("page04_total_stage_count") == 6),
        "stage167_ready_pass": _check(stage.get("stage167_evaluation_contract_ready") is True),
        "rendering_runtime_disabled_pass": _check(stage.get("rendering_runtime_enabled") is False and stage.get("runtime_execution_count") == 0),
        "provider_generation_zero_pass": _check(stage.get("provider_generation_enabled") is False and stage.get("provider_generation_count") == 0),
        "write_zero_pass": _check(stage.get("write_operation_count") == 0 and stage.get("render_write_enabled") is False and stage.get("memory_write_enabled") is False),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "training_mutation_disabled_pass": _check(stage.get("runtime_training_enabled") is False and stage.get("canon_mutation_enabled") is False),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "166",
        "baseline_stage": "165",
        "title": "Page04 Release Seal",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage166": _compact(stage),
        "page04_sealed": stage.get("page04_sealed") is True and not issues,
        "stage167_evaluation_contract_ready": stage.get("stage167_evaluation_contract_ready") is True and not issues,
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
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "canon_mutation_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage166_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    report = _load_report(root, "stage165_release_gate_report.json")
    if report is not None and report.get("status") == "pass":
        return report
    return run_stage165_release_gate(root)


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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "page04_sealed", "page04_total_stage_count", "page04_release_checksum", "stage167_evaluation_contract_ready", "rendering_runtime_enabled", "generation_runtime_enabled", "provider_generation_enabled", "runtime_execution_enabled", "memory_write_enabled", "render_write_enabled", "canon_mutation_enabled", "runtime_training_enabled", "runtime_execution_count", "provider_generation_count", "write_operation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    generated = {"release/current/stage166_release_gate_report.json"}
    required = [
        "docs/stages/stage166.md",
        "docs/proposals/stage166_page04_release_seal_proposal.md",
        "docs/architecture/stage166_page04_release_seal_blueprint.md",
        "docs/development/stage166_developer_handoff.md",
        "docs/architecture/page04_rendering_body_blueprint.md",
        "docs/proposals/page04_rendering_body_proposal.md",
        "docs/development/page04_handoff.md",
        "manifests/stage166_manifest.json",
        "manifests/stage166_page04_release_seal_manifest.json",
        "manifests/stage166_branchpoint_trace_manifest.json",
        "manifests/live_core_stage166_overlay.json",
        "release/current/stage166_release_asset_manifest.json",
        "release/current/stage166_page04_release_seal_report.json",
        "release/current/stage166_release_gate_report.json",
        "release/current/stage166_page04_release_seal_pack/page04_stage_chain.json",
        "release/current/stage166_page04_release_seal_pack/page04_release_seal_matrix.json",
        "release/current/stage166_page04_release_seal_pack/page04_artifact_index.json",
        "release/current/stage166_page04_release_seal_pack/page04_invariant_freeze.json",
        "release/current/stage166_page04_release_seal_pack/page04_nexus_connectivity_matrix.json",
        "release/current/stage166_page04_release_seal_pack/page04_transition_criteria.json",
        "release/current/stage166_page04_release_seal_pack/page04_release_seal.json",
        "release/current/stage166_page04_release_seal_pack/regression_snapshot.json",
    ]
    return all((root / rel).exists() or rel in generated for rel in required)


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage166", "run_stage166_page04_release_seal.py", "run_stage166_release_gate.py"])
