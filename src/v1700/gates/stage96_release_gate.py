from __future__ import annotations

from pathlib import Path

from v1700.gates.stage95_release_gate import run_stage95_release_gate
from v1700.stage96.orchestrator import run_stage96_pipeline

_STAGE96_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage96_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE96_CACHE:
        return _STAGE96_CACHE[cache_key]

    stage95_gate = run_stage95_release_gate(root)
    pipeline = run_stage96_pipeline(root)
    checks = {
        "stage95_baseline_gate": stage95_gate,
        "stage96_pipeline": pipeline,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    phase_checks = pipeline.get("checks", {})
    optimization = phase_checks.get("narrative_optimization", {})
    learning = phase_checks.get("manuscript_learning", {})
    ensemble = phase_checks.get("provider_ensemble", {})
    if optimization.get("drift_guard", {}).get("status") != "pass":
        issues.append("coefficient_drift_guard_blocked")
    if learning.get("privacy_report", {}).get("status") != "pass":
        issues.append("privacy_guard_blocked")
    if ensemble.get("live_provider_call_count") != 0:
        issues.append("live_provider_call_count_not_zero")
    if ensemble.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if ensemble.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")

    result = {
        "stage": "96",
        "baseline_stage": "95",
        "status": "pass" if not issues else "blocked",
        "checks": checks,
        "issues": issues,
        "provider_call_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "coefficient_drift_summary": optimization.get("drift_guard", {}),
        "manuscript_learning_summary": {
            "scene_feature_count": learning.get("scene_feature_count", 0),
            "source_policy": learning.get("privacy_report", {}).get("source_policy", ""),
        },
        "provider_ensemble_summary": {
            "candidate_count": ensemble.get("candidate_count", 0),
            "decisions": [item.get("decision") for item in ensemble.get("decisions", [])],
        },
        "branchpoint_survival_summary": phase_checks.get("stage95_baseline", {}).get("branchpoint_survival", {}),
    }
    _STAGE96_CACHE[cache_key] = result
    return result
