from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage153_release_gate import run_stage153_release_gate
from v1700.stage154 import run_stage154

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage154_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage154":
        existing = _load_report(root, "stage154_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage154(root)
    parts = stage.get("parts", {})
    stage_chain = parts.get("page02_stage_chain", {})
    seal_matrix = parts.get("page02_release_seal_matrix", {})
    blocker_registry = parts.get("page02_blocker_registry", {})
    artifact_index = parts.get("page02_artifact_index", {})
    lineage = parts.get("page02_lineage_evidence_index", {})
    boundary_freeze = parts.get("page02_boundary_freeze", {})

    checks = {
        "stage153_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage154_report_pass": _check(stage.get("status") == "pass"),
        "page02_release_seal_mode_pass": _check(stage.get("page02_release_seal_only") is True and stage.get("mode") == "PAGE02_RELEASE_SEAL_LOCAL"),
        "page02_stage_chain_pass": _check(stage_chain.get("status") == "pass" and stage_chain.get("stage_count") == 4),
        "page02_release_seal_matrix_pass": _check(seal_matrix.get("status") == "pass" and seal_matrix.get("sealed_page02") is True),
        "page02_blocker_registry_pass": _check(blocker_registry.get("status") == "pass" and blocker_registry.get("blocker_count", 0) == blocker_registry.get("blocked_capability_count", -1)),
        "page02_artifact_index_pass": _check(artifact_index.get("status") == "pass" and artifact_index.get("missing_count") == 0),
        "page02_lineage_evidence_pass": _check(lineage.get("status") == "pass" and lineage.get("lineage_evidence_complete") is True),
        "page02_boundary_freeze_pass": _check(boundary_freeze.get("status") == "pass"),
        "stage155_entry_ready": _check(stage.get("stage155_entry_ready") is True),
        "memory_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("store_write_enabled") is False and stage.get("query_write_enabled") is False),
        "vector_db_runtime_dependency_blocked": _check(stage.get("vector_db_runtime_dependency") is False),
        "live_provider_rag_blocked": _check(stage.get("live_provider_rag_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "canon_auto_resolution_zero": _check(stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_mutation_zero": _check(stage.get("auto_repair_mutation_count") == 0),
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
        "stage": "154",
        "baseline_stage": "153",
        "title": "Page02 Release Seal",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage154": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage154_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage154":
        report = _load_report(root, "stage153_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage153_release_gate(root)


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
        "status", "stage", "baseline_stage", "title", "issues", "mode",
        "page02_release_seal_only", "page02_sealed", "page02_stage_count",
        "page02_stage_chain_pass", "page02_artifact_index_complete",
        "page02_boundary_freeze_pass", "stage155_entry_ready",
        "memory_write_enabled", "store_write_enabled", "query_write_enabled",
        "vector_db_runtime_dependency", "live_provider_rag_enabled",
        "runtime_training_enabled", "active_meta_learning_enabled",
        "model_weight_update_count", "canon_auto_resolution_count",
        "auto_repair_mutation_count", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "boundary_violation_count", "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage", "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage154.md",
            "docs/proposals/stage154_page02_release_seal_proposal.md",
            "docs/architecture/stage154_page02_release_seal_blueprint.md",
            "docs/development/stage154_developer_handoff.md",
            "manifests/stage154_manifest.json",
            "manifests/stage154_page02_release_seal_manifest.json",
            "manifests/stage154_branchpoint_trace_manifest.json",
            "manifests/live_core_stage154_overlay.json",
            "release/current/stage154_page02_release_seal_report.json",
            "release/current/stage154_release_asset_manifest.json",
            "release/current/stage154_page02_release_seal_pack/page02_stage_chain.json",
            "release/current/stage154_page02_release_seal_pack/page02_release_seal_matrix.json",
            "release/current/stage154_page02_release_seal_pack/page02_blocker_registry.json",
            "release/current/stage154_page02_release_seal_pack/page02_artifact_index.json",
            "release/current/stage154_page02_release_seal_pack/page02_lineage_evidence_index.json",
            "release/current/stage154_page02_release_seal_pack/page02_boundary_freeze.json",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage154", "run_stage154_page02_release_seal.py", "run_stage154_release_gate.py"])
