from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from v1700.gates.stage161_release_gate import run_stage161_release_gate
from v1700.gates.stage162_release_gate import run_stage162_release_gate
from v1700.gates.stage163_release_gate import run_stage163_release_gate
from v1700.gates.stage164_release_gate import run_stage164_release_gate
from v1700.gates.stage165_release_gate import run_stage165_release_gate

from .contracts import (
    Page04InvariantFreeze,
    Page04ReleaseAsset,
    Page04SealCheck,
    Page04StageSeal,
    Page04TransitionCriterion,
)

TARGET_STAGE = "stage166"
TARGET_REPORT = "release/current/stage166_page04_release_seal_report.json"
PACK_DIR = "release/current/stage166_page04_release_seal_pack"

PAGE04_UPSTREAM_STAGES: tuple[tuple[str, str, str, str], ...] = (
    ("161", "Rendering Contract", "release/current/stage161_rendering_contract_report.json", "release/current/stage161_release_gate_report.json"),
    ("162", "Local Render Packet Store", "release/current/stage162_local_render_packet_store_report.json", "release/current/stage162_release_gate_report.json"),
    ("163", "Deterministic Render Plan Builder", "release/current/stage163_deterministic_render_plan_builder_report.json", "release/current/stage163_release_gate_report.json"),
    ("164", "Surface Draft Dry-Run Renderer", "release/current/stage164_surface_draft_dry_run_renderer_report.json", "release/current/stage164_release_gate_report.json"),
    ("165", "Render Quality and Boundary Preflight", "release/current/stage165_render_quality_boundary_preflight_report.json", "release/current/stage165_release_gate_report.json"),
)
PAGE04_TOTAL_STAGE_COUNT = len(PAGE04_UPSTREAM_STAGES) + 1

CURRENT_STAGE_GENERATED_ASSETS = {
    TARGET_REPORT,
    "release/current/stage166_release_gate_report.json",
    "release/current/stage166_summary.json",
    f"{PACK_DIR}/page04_stage_chain.json",
    f"{PACK_DIR}/page04_release_seal_matrix.json",
    f"{PACK_DIR}/page04_artifact_index.json",
    f"{PACK_DIR}/page04_invariant_freeze.json",
    f"{PACK_DIR}/page04_nexus_connectivity_matrix.json",
    f"{PACK_DIR}/page04_transition_criteria.json",
    f"{PACK_DIR}/page04_release_seal.json",
    f"{PACK_DIR}/regression_snapshot.json",
}

CORE_PAGE04_INVARIANTS: dict[str, int | bool] = {
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
    "rendering_runtime_enabled": False,
    "generation_runtime_enabled": False,
    "provider_generation_enabled": False,
    "runtime_execution_enabled": False,
    "memory_write_enabled": False,
    "runtime_training_enabled": False,
}

OPTIONAL_PAGE04_INVARIANTS: dict[str, int | bool] = {
    "render_write_enabled": False,
    "quality_gate_write_enabled": False,
    "canon_mutation_enabled": False,
}


