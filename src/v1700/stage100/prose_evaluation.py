from __future__ import annotations

from v1700.stage100.contracts import DualModeEvaluationResult


def evaluate_prose_candidate() -> DualModeEvaluationResult:
    scores = {
        "sentence_density": 8.8,
        "sensory_texture": 8.6,
        "interiority": 8.7,
        "voice_drift_control": 8.9,
        "longform_literary_structure": 9.1,
    }
    return DualModeEvaluationResult(
        seed_id="STAGE100_SEED_KDRAMA_001",
        mode="PROSE",
        candidate_id="v1700_stage100_prose_fixture",
        engine_profile="V1700 Literary OS local-first prose authority",
        score_total=round(sum(scores.values()) / len(scores), 2),
        score_breakdown=scores,
        reviewer_notes=[
            "Prose mode values density, sensory residue, interiority, and longform voice stability.",
            "Scenario-only beat metrics are intentionally excluded from prose scoring.",
        ],
    )

