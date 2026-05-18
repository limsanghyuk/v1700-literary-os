from __future__ import annotations

from .contracts import TrialCandidate, WriterTrialSeed


def build_stage102_trial_candidates(seed: WriterTrialSeed) -> tuple[TrialCandidate, ...]:
    prompt = seed.prompt
    return (
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_A",
            hidden_label="A",
            mode="PURE_GPT_DIRECT",
            visible_excerpt=(
                f"Prompt: {prompt}. The story moves quickly through conflict, secret, and resolution, "
                "but the macro plot, scene contract, payoff debt, and revision evidence remain mostly implicit."
            ),
            evidence_markers=("direct_draft", "low_structure_evidence"),
        ),
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_B",
            hidden_label="B",
            mode="CLAUDE_REFERENCE",
            visible_excerpt=(
                f"Prompt: {prompt}. The draft has reflective emotional texture and clear motivations, "
                "yet the writer must still infer scenario beats, reveal timing, and branchpoint survival manually."
            ),
            evidence_markers=("long_context_texture", "manual_gate_inference"),
        ),
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_C",
            hidden_label="C",
            mode="GEMINI_REFERENCE",
            visible_excerpt=(
                f"Prompt: {prompt}. The draft gives cinematic scene images and broad action direction, "
                "but the evidence trail for character knowledge, payoff slots, and writer revision tasks is partial."
            ),
            evidence_markers=("visual_scene_energy", "partial_contract_trace"),
        ),
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_D",
            hidden_label="D",
            mode="OLLAMA_LOCAL_DRAFT",
            visible_excerpt=(
                f"Prompt: {prompt}. The draft keeps the manuscript local and inexpensive, "
                "but its prose surface, dialogue hierarchy, and episode-level escalation need heavier revision."
            ),
            evidence_markers=("local_privacy", "revision_heavy"),
        ),
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_E",
            hidden_label="E",
            mode="V1700_PROSE",
            visible_excerpt=(
                f"Prompt: {prompt}. The prose mode keeps Node2 surface-only, removes flat AI phrasing, "
                "and turns emotion into behavior while preserving hidden reveal facts outside the visible draft."
            ),
            evidence_markers=("node2_surface_only", "anti_llm_surface", "emotion_to_behavior"),
        ),
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_F",
            hidden_label="F",
            mode="V1700_SCENARIO",
            visible_excerpt=(
                f"Prompt: {prompt}. The scenario mode exposes scene beats, investigation movement, "
                "dialogue silence, prop-led reveal cues, and production-ready episode handoff evidence."
            ),
            evidence_markers=("scene_beat_board", "dialogue_silence", "prop_reveal_budget"),
        ),
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_G",
            hidden_label="G",
            mode="V430_SCENARIO_ROOM",
            visible_excerpt=(
                f"Prompt: {prompt}. The scenario-room candidate improves actionability and shot logic, "
                "but remains accepted only as a V1700 contract fixture until its source lineage is traced."
            ),
            evidence_markers=("scenario_room_fixture", "cross_lineage_guard"),
        ),
        TrialCandidate(
            candidate_id=f"{seed.seed_id}_H",
            hidden_label="H",
            mode="V1700_HYBRID",
            visible_excerpt=(
                f"Prompt: {prompt}. The hybrid candidate combines prose surface, scenario beats, payoff debt, "
                "writer revision queue, branchpoint trace, and provider-zero privacy into one auditable workflow."
            ),
            evidence_markers=("hybrid_workflow", "payoff_debt_audit", "writer_revision_queue", "provider_zero"),
        ),
    )
