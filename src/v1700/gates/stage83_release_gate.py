from __future__ import annotations
from pathlib import Path

from v1700.commercial_release import run_commercial_release_candidate
from v1700.gates.stage82_release_gate import run_stage82_release_gate


def run_stage83_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage82 = run_stage82_release_gate(root)
    commercial = run_commercial_release_candidate(root)
    manifest = commercial.get("commercial_release_manifest", {})
    issues: list[str] = []
    if stage82.get("status") != "pass":
        issues.append("stage82_release_gate_blocked")
    if commercial.get("status") != "pass":
        issues.append("commercial_release_candidate_blocked")
    if manifest.get("episode_count", 0) < 3:
        issues.append("episode_count_below_3")
    if manifest.get("actual_rendered_scene_count", 0) < 30:
        issues.append("actual_rendered_scene_count_below_30")
    if manifest.get("quality_average_after", 0.0) < 8.0:
        issues.append("quality_average_after_below_8")
    if manifest.get("quality_average_delta", 0.0) < 0.5:
        issues.append("quality_delta_below_0_5")
    if manifest.get("quality_blocker_count_after", 1) != 0:
        issues.append("quality_blockers_remain")
    if manifest.get("reveal_leakage_count", 1) != 0:
        issues.append("reveal_leakage_detected")
    if manifest.get("timeline_contradiction_count", 1) != 0:
        issues.append("timeline_contradiction_detected")
    if manifest.get("blind_v1700_margin_over_pure_gpt", 0.0) < 1.0:
        issues.append("blind_margin_below_1_0")
    return {
        "stage": "83",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage83 packages a local-first commercial longform release candidate evidence pack: 3 episode files, 30 actual rendered scenes, quality/refinement reports, and blind critic benchmark evidence.",
        "stage82_release_gate": stage82,
        "commercial_release_candidate": commercial,
        "episode_count": manifest.get("episode_count"),
        "actual_rendered_scene_count": manifest.get("actual_rendered_scene_count"),
        "quality_average_after": manifest.get("quality_average_after"),
        "quality_average_delta": manifest.get("quality_average_delta"),
        "blind_v1700_margin_over_pure_gpt": manifest.get("blind_v1700_margin_over_pure_gpt"),
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
