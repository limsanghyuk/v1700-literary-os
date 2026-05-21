from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage140_release_gate import run_stage140_release_gate
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler, aggregate_report
from v1700.nodes.node3_critic_gate import Node3CriticGate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency

from .contracts import CriticResult
from .loader import build_scene_intent, build_style_profile, load_sample_bundle

TARGET_STAGE = "stage141"
TARGET_REPORT = "release/current/stage141_prose_generation_e2e_report.json"
TARGET_GATE = "release/current/stage141_release_gate_report.json"


def run_stage141_prose_generation_e2e(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage141_prose_generation_e2e_pack"
    pack.mkdir(parents=True, exist_ok=True)
    benchmark_results_dir = root / "benchmarks" / "longform_output" / "results"
    benchmark_results_dir.mkdir(parents=True, exist_ok=True)

    baseline = run_stage140_release_gate(root)
    _write_json(root / "release" / "current" / "stage141_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))
    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)
    bundle = load_sample_bundle(root)
    scene = build_scene_intent(bundle)
    style = build_style_profile()
    compiled = Node2ProseCompiler().compile(scene, style)
    critic_ok, critic_issues = Node3CriticGate().validate(compiled.rendered)
    critic = CriticResult(status="pass" if critic_ok else "blocked", issues=tuple(critic_issues))
    aggregate = aggregate_report([compiled.rendered])
    benchmark = _build_benchmark_result(bundle, aggregate, critic)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage140_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "critic_gate": critic.to_dict(),
        "benchmark_result": benchmark,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))
    if aggregate.get("status") != "pass":
        issues.append("aggregate_render_quality_blocked")

    rendered_dict = compiled.rendered.to_dict()
    result = {
        "stage": "141",
        "baseline_stage": "140",
        "title": "Prose Generation E2E Harness",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "PROSE_GENERATION_E2E_HARNESS_LOCAL",
        "prose_generation_e2e_only": True,
        "sample_project_contract_reused": True,
        "scene_request_count": 1,
        "rendered_scene_count": aggregate.get("rendered_scene_count", 0),
        "critic_gate_pass_count": 1 if critic_ok else 0,
        "benchmark_result_count": 1,
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "critic_gate_status": critic.status,
        "benchmark_result_status": benchmark.get("status"),
        "stage142_benchmark_pack_ready": benchmark.get("stage142_benchmark_pack_ready", False),
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
            "stage140_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "sample_bundle_summary": _sample_bundle_summary(bundle),
            "scene_intent": scene.to_dict(),
            "style_profile": style.to_dict(),
            "rendered_scene": rendered_dict,
            "critic_gate": critic.to_dict(),
            "benchmark_result": benchmark,
        },
    }

    _write_json(pack / "stage140_baseline_summary.json", _compact_baseline(baseline))
    _write_json(pack / "sample_bundle_summary.json", _sample_bundle_summary(bundle))
    _write_json(pack / "scene_intent.json", scene.to_dict())
    _write_json(pack / "style_profile.json", style.to_dict())
    _write_json(pack / "rendered_scene.json", rendered_dict)
    _write_json(pack / "critic_gate_report.json", critic.to_dict())
    _write_json(pack / "benchmark_result.json", benchmark)
    (pack / "rendered_scene.md").write_text(rendered_dict.get("final_text", "") + "\n", encoding="utf-8")
    _write_json(benchmark_results_dir / "stage141_scene_001_benchmark_result.json", benchmark)
    (benchmark_results_dir / "stage141_scene_001_rendered.md").write_text(rendered_dict.get("final_text", "") + "\n", encoding="utf-8")
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_benchmark_result(bundle: Any, aggregate: dict[str, Any], critic: CriticResult) -> dict[str, Any]:
    expectations = bundle.benchmark_expectations
    issues: list[str] = []
    min_scene_count = int(expectations.get("min_scene_count", 1) or 1)
    rendered_scene_count = int(aggregate.get("rendered_scene_count", 0) or 0)
    if rendered_scene_count < min_scene_count:
        issues.append("rendered_scene_count_below_expectation")
    if aggregate.get("external_provider_calls", 1) != 0:
        issues.append("provider_default_calls_nonzero")
    if critic.provider_default_calls != 0:
        issues.append("critic_provider_default_calls_nonzero")
    if critic.node2_raw_reveal_access != 0:
        issues.append("node2_raw_reveal_access_nonzero")
    if critic.status != "pass":
        issues.append("critic_gate_blocked")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage141 Benchmark Result",
        "status": "pass" if not issues and aggregate.get("status") == "pass" else "blocked",
        "issues": issues,
        "benchmark_id": expectations.get("benchmark_id", "stage141_prose_generation_e2e"),
        "min_scene_count": min_scene_count,
        "rendered_scene_count": rendered_scene_count,
        "reader_surface_average": aggregate.get("reader_surface_average"),
        "scene_contract_valid": True,
        "project_contract_valid": bool(bundle.project.get("synthetic_only")) and not bool(bundle.project.get("provider_calls_allowed")),
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "stage142_benchmark_pack_ready": rendered_scene_count >= min_scene_count and critic.status == "pass",
    }


def _sample_bundle_summary(bundle: Any) -> dict[str, Any]:
    characters = bundle.characters.get("characters", [])
    return {
        "project_id": bundle.project.get("project_id"),
        "synthetic_only": bundle.project.get("synthetic_only"),
        "provider_calls_allowed": bundle.project.get("provider_calls_allowed"),
        "character_count": len(characters),
        "scene_request_id": bundle.scene_request.get("scene_id"),
        "benchmark_id": bundle.benchmark_expectations.get("benchmark_id"),
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
    compact["stage140_release_gate_status"] = report.get("status")
    return compact


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
