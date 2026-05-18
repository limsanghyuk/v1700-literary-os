from __future__ import annotations

from v1700.provider_evaluation.contracts import ProviderEvaluationPrompt


def build_stage94_prompt_suite() -> tuple[ProviderEvaluationPrompt, ...]:
    return (
        ProviderEvaluationPrompt(
            prompt_id="stage94_drama_scene_surface",
            task="reader_facing_scene_render",
            system="You are evaluating provider behavior for V1700. Preserve reveal boundaries.",
            prompt=(
                "Render a restrained Korean drama scene beat: a doctor returns to an empty call room, "
                "finds a cold cup of coffee, and realizes a promise was kept without anyone saying it aloud."
            ),
            branchpoint_requirements=(
                "provider_zero_release_gate",
                "node2_surface_only",
                "no_raw_reveal_access",
                "reader_facing_prose",
            ),
        ),
        ProviderEvaluationPrompt(
            prompt_id="stage94_reveal_guard_probe",
            task="reveal_boundary_probe",
            system="You are evaluating reveal discipline. Do not expose hidden facts.",
            prompt=(
                "Write a short response that implies a family secret exists without naming the secret, "
                "and keep the character unaware of what the reader suspects."
            ),
            branchpoint_requirements=(
                "episode_reveal_budget",
                "character_knowledge_bridge",
                "no_direct_secret_reveal",
            ),
        ),
        ProviderEvaluationPrompt(
            prompt_id="stage94_studio_handoff_probe",
            task="writer_studio_handoff",
            system="You are evaluating Writer Studio handoff text.",
            prompt=(
                "Summarize why this scene should be revised: the emotional beat is clear, "
                "but the dialogue explains too much and needs more subtext."
            ),
            branchpoint_requirements=(
                "writer_studio_review_queue",
                "anti_llm_surface",
                "branchpoint_compliance",
            ),
        ),
    )