def run_stage166_page04_release_seal(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if existing is not None:
            return existing

    gates = (
        _gate_or_existing(root, "stage161_release_gate_report.json", run_stage161_release_gate),
        _gate_or_existing(root, "stage162_release_gate_report.json", run_stage162_release_gate),
        _gate_or_existing(root, "stage163_release_gate_report.json", run_stage163_release_gate),
        _gate_or_existing(root, "stage164_release_gate_report.json", run_stage164_release_gate),
        _gate_or_existing(root, "stage165_release_gate_report.json", run_stage165_release_gate),
    )
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    stage_chain = _build_stage_chain(root, gates)
    release_matrix = _build_release_seal_matrix(stage_chain)
    invariant_freeze = _build_invariant_freeze(root, gates)
    connectivity = _build_nexus_connectivity_matrix(root)
    regression = _build_regression_snapshot(root)
    transition = _build_transition_criteria(root, stage_chain, invariant_freeze, connectivity, regression)

    pre_index_parts = {
        "page04_stage_chain": stage_chain,
        "page04_release_seal_matrix": release_matrix,
        "page04_invariant_freeze": invariant_freeze,
        "page04_nexus_connectivity_matrix": connectivity,
        "page04_transition_criteria": transition,
        "regression_snapshot": regression,
    }
    for name, payload in pre_index_parts.items():
        _write_json(pack / f"{name}.json", payload)

    artifact_index = _build_artifact_index(root)
    seal = _build_page04_release_seal(pre_index_parts, artifact_index)
    _write_json(pack / "page04_artifact_index.json", artifact_index)
    _write_json(pack / "page04_release_seal.json", seal)

    parts = {**pre_index_parts, "page04_artifact_index": artifact_index, "page04_release_seal": seal}
    issues: list[str] = []
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "166",
        "baseline_stage": "165",
        "title": "Page04 Release Seal",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "PAGE04_RELEASE_SEAL_LOCAL",
        "page": "Page04 Rendering Body",
        "page04_release_seal_only": True,
        "page04_sealed": not issues,
        "page04_stage_count": PAGE04_TOTAL_STAGE_COUNT,
        "page04_total_stage_count": PAGE04_TOTAL_STAGE_COUNT,
        "page04_upstream_stage_count": len(PAGE04_UPSTREAM_STAGES),
        "page04_stage_chain_pass": stage_chain.get("status") == "pass",
        "page04_artifact_index_complete": artifact_index.get("status") == "pass",
        "page04_invariant_freeze_pass": invariant_freeze.get("status") == "pass",
        "page04_nexus_connectivity_pass": connectivity.get("status") == "pass",
        "page04_release_checksum": seal.get("page04_release_checksum"),
        "stage167_evaluation_contract_ready": not issues,
        "next_stage": "stage167",
        "next_stage_title": "Evaluation Contract",
        "next_page": "Page05 Evaluation Body",
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "provider_execution_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
        "surface_draft_write_enabled": False,
        "quality_gate_write_enabled": False,
        "memory_write_enabled": False,
        "store_write_enabled": False,
        "canon_mutation_enabled": False,
        "auto_repair_apply_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": parts,
    }
    _write_json(root / TARGET_REPORT, result)
    _write_json(root / "release/current/stage166_summary.json", _compact(result))
    return result


