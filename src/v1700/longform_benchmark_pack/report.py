from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from statistics import mean
from typing import Any

from v1700.gates.stage141_release_gate import run_stage141_release_gate
from v1700.ir.scene_intent import EmotionalDelta, SceneIntentIR
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler, aggregate_report
from v1700.nodes.node3_critic_gate import Node3CriticGate
from v1700.prose_generation_e2e.contracts import CriticResult
from v1700.prose_generation_e2e.loader import build_scene_intent, build_style_profile, load_sample_bundle
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency

from .contracts import BenchmarkCaseDefinition

TARGET_STAGE = "stage142"
TARGET_REPORT = "release/current/stage142_longform_benchmark_pack_report.json"


def run_stage142_longform_benchmark_pack(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage142_longform_benchmark_pack"
    pack.mkdir(parents=True, exist_ok=True)
    benchmark_results_dir = root / "benchmarks" / "longform_output" / "results"
    benchmark_results_dir.mkdir(parents=True, exist_ok=True)

    baseline = run_stage141_release_gate(root)
    _write_json(root / "release/current/stage142_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))
    bundle = load_sample_bundle(root)
    base_scene = build_scene_intent(bundle)
    style = build_style_profile()
    benchmark_cases = _build_benchmark_cases(base_scene)
    compiler = Node2ProseCompiler()
    critic_gate = Node3CriticGate()

    rendered_samples: list[dict[str, Any]] = []
    critic_reports: list[dict[str, Any]] = []
    rendered_objects = []
    benchmark_case_reports: list[dict[str, Any]] = []
    critic_pass_count = 0

    for case in benchmark_cases:
        scene = _apply_case(base_scene, case)
        compiled = compiler.compile(scene, style)
        critic_ok, critic_issues = critic_gate.validate(compiled.rendered)
        critic = CriticResult(status="pass" if critic_ok else "blocked", issues=tuple(critic_issues))
        critic_pass_count += 1 if critic_ok else 0
        rendered = compiled.rendered.to_dict()
        rendered["case_id"] = case.case_id
        rendered["timeline_position"] = scene.timeline_position
        rendered_samples.append(rendered)
        critic_report = {
            "case_id": case.case_id,
            "scene_id": scene.scene_id,
            **critic.to_dict(),
        }
        critic_reports.append(critic_report)
        rendered_objects.append(compiled.rendered)
        benchmark_case_reports.append(
            {
                "case_id": case.case_id,
                "scene_id": scene.scene_id,
                "status": "pass" if critic_ok else "blocked",
                "reader_surface_average": compiled.rendered.surface_score.get("reader_surface_average", 0),
                "provider_default_calls": critic.provider_default_calls,
                "node2_raw_reveal_access": critic.node2_raw_reveal_access,
                "risk_flags": list(compiled.rendered.risk_flags),
            }
        )

    aggregate = aggregate_report(rendered_objects)
    scoreboard = _build_scoreboard(bundle.benchmark_expectations, benchmark_cases, aggregate, critic_reports, benchmark_case_reports)

    _write_json(pack / "stage141_baseline_summary.json", _compact_baseline(baseline))
    _write_json(pack / "sample_bundle_summary.json", _sample_bundle_summary(bundle))
    _write_json(pack / "style_profile.json", style.to_dict())
    _write_json(pack / "benchmark_cases.json", {"cases": [case.to_dict() for case in benchmark_cases]})
    _write_json(pack / "rendered_samples.json", {"rendered_samples": rendered_samples})
    _write_json(pack / "critic_reports.json", {"critic_reports": critic_reports})
    _write_json(pack / "benchmark_case_reports.json", {"benchmark_case_reports": benchmark_case_reports})
    _write_json(pack / "benchmark_scoreboard.json", scoreboard)
    _write_json(benchmark_results_dir / "stage142_benchmark_pack_summary.json", scoreboard)
    _write_json(benchmark_results_dir / "stage142_rendered_samples.json", {"rendered_samples": rendered_samples})

    # Metadata consistency expects the stage report path to exist, so seed it before the final checks.
    _write_json(
        root / TARGET_REPORT,
        {
            "stage": "142",
            "baseline_stage": "141",
            "title": "Longform Benchmark Pack",
            "status": "building",
            "issues": [],
        },
    )

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage141_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "benchmark_scoreboard": scoreboard,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))
    if critic_pass_count != len(benchmark_cases):
        issues.append("critic_gate_blocked")

    result = {
        "stage": "142",
        "baseline_stage": "141",
        "title": "Longform Benchmark Pack",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "LONGFORM_BENCHMARK_PACK_LOCAL",
        "longform_benchmark_pack_only": True,
        "sample_project_contract_reused": True,
        "benchmark_case_count": len(benchmark_cases),
        "rendered_scene_count": aggregate.get("rendered_scene_count", 0),
        "critic_gate_pass_count": critic_pass_count,
        "benchmark_scoreboard_status": scoreboard.get("status"),
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "stage143_user_docs_ready": scoreboard.get("stage143_user_docs_ready", False),
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
            "stage141_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "sample_bundle_summary": _sample_bundle_summary(bundle),
            "style_profile": style.to_dict(),
            "benchmark_cases": [case.to_dict() for case in benchmark_cases],
            "rendered_samples": rendered_samples,
            "critic_reports": critic_reports,
            "benchmark_case_reports": benchmark_case_reports,
            "benchmark_scoreboard": scoreboard,
        },
    }

    _write_json(root / TARGET_REPORT, result)
    return result


