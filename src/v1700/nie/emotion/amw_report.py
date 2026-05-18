from __future__ import annotations

from v1700.nie.emotion.adaptive_momentum_weights import AdaptiveMomentumWeights, build_amw_inputs
from v1700.nie.emotion.contracts import AMWReport, GenreName
from v1700.nie.emotion.genre_alpha_table import initial_alpha_state
from v1700.nie.reward.mae_result_fixture import build_stage113_fixture_mae_result


def build_stage114_amw_report(genre: GenreName = "melodrama", act_pos: float = 0.56) -> dict:
    mae = build_stage113_fixture_mae_result(scene_id="stage114_fixture_scene_001")
    inputs = build_amw_inputs(mae.dimension_scores.to_dict(), genre=genre, act_pos=act_pos)
    before = initial_alpha_state(genre, act_pos)
    amw = AdaptiveMomentumWeights(genre=genre, alpha=before.copy())
    updates = amw.update_many(inputs)
    guard = amw.drift_guard(updates)
    issues: list[str] = []
    if guard.status != "pass":
        issues.extend(guard.issues)
    report = AMWReport(
        stage="114",
        status="pass" if not issues else "blocked",
        genre=genre,
        scene_id=mae.scene_id,
        alpha_before=before,
        alpha_after=amw.to_dict(),
        updates=updates,
        drift_guard=guard,
        provider_call_count=mae.live_provider_call_count,
        physics_reward_bridge_llm_call_count=0,
        issues=tuple(issues),
    )
    return report.to_dict()
