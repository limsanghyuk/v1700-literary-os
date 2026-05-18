from __future__ import annotations

from v1700.nie.reward.contracts import MAEDimensionScores, MAEResult


def build_stage113_fixture_mae_result(scene_id: str = "stage113_fixture_scene_001") -> MAEResult:
    """Build a deterministic, release-safe four-agent MAE fixture.

    The numbers intentionally make the reward positive against a 0.50 baseline
    so the bridge can demonstrate advantage and bounded coefficient proposals
    without any live model call.
    """

    return MAEResult(
        scene_id=scene_id,
        reader_score=0.82,
        writer_score=0.76,
        editor_score=0.79,
        cultural_score=0.74,
        dimension_scores=MAEDimensionScores(
            tension=0.78,
            sympathy=0.72,
            dread=0.61,
            catharsis=0.69,
        ),
        rubric_evidence={
            "reader": ("curiosity_present", "empathy_anchor_present", "next_scene_pull"),
            "writer": ("dialogue_voice_distinct", "image_specificity", "subtext_present"),
            "editor": ("causal_link_clear", "reveal_timing_safe", "pace_consistent"),
            "cultural": ("k_drama_emotional_code", "relationship_pressure_legible", "cliche_avoidance"),
        },
        live_provider_call_count=0,
        source="fixture",
    )


def build_stage113_feature_vector(mae_result: MAEResult | None = None) -> dict[str, float]:
    mae_result = mae_result or build_stage113_fixture_mae_result()
    dims = mae_result.dimension_scores.to_dict()
    return {
        "emotional_momentum_weight": dims["tension"],
        "curiosity_gradient_weight": mae_result.reader_score,
        "scene_energy_weight": mae_result.editor_score,
        "motif_residue_weight": mae_result.cultural_score,
    }
