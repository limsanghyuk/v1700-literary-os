from __future__ import annotations

from pathlib import Path

from v1700.gates.stage96_release_gate import run_stage96_release_gate
from v1700.longform_endurance.endurance_orchestrator import run_stage97_longform_endurance

_STAGE97_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage97_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE97_CACHE:
        return _STAGE97_CACHE[cache_key]
    stage96 = run_stage96_release_gate(root)
    endurance = run_stage97_longform_endurance(root)
    proof = endurance.get("required_16_episode_proof", {})
    checks = proof.get("checks", {})
    issues = []
    if stage96.get("status") != "pass":
        issues.append("stage96_baseline_gate_blocked")
    if endurance.get("status") != "pass":
        issues.append("longform_production_proof_blocked")
    for name, report in checks.items():
        if report.get("status") != "pass":
            issues.append(f"{name}_blocked")
    if proof.get("provider_default_calls") != 0 or proof.get("live_provider_call_count") != 0:
        issues.append("provider_zero_blocked")
    if proof.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_surface_guard_blocked")
    payoff = checks.get("payoff_debt_ledger", {})
    scene = checks.get("scene_necessity", {})
    agency = checks.get("agency_conservation", {})
    voice = checks.get("voice_manifold", {})
    attention = checks.get("attention_economy", {})
    result = {
        "stage": "97",
        "baseline_stage": "96",
        "status": "pass" if not issues else "blocked",
        "checks": {
            "stage96_baseline_gate": stage96,
            "longform_endurance": endurance,
        },
        "issues": issues,
        "episode_count_verified": endurance.get("episode_count_verified", 0),
        "microplot_count": endurance.get("microplot_count", 0),
        "scene_count_estimate": endurance.get("scene_count_estimate", 0),
        "critical_debt_default_count": payoff.get("critical_debt_default_count", 0),
        "weak_scene_ratio": scene.get("weak_scene_ratio", 1.0),
        "agency_floor_status": agency.get("agency_floor_status", "blocked"),
        "style_drift_summary": voice.get("style_drift_summary", ""),
        "attention_fatigue_risk": attention.get("attention_fatigue_risk", 1.0),
        "provider_call_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_survival_summary": stage96.get("branchpoint_survival_summary", {}),
    }
    _STAGE97_CACHE[cache_key] = result
    return result
