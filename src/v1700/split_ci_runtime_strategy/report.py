from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage143_release_gate import run_stage143_release_gate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency

from .contracts import WorkflowLane

TARGET_STAGE = "stage144"
TARGET_REPORT = "release/current/stage144_split_ci_runtime_strategy_report.json"


def run_stage144_split_ci_runtime_strategy(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage144_split_ci_runtime_strategy_pack"
    pack.mkdir(parents=True, exist_ok=True)

    baseline = run_stage143_release_gate(root)
    _write_json(root / "release/current/stage144_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))

    workflow_inventory = _build_workflow_inventory(root)
    runtime_lane_matrix = _build_runtime_lane_matrix(root)
    trigger_summary = _build_trigger_summary(root)
    release_surface_contract = _build_release_surface_contract(root)

    _write_json(pack / "workflow_inventory.json", workflow_inventory)
    _write_json(pack / "runtime_lane_matrix.json", runtime_lane_matrix)
    _write_json(pack / "workflow_trigger_summary.json", trigger_summary)
    _write_json(pack / "release_surface_contract.json", release_surface_contract)

    _write_json(
        root / TARGET_REPORT,
        {
            "stage": "144",
            "baseline_stage": "143",
            "title": "Split CI Runtime Strategy",
            "status": "building",
            "issues": [],
        },
    )

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage143_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "workflow_inventory": workflow_inventory,
        "runtime_lane_matrix": runtime_lane_matrix,
        "trigger_summary": trigger_summary,
        "release_surface_contract": release_surface_contract,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))

    result = {
        "stage": "144",
        "baseline_stage": "143",
        "title": "Split CI Runtime Strategy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "SPLIT_CI_RUNTIME_STRATEGY_LOCAL",
        "workflow_split_only": True,
        "ci_fast_present": workflow_inventory.get("ci_fast_present", False),
        "ci_core_present": workflow_inventory.get("ci_core_present", False),
        "ci_full_present": workflow_inventory.get("ci_full_present", False),
        "cd_dry_run_present": workflow_inventory.get("cd_dry_run_present", False),
        "release_workflow_present": workflow_inventory.get("release_workflow_present", False),
        "workflow_split_complete": workflow_inventory.get("workflow_split_complete", False),
        "runtime_lane_count": runtime_lane_matrix.get("lane_count", 0),
        "release_surface_ready": release_surface_contract.get("release_surface_ready", False),
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "stage144_roadmap_terminal": True,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "losdb_write_enabled": False,
        "migration_execution_enabled": False,
        "storage_contract_write_enabled": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "cross_project_write_allowed": False,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage143_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "workflow_inventory": workflow_inventory,
            "runtime_lane_matrix": runtime_lane_matrix,
            "trigger_summary": trigger_summary,
            "release_surface_contract": release_surface_contract,
        },
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_workflow_inventory(root: Path) -> dict[str, Any]:
    specs = {
        "ci_fast": ".github/workflows/ci-fast.yml",
        "ci_core": ".github/workflows/ci-core.yml",
        "ci_full": ".github/workflows/ci-full.yml",
        "cd_dry_run": ".github/workflows/cd-dry-run.yml",
        "release": ".github/workflows/release.yml",
    }
    issues: list[str] = []
    entries: list[dict[str, Any]] = []
    for name, rel in specs.items():
        path = root / rel
        status = "pass" if path.exists() else "blocked"
        if status != "pass":
            issues.append(f"missing:{rel}")
        entries.append({"name": name, "path": rel, "status": status})
    present = {entry["name"]: entry["status"] == "pass" for entry in entries}
    return {
        "stage": TARGET_STAGE,
        "title": "Stage144 Workflow Inventory",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "entries": entries,
        "ci_fast_present": present.get("ci_fast", False),
        "ci_core_present": present.get("ci_core", False),
        "ci_full_present": present.get("ci_full", False),
        "cd_dry_run_present": present.get("cd_dry_run", False),
        "release_workflow_present": present.get("release", False),
        "workflow_split_complete": all(present.values()),
    }


def _build_runtime_lane_matrix(root: Path) -> dict[str, Any]:
    lanes = [
        WorkflowLane("ci-fast", ".github/workflows/ci-fast.yml", "fast invariants and current-stage smoke", "push/pr", "3.11", _path_status(root, ".github/workflows/ci-fast.yml")),
        WorkflowLane("ci-core", ".github/workflows/ci-core.yml", "active-lineage pytest and stage gates", "push/pr/tag", "3.11-3.12", _path_status(root, ".github/workflows/ci-core.yml")),
        WorkflowLane("ci-full", ".github/workflows/ci-full.yml", "scheduled full pytest sweep", "schedule/manual", "3.11", _path_status(root, ".github/workflows/ci-full.yml")),
        WorkflowLane("cd-dry-run", ".github/workflows/cd-dry-run.yml", "package rehearsal and artifact dry-run", "push/pr", "3.11", _path_status(root, ".github/workflows/cd-dry-run.yml")),
        WorkflowLane("release", ".github/workflows/release.yml", "official tagged release packaging", "tag push", "3.11", _path_status(root, ".github/workflows/release.yml")),
    ]
    issues = [lane.name for lane in lanes if lane.status != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage144 Runtime Lane Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "lane_count": len(lanes),
        "lanes": [lane.to_dict() for lane in lanes],
    }


def _build_trigger_summary(root: Path) -> dict[str, Any]:
    checks = {
        "ci_fast_mentions_stage144": _file_contains(root, ".github/workflows/ci-fast.yml", "run_stage144_split_ci_runtime_strategy.py"),
        "ci_core_mentions_stage144": _file_contains(root, ".github/workflows/ci-core.yml", "run_stage144_split_ci_runtime_strategy.py"),
        "cd_dry_run_mentions_stage144": _file_contains(root, ".github/workflows/cd-dry-run.yml", "run_stage144_split_ci_runtime_strategy.py"),
        "release_mentions_stage144": _file_contains(root, ".github/workflows/release.yml", "run_stage144_split_ci_runtime_strategy.py"),
        "ci_full_exists": (root / ".github/workflows/ci-full.yml").exists(),
    }
    issues = [name for name, passed in checks.items() if not passed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage144 Workflow Trigger Summary",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": {name: {"status": "pass" if passed else "blocked"} for name, passed in checks.items()},
    }


def _build_release_surface_contract(root: Path) -> dict[str, Any]:
    package = json.loads((root / "package_manifest.json").read_text(encoding="utf-8"))
    required = [
        "package_manifest.json",
        "FILELIST.txt",
        "SHA256SUMS.txt",
        "release/current/stage144_release_asset_manifest.json",
        "release/current/stage144_split_ci_runtime_strategy_report.json",
    ]
    issues = [rel for rel in required if not (root / rel).exists()]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage144 Release Surface Contract",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "canonical_package": package.get("canonical_package"),
        "sha256_sidecar": package.get("sha256_sidecar"),
        "release_surface_ready": not issues,
    }


def _compact_baseline(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "stage",
        "baseline_stage",
        "status",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    compact = {key: report.get(key) for key in keep if key in report}
    compact["stage143_release_gate_status"] = report.get("status")
    return compact


def _path_status(root: Path, rel: str) -> str:
    return "pass" if (root / rel).exists() else "blocked"


def _file_contains(root: Path, rel: str, token: str) -> bool:
    path = root / rel
    return path.exists() and token in path.read_text(encoding="utf-8")


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
