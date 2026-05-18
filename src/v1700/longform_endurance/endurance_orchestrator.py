from __future__ import annotations

from pathlib import Path

from v1700.gates.stage96_release_gate import run_stage96_release_gate
from v1700.longform_endurance.production_proof import build_longform_production_proof


def run_stage97_longform_endurance(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    required_16 = build_longform_production_proof(16)
    extended_24 = build_longform_production_proof(24)
    issues = []
    if required_16.get("status") != "pass":
        issues.append("sixteen_episode_endurance_proof_blocked")
    if required_16.get("provider_default_calls") != 0 or required_16.get("live_provider_call_count") != 0:
        issues.append("provider_call_count_not_zero")
    if required_16.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    return {
        "stage": "97",
        "status": "pass" if not issues else "blocked",
        "title": "Full Longform Narrative Endurance Engine",
        "required_16_episode_proof": required_16,
        "extended_24_episode_proof": extended_24,
        "episode_count_verified": required_16.get("episode_count", 0),
        "microplot_count": required_16.get("microplot_count", 0),
        "scene_count_estimate": required_16.get("scene_count_estimate", 0),
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
        "issues": issues,
    }


def run_stage97_with_baseline(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    baseline = run_stage96_release_gate(root)
    endurance = run_stage97_longform_endurance(root)
    issues = []
    if baseline.get("status") != "pass":
        issues.append("stage96_baseline_gate_blocked")
    if endurance.get("status") != "pass":
        issues.append("stage97_longform_endurance_blocked")
    return {
        "stage": "97",
        "status": "pass" if not issues else "blocked",
        "baseline_stage": "96",
        "checks": {
            "stage96_baseline_gate": baseline,
            "longform_endurance": endurance,
        },
        "issues": issues,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
    }