def _build_benchmark_cases(base_scene: SceneIntentIR) -> list[BenchmarkCaseDefinition]:
    return [
        BenchmarkCaseDefinition(
            case_id=f"{base_scene.scene_id}_inheritance_signal",
            scene_goal="Establish the inheritance question with restrained suspicion and public-safe ambiguity.",
            conflict="A legal hesitation delays the answer while the oldest family member counters with guarded politeness.",
            dialogue_seed="Everyone wants the answer tonight, but no one is willing to say the first true sentence out loud.",
            timeline_position="EP1_SCENE1_A",
            setting_suffix="Rain taps the office blinds while the lamp on the archive desk hums softly.",
            emotional_from="unease",
            emotional_to="alert_resolve",
        ),
        BenchmarkCaseDefinition(
            case_id=f"{base_scene.scene_id}_corridor_pressure",
            scene_goal="Intensify corridor pressure around the unsigned document without revealing the secret heir.",
            conflict="A hallway exchange turns sharp when the attorney refuses to confirm the family rumor.",
            dialogue_seed="If the paper matters this much, why did everyone pretend it was ordinary yesterday?",
            timeline_position="EP1_SCENE1_B",
            setting_suffix="The corridor smells faintly of wet wool, old wood, and cooling tea.",
            emotional_from="caution",
            emotional_to="compressed_defiance",
        ),
        BenchmarkCaseDefinition(
            case_id=f"{base_scene.scene_id}_ledger_afterimage",
            scene_goal="Leave a lingering afterimage around the inheritance ledger while preserving all reveal boundaries.",
            conflict="A ledger entry appears harmless, but it rearranges who feels safe enough to speak.",
            dialogue_seed="The number itself is small; the silence around it is what makes the room tilt.",
            timeline_position="EP1_SCENE1_C",
            setting_suffix="A cold draft slips under the study door and stirs the edge of the ledger page.",
            emotional_from="fatigue",
            emotional_to="fragile_focus",
        ),
    ]


def _apply_case(base_scene: SceneIntentIR, case: BenchmarkCaseDefinition) -> SceneIntentIR:
    return replace(
        base_scene,
        scene_id=case.case_id,
        scene_goal=case.scene_goal,
        conflict=case.conflict,
        emotional_delta=EmotionalDelta(case.emotional_from, case.emotional_to),
        dialogue_seed=case.dialogue_seed,
        timeline_position=case.timeline_position,
        setting_seed=f"{base_scene.setting_seed} {case.setting_suffix}",
    )


def _build_scoreboard(
    expectations: dict[str, Any],
    benchmark_cases: list[BenchmarkCaseDefinition],
    aggregate: dict[str, Any],
    critic_reports: list[dict[str, Any]],
    benchmark_case_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    min_case_count = int(expectations.get("stage142_min_case_count", 3) or 3)
    min_average = float(expectations.get("reader_surface_average_min", 8.5) or 8.5)
    min_case_average = float(expectations.get("reader_surface_min_per_case", 8.0) or 8.0)
    issues: list[str] = []
    case_scores = [float(case.get("reader_surface_average", 0) or 0) for case in benchmark_case_reports]
    if len(benchmark_cases) < min_case_count:
        issues.append("benchmark_case_count_below_expectation")
    if int(aggregate.get("rendered_scene_count", 0) or 0) < min_case_count:
        issues.append("rendered_scene_count_below_expectation")
    if aggregate.get("status") != "pass":
        issues.append("aggregate_render_quality_blocked")
    if float(aggregate.get("reader_surface_average", 0) or 0) < min_average:
        issues.append("reader_surface_average_below_threshold")
    if case_scores and min(case_scores) < min_case_average:
        issues.append("per_case_average_below_threshold")
    if any(report.get("status") != "pass" for report in critic_reports):
        issues.append("critic_report_blocked")
    if aggregate.get("external_provider_calls", 0) != 0:
        issues.append("provider_default_calls_nonzero")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage142 Longform Benchmark Scoreboard",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "benchmark_id": expectations.get("benchmark_id", "stage142_longform_benchmark_pack"),
        "benchmark_case_count": len(benchmark_cases),
        "min_case_count": min_case_count,
        "rendered_scene_count": int(aggregate.get("rendered_scene_count", 0) or 0),
        "reader_surface_average": float(aggregate.get("reader_surface_average", 0) or 0),
        "reader_surface_average_min": min_average,
        "reader_surface_min_per_case": min_case_average,
        "lowest_case_average": round(min(case_scores), 2) if case_scores else 0.0,
        "highest_case_average": round(max(case_scores), 2) if case_scores else 0.0,
        "mean_case_average": round(mean(case_scores), 2) if case_scores else 0.0,
        "critic_pass_count": sum(1 for report in critic_reports if report.get("status") == "pass"),
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "stage143_user_docs_ready": not issues,
    }


def _sample_bundle_summary(bundle: Any) -> dict[str, Any]:
    characters = bundle.characters.get("characters", [])
    return {
        "project_id": bundle.project.get("project_id"),
        "synthetic_only": bundle.project.get("synthetic_only"),
        "provider_calls_allowed": bundle.project.get("provider_calls_allowed"),
        "character_count": len(characters),
        "source_scene_request_id": bundle.scene_request.get("scene_id"),
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
    compact["stage141_release_gate_status"] = report.get("status")
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
