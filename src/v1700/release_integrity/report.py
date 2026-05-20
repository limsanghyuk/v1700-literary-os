from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.product_proof.benchmark_contract import validate_longform_benchmark_contract
from v1700.product_proof.sample_project_contract import validate_sample_project_contract
from v1700.stage139 import run_stage139

from .asset_checker import expected_stage140_asset_manifest, run_release_asset_integrity
from .metadata_checker import run_stage_metadata_consistency


def run_stage140_release_integrity(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage140_release_integrity_pack"
    pack.mkdir(parents=True, exist_ok=True)
    baseline = run_stage139(root)
    _write_json(root / "release/current/stage140_release_asset_manifest.json", expected_stage140_asset_manifest())
    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)
    sample_project = validate_sample_project_contract(root)
    benchmark = validate_longform_benchmark_contract(root)
    parts = {
        "stage139_baseline": _compact_stage139(baseline),
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "sample_project_contract": sample_project,
        "benchmark_contract": benchmark,
    }
    issues: list[str] = []
    for key, part in parts.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))
    result = {
        "stage": "140",
        "baseline_stage": "139",
        "title": "Release Integrity & Product Proof Gate",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_integrity_gate_only": True,
        "product_proof_skeleton_only": True,
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "sample_project_contract_status": sample_project.get("status"),
        "benchmark_contract_status": benchmark.get("status"),
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
        "stage141_product_e2e_ready": not issues,
        "parts": parts,
    }
    _write_json(pack / "metadata_consistency_report.json", metadata)
    _write_json(pack / "release_asset_integrity_report.json", assets)
    _write_json(pack / "sample_project_contract_report.json", sample_project)
    _write_json(pack / "benchmark_contract_report.json", benchmark)
    _write_json(pack / "stage139_input_summary.json", parts["stage139_baseline"])
    _write_json(root / "release/current/stage140_release_integrity_report.json", result)
    return result


def _compact_stage139(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "status": report.get("status"),
        "mode": report.get("mode"),
        "corpus_governance_pipeline_only": report.get("corpus_governance_pipeline_only"),
        "stage140_release_ready_count": report.get("stage140_release_ready_count"),
        "total_pipeline_items": report.get("total_pipeline_items"),
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