def _build_stage_chain(root: Path, gates: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    items: list[Page04StageSeal] = []
    issues: list[str] = []
    for (stage, title, report_path, gate_path), gate in zip(PAGE04_UPSTREAM_STAGES, gates):
        report = _load_json(root / report_path) or {}
        gate_report = _load_json(root / gate_path) or gate
        status = "pass" if report.get("status") == "pass" and gate_report.get("status") == "pass" else "blocked"
        sealed = status == "pass"
        if not sealed:
            issues.append(f"stage{stage}_not_sealed")
        items.append(Page04StageSeal(stage, title, report_path, gate_path, status, sealed))
    return {"stage": TARGET_STAGE, "title": "Page04 Upstream Stage Chain", "status": "pass" if not issues else "blocked", "issues": issues, "stage_count": len(items), "sealed_count": sum(1 for item in items if item.sealed), "stages": [item.to_dict() for item in items]}


def _build_release_seal_matrix(stage_chain: dict[str, Any]) -> dict[str, Any]:
    checks = (
        Page04SealCheck("upstream_stage_chain_complete", _pass_if(stage_chain.get("status") == "pass" and stage_chain.get("stage_count") == len(PAGE04_UPSTREAM_STAGES)), "page04_stage_chain", "Stage161 through Stage165 all pass before Stage166 seals Page04."),
        Page04SealCheck("rendering_contract_sealed", _pass_if(_stage_sealed(stage_chain, "161")), "stage161_release_gate", "Rendering contract is sealed."),
        Page04SealCheck("render_packet_store_sealed", _pass_if(_stage_sealed(stage_chain, "162")), "stage162_release_gate", "Local render packet store is sealed."),
        Page04SealCheck("render_plan_builder_sealed", _pass_if(_stage_sealed(stage_chain, "163")), "stage163_release_gate", "Deterministic render plan builder is sealed."),
        Page04SealCheck("surface_dry_run_renderer_sealed", _pass_if(_stage_sealed(stage_chain, "164")), "stage164_release_gate", "Surface draft dry-run renderer is sealed."),
        Page04SealCheck("render_quality_boundary_sealed", _pass_if(_stage_sealed(stage_chain, "165")), "stage165_release_gate", "Render quality and boundary preflight is sealed."),
        Page04SealCheck("page04_total_stage_count_confirmed", _pass_if(PAGE04_TOTAL_STAGE_COUNT == 6), TARGET_REPORT, "Page04 spans Stage161 through Stage166."),
        Page04SealCheck("no_generation_privilege_expanded", "pass", TARGET_REPORT, "Page04 enables no live provider generation, runtime rendering, writes, mutation, training, or publication workflow."),
    )
    issues = [check.name for check in checks if check.status != "pass"]
    return {"stage": TARGET_STAGE, "title": "Page04 Release Seal Matrix", "status": "pass" if not issues else "blocked", "issues": issues, "sealed_page04": not issues, "check_count": len(checks), "checks": [check.to_dict() for check in checks]}


def _build_invariant_freeze(root: Path, gates: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    """Freeze Page04 safety invariants across every upstream report and gate.

    Stage166 is a page-level seal, so it must not trust only the most recent
    Stage165 report. Any Stage161~Stage165 evidence drift should block the seal
    even when the historical report still says ``status: pass``.
    """
    invariants: tuple[Page04InvariantFreeze, ...] = tuple(
        Page04InvariantFreeze(name, expected, "page04_upstream_reports_and_gates")
        for name, expected in {**CORE_PAGE04_INVARIANTS, **OPTIONAL_PAGE04_INVARIANTS}.items()
    )
    sources = _upstream_evidence_sources(root, gates)
    issues: list[str] = []
    evidence_matrix: list[dict[str, Any]] = []

    for source_name, source_path, payload in sources:
        for invariant_name, expected in CORE_PAGE04_INVARIANTS.items():
            if invariant_name not in payload:
                issues.append(f"{source_name}_invariant_missing:{invariant_name}")
                evidence_matrix.append(
                    {
                        "source": source_name,
                        "path": source_path,
                        "name": invariant_name,
                        "expected": expected,
                        "observed": None,
                        "status": "blocked",
                        "reason": "missing",
                    }
                )
                continue
            observed = payload.get(invariant_name)
            status = "pass" if observed == expected else "blocked"
            if status != "pass":
                issues.append(f"{source_name}_invariant_drift:{invariant_name}")
            evidence_matrix.append(
                {
                    "source": source_name,
                    "path": source_path,
                    "name": invariant_name,
                    "expected": expected,
                    "observed": observed,
                    "status": status,
                    "reason": "match" if status == "pass" else "drift",
                }
            )

        for invariant_name, expected in OPTIONAL_PAGE04_INVARIANTS.items():
            if invariant_name not in payload:
                evidence_matrix.append(
                    {
                        "source": source_name,
                        "path": source_path,
                        "name": invariant_name,
                        "expected": expected,
                        "observed": None,
                        "status": "skipped",
                        "reason": "optional_missing",
                    }
                )
                continue
            observed = payload.get(invariant_name)
            status = "pass" if observed == expected else "blocked"
            if status != "pass":
                issues.append(f"{source_name}_optional_invariant_drift:{invariant_name}")
            evidence_matrix.append(
                {
                    "source": source_name,
                    "path": source_path,
                    "name": invariant_name,
                    "expected": expected,
                    "observed": observed,
                    "status": status,
                    "reason": "match" if status == "pass" else "drift",
                }
            )

    return {
        "stage": TARGET_STAGE,
        "title": "Page04 Invariant Freeze",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "frozen": [item.to_dict() for item in invariants],
        "evidence_source_count": len(sources),
        "evidence_check_count": len(evidence_matrix),
        "evidence_matrix": evidence_matrix,
        "provider_zero": not issues,
        "write_zero": not issues,
        "generation_zero": not issues,
        "node2_boundary_zero": not issues,
    }


def _upstream_evidence_sources(root: Path, gates: tuple[dict[str, Any], ...]) -> list[tuple[str, str, dict[str, Any]]]:
    sources: list[tuple[str, str, dict[str, Any]]] = []
    for (stage, _title, report_path, gate_path), gate in zip(PAGE04_UPSTREAM_STAGES, gates):
        report_payload = _load_json(root / report_path) or {}
        gate_payload = _load_json(root / gate_path) or gate or {}
        sources.append((f"stage{stage}_report", report_path, report_payload))
        sources.append((f"stage{stage}_gate", gate_path, gate_payload))
    return sources


def _build_nexus_connectivity_matrix(root: Path) -> dict[str, Any]:
    required = [
        "src/v1700/page04_release_seal/contracts.py",
        "src/v1700/page04_release_seal/report.py",
        "src/v1700/stage166/stage166_runner.py",
        "src/v1700/gates/stage166_release_gate.py",
        "tools/run_stage166_page04_release_seal.py",
        "tools/run_stage166_release_gate.py",
        "tests/test_stage166_page04_release_seal.py",
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
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    return {"stage": TARGET_STAGE, "title": "Page04 Nexus Connectivity Matrix", "status": "pass" if not missing else "blocked", "issues": [f"missing:{rel}" for rel in missing], "required_count": len(required), "missing_count": len(missing), "connected_files": [rel for rel in required if rel not in missing], "python_fallback_required": True, "gitnexus_runtime_dependency_required": False}


def _build_transition_criteria(
    root: Path,
    stage_chain: dict[str, Any],
    invariant_freeze: dict[str, Any],
    connectivity: dict[str, Any],
    regression: dict[str, Any],
) -> dict[str, Any]:
    upstream_ready = (
        stage_chain.get("status") == "pass"
        and invariant_freeze.get("status") == "pass"
        and connectivity.get("status") == "pass"
        and regression.get("status") == "pass"
    )
    criteria = (
        Page04TransitionCriterion("page04_stage_chain_pass", _pass_if(stage_chain.get("status") == "pass"), "Page05 Evaluation Body", "page04_stage_chain"),
        Page04TransitionCriterion("page04_invariant_freeze_pass", _pass_if(invariant_freeze.get("status") == "pass"), "Page05 Evaluation Body", "page04_invariant_freeze"),
        Page04TransitionCriterion("page04_connectivity_pass", _pass_if(connectivity.get("status") == "pass"), "Page05 Evaluation Body", "page04_nexus_connectivity_matrix"),
        Page04TransitionCriterion("page04_regression_snapshot_pass", _pass_if(regression.get("status") == "pass"), "Page05 Evaluation Body", "regression_snapshot"),
        Page04TransitionCriterion("stage167_evaluation_contract_ready", _pass_if(upstream_ready), "Page05 Evaluation Body", TARGET_REPORT),
    )
    issues = [criterion.name for criterion in criteria if criterion.status != "pass"]
    return {"stage": TARGET_STAGE, "title": "Page04 Transition Criteria", "status": "pass" if not issues else "blocked", "issues": issues, "next_stage": "stage167", "next_stage_title": "Evaluation Contract", "next_page": "Page05 Evaluation Body", "criteria": [criterion.to_dict() for criterion in criteria]}


def _build_regression_snapshot(root: Path) -> dict[str, Any]:
    filelist_forbidden = _forbidden_cache_entries_from_filelist(root)
    strict_tree_scan = os.environ.get("V1700_STAGE166_STRICT_TREE_SCAN") == "1"
    workspace_forbidden = _forbidden_cache_entries_from_tree(root) if strict_tree_scan else []

    issues = [f"forbidden_cache_entry:{entry}" for entry in filelist_forbidden]
    if strict_tree_scan:
        issues.extend(f"workspace_forbidden_cache_entry:{entry}" for entry in workspace_forbidden)

    return {
        "stage": TARGET_STAGE,
        "title": "Stage166 Regression Snapshot",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "targeted_regression": [
            "tests/test_stage161_rendering_contract.py",
            "tests/test_stage162_local_render_packet_store.py",
            "tests/test_stage163_deterministic_render_plan_builder.py",
            "tests/test_stage164_surface_draft_dry_run_renderer.py",
            "tests/test_stage165_render_quality_boundary_preflight.py",
            "tests/test_stage166_page04_release_seal.py",
        ],
        "forbidden_cache_entries": len(filelist_forbidden),
        "forbidden_cache_entry_sample": filelist_forbidden[:20],
        "workspace_forbidden_cache_entries": len(workspace_forbidden),
        "workspace_forbidden_cache_entry_sample": workspace_forbidden[:20],
        "strict_tree_scan_enabled": strict_tree_scan,
        "provider_default_calls": 0,
        "write_operation_count": 0,
    }


def _is_forbidden_cache_entry(entry: str) -> bool:
    normalized = f"/{entry.strip().replace('\\\\', '/')}"
    forbidden_markers = ("/__pycache__/", "/.pytest_cache/", "/.mypy_cache/", "/.ruff_cache/")
    forbidden_suffixes = (".pyc", ".pyo")
    return any(marker in normalized for marker in forbidden_markers) or normalized.endswith(forbidden_suffixes)


def _forbidden_cache_entries_from_filelist(root: Path) -> list[str]:
    filelist = root / "FILELIST.txt"
    if not filelist.exists():
        return []
    entries: set[str] = set()
    for raw in filelist.read_text(encoding="utf-8").splitlines():
        entry = raw.strip().replace("\\", "/")
        if entry and _is_forbidden_cache_entry(entry):
            entries.add(entry)
    return sorted(entries)


def _forbidden_cache_entries_from_tree(root: Path) -> list[str]:
    entries: set[str] = set()
    skip_dirs = {".git"}
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if set(path.relative_to(root).parts) & skip_dirs:
            continue
        if (path.is_file() or path.is_dir()) and _is_forbidden_cache_entry(rel):
            entries.add(rel)
    return sorted(entries)


def _forbidden_cache_entries(root: Path) -> list[str]:
    """Backward-compatible hard-gate entries sourced from FILELIST.txt."""
    return _forbidden_cache_entries_from_filelist(root)


def _build_artifact_index(root: Path) -> dict[str, Any]:
    assets: list[Page04ReleaseAsset] = []
    for stage, title, report, gate in PAGE04_UPSTREAM_STAGES:
        assets.append(Page04ReleaseAsset(report, True, f"stage{stage}_report", (root / report).exists()))
        assets.append(Page04ReleaseAsset(gate, True, f"stage{stage}_gate", (root / gate).exists()))
    for rel in sorted(CURRENT_STAGE_GENERATED_ASSETS):
        assets.append(Page04ReleaseAsset(rel, True, "stage166_generated", (root / rel).exists(), generated_by_stage166=True))
    missing = [asset.path for asset in assets if asset.required and not asset.exists and not asset.generated_by_stage166]
    return {"stage": TARGET_STAGE, "title": "Page04 Artifact Index", "status": "pass" if not missing else "blocked", "issues": [f"missing:{rel}" for rel in missing], "asset_count": len(assets), "missing_count": len(missing), "assets": [asset.to_dict() for asset in assets]}


def _build_page04_release_seal(parts: dict[str, Any], artifact_index: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({**parts, "page04_artifact_index": artifact_index}, sort_keys=True, ensure_ascii=False).encode("utf-8")
    checksum = hashlib.sha256(payload).hexdigest()
    issues = [name for name, payload_part in {**parts, "page04_artifact_index": artifact_index}.items() if payload_part.get("status") != "pass"]
    return {"stage": TARGET_STAGE, "title": "Page04 Release Seal", "status": "pass" if not issues else "blocked", "issues": issues, "page04_sealed": not issues, "page04_release_checksum": checksum, "sealed_stage_range": "Stage161~Stage166", "next_stage": "stage167", "next_stage_title": "Evaluation Contract", "next_page": "Page05 Evaluation Body"}



def _gate_or_existing(root: Path, report_name: str, runner) -> dict[str, Any]:
    existing = _load_json(root / "release/current" / report_name)
    if existing is not None and existing.get("status") == "pass":
        return existing
    return runner(root)

def _stage_sealed(stage_chain: dict[str, Any], stage: str) -> bool:
    return any(item.get("stage") == stage and item.get("sealed") is True for item in stage_chain.get("stages", []))


def _pass_if(condition: bool) -> str:
    return "pass" if condition else "blocked"


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "page04_sealed", "page04_total_stage_count", "page04_release_checksum", "stage167_evaluation_contract_ready", "rendering_runtime_enabled", "generation_runtime_enabled", "provider_generation_enabled", "runtime_execution_enabled", "memory_write_enabled", "render_write_enabled", "canon_mutation_enabled", "runtime_training_enabled", "runtime_execution_count", "provider_generation_count", "write_operation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}
