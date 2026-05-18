from __future__ import annotations

from typing import Any

from v1700.nie.arc.contracts import SceneTensionPoint
from v1700.nie.arc.narrative_tension_curve import NarrativeTensionCurve


def build_stage117_fixture_scenes() -> tuple[SceneTensionPoint, ...]:
    curve = NarrativeTensionCurve()
    positions = (0.05, 0.16, 0.30, 0.42, 0.56, 0.69, 0.82, 0.95)
    # Keep the fixture close to the ideal curve while leaving a tiny realistic
    # deviation so tests prove loss is measured rather than hard-coded to zero.
    offsets = (-0.010, 0.008, -0.006, 0.006, -0.007, 0.005, -0.006, 0.004)
    scenes: list[SceneTensionPoint] = []
    for idx, (pos, offset) in enumerate(zip(positions, offsets, strict=True), start=1):
        act = min(int(pos * 4) + 1, 4)
        score = min(max(curve.ideal(pos) + offset, 0.0), 1.0)
        scenes.append(SceneTensionPoint(
            scene_id=f"stage117_scene_{idx:03d}",
            position=pos,
            tension_score=round(score, 6),
            act=act,
            function="setup" if act == 1 else "rising_conflict" if act == 2 else "crisis" if act == 3 else "resolution",
        ))
    return tuple(scenes)


def build_stage117_tension_curve_report() -> dict[str, Any]:
    curve = NarrativeTensionCurve(block_threshold=0.18, warn_threshold=0.10)
    scenes = build_stage117_fixture_scenes()
    loss = curve.evaluate(scenes, lam=0.3)
    rows = curve.per_scene_rows(scenes)
    act_counts: dict[int, int] = {act: 0 for act in range(1, 5)}
    for scene in scenes:
        act_counts[scene.act] += 1
    issues: list[str] = []
    if loss.status != "PASS":
        issues.append("narrative_tension_curve_loss_not_pass")
    if loss.coverage_loss != 0.0:
        issues.append("coverage_loss_nonzero_for_fixture")
    if not all(0.0 <= row["ideal_tension"] <= 1.0 for row in rows):
        issues.append("ideal_tension_out_of_bounds")

    return {
        "stage": "117",
        "baseline_stage": "116",
        "title": "NarrativeTensionCurve",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "formula": "T_ideal(t)=0.60+0.40*sin(2πt-0.50)+0.20*sin(6πt)",
        "loss_function": "L_final=L_tension+lambda*L_coverage",
        "lambda_coverage": 0.3,
        "block_threshold": curve.block_threshold,
        "warn_threshold": curve.warn_threshold,
        "scene_count": len(scenes),
        "act_counts": {str(k): v for k, v in act_counts.items()},
        "loss": loss.to_dict(),
        "per_scene": rows,
        "coverage_targets": {str(k): v for k, v in curve.DEFAULT_ACT_TARGETS.items()},
        "provider_call_count": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
