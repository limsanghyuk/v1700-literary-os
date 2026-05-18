from __future__ import annotations

from v1700.stage100.contracts import DualModeEvaluationResult


def evaluate_scenario_candidate() -> DualModeEvaluationResult:
    scores = {
        "scene_beat_clarity": 8.5,
        "investigative_action": 8.2,
        "dialogue_silence_pressure": 8.4,
        "visualizability": 8.6,
        "production_feasibility": 8.3,
    }
    return DualModeEvaluationResult(
        seed_id="STAGE100_SEED_SCENARIO_001",
        mode="SCENARIO",
        candidate_id="v1700_stage100_scenario_fixture",
        engine_profile="V1700 Literary OS local-first scenario authority",
        score_total=round(sum(scores.values()) / len(scores), 2),
        score_breakdown=scores,
        reviewer_notes=[
            "Scenario mode values scene action, beat legibility, silence, camera-readiness, and production feasibility.",
            "Prose interiority metrics are intentionally excluded from scenario scoring.",
        ],
    )

