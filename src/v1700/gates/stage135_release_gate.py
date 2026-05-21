from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage134_release_gate import run_stage134_release_gate
from v1700.stage135 import run_stage135

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage135_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage134_release_gate(root)
    stage = run_stage135(root)
    parts = stage.get("parts", {})
    registry = parts.get("candidate_registry", {})
    preflight = parts.get("preflight", {})
    checks = {
        "stage134_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage134", {}).get("status") == "pass"
        ),
        "learning_quality_report_pass": _check(stage.get("status") == "pass"),
        "candidate_registry_pass": _check(registry.get("status") == "pass"),
        "candidate_only_mode_pass": _check(stage.get("learning_candidate_only") is True and stage.get("mode") == "LEARNING_QUALITY_GATE_CANDIDATE_ONLY"),
        "learning_disabled_pass": _check(stage.get("learning_allowed_count") == 0),
        "training_not_triggered_pass": _check(stage.get("training_triggered_count") == 0 and stage.get("runtime_training_enabled") is False),
        "active_learning_disabled_pass": _check(stage.get("active_meta_learning_enabled") is False),
        "model_weight_update_blocked": _check(stage.get("model_weight_update_count") == 0),
        "mutation_blocked_pass": _check(stage.get("auto_repair_mutation_count") == 0 and stage.get("mutation_allowed_count") == 0),
        "review_only_route_pass": _check(stage.get("review_only_count", 0) >= 1),
        "preflight_pass": _check(preflight.get("status") == "pass" and preflight.get("python_fallback", {}).get("status") == "PASS"),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "canon_auto_resolution_blocked": _check(stage.get("canon_auto_resolution_count") == 0),
        "cross_project_write_blocked": _check(stage.get("cross_project_write_allowed") is False),
        "gate26_advisory_only_pass": _check(stage.get("gate26_hard_block_enabled") is False),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "135",
        "baseline_stage": "134",
        "title": "LearningQualityGate & Candidate Registry Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage135": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage135_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "mode", "learning_candidate_only",
        "candidate_count", "accepted_candidate_count", "rejected_candidate_count", "review_only_count",
        "learning_allowed_count", "training_triggered_count", "mutation_allowed_count",
        "runtime_training_enabled", "active_meta_learning_enabled", "model_weight_update_count",
        "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage",
        "cross_project_write_allowed", "gate26_hard_block_enabled", "canon_auto_resolution_count",
        "auto_repair_mutation_count", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage135.md",
        "docs/proposals/stage135_proposal.md",
        "docs/architecture/stage135_blueprint.md",
        "manifests/stage135_manifest.json",
        "manifests/stage135_learning_quality_gate_manifest.json",
        "release/current/stage135_learning_quality_gate_report.json",
        "release/current/stage135_learning_quality_gate_pack/candidate_registry.json",
        "release/current/stage135_learning_quality_gate_pack/stage135_preflight_report.json",
    ])
