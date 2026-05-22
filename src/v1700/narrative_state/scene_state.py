from __future__ import annotations

from .contracts import NarrativeFieldSpec, NarrativeStateContract, RevealBoundarySpec


def build_scene_state_contract() -> NarrativeStateContract:
    return NarrativeStateContract(
        name="SceneState",
        scope="scene",
        purpose="Defines the smallest canonical narrative unit that generation and criticism will consume later.",
        write_policy="read_only_contract_until_generation_layer_is_gated",
        fields=(
            NarrativeFieldSpec("scene_id", "string", True, "Stable scene identifier.", "scene packet"),
            NarrativeFieldSpec("episode_id", "string", True, "Parent episode identifier.", "episode state"),
            NarrativeFieldSpec("location_id", "string", True, "Canonical location reference.", "world state"),
            NarrativeFieldSpec("participants", "list[string]", True, "Character identifiers present in the scene.", "character roster"),
            NarrativeFieldSpec("objective", "string", True, "Immediate dramatic objective of the scene.", "scene packet"),
            NarrativeFieldSpec("surface_constraints", "list[string]", True, "Reader-surface rules for prose rendering.", "node2 boundary policy"),
        ),
    )


def build_reveal_state_contract() -> NarrativeStateContract:
    return NarrativeStateContract(
        name="RevealState",
        scope="reveal",
        purpose="Controls reveal visibility and knowledge budgets without exposing raw hidden state to Node2.",
        write_policy="read_only_contract_until_human_approval_layer",
        fields=(
            NarrativeFieldSpec("reveal_id", "string", True, "Stable reveal identifier.", "reveal packet"),
            NarrativeFieldSpec("owner_scope", "string", True, "Series, episode, or scene ownership.", "reveal packet"),
            NarrativeFieldSpec("visibility_level", "string", True, "Allowed visibility such as hidden, critic_only, or reader_surface.", "reveal packet"),
            NarrativeFieldSpec("knowledge_holders", "list[string]", True, "Characters or system lanes allowed to know the reveal.", "reveal packet"),
            NarrativeFieldSpec("unlock_condition", "string", True, "Approved condition for future reveal progression.", "reveal packet"),
            NarrativeFieldSpec("node2_surface_projection", "string", True, "Surface-safe projection available to Node2.", "node boundary policy"),
        ),
    )


def build_reveal_boundaries() -> tuple[RevealBoundarySpec, ...]:
    return (
        RevealBoundarySpec("SeriesState", "full_contract", "surface_summary_only", "critic_summary_only", "Series metadata can be summarized but not fully exposed to Node2."),
        RevealBoundarySpec("EpisodeState", "full_contract", "surface_summary_only", "critic_summary_only", "Episode planning remains authoritative outside reader-facing prose."),
        RevealBoundarySpec("SceneState", "full_contract", "surface_safe_scene_packet", "critic_surface_plus_flags", "Scene state is rendered through Node2-safe packets only."),
        RevealBoundarySpec("CharacterState", "full_contract", "surface_traits_only", "critic_relationship_summary", "Private goals and hidden beliefs stay out of Node2."),
        RevealBoundarySpec("WorldState", "full_contract", "surface_world_facts_only", "critic_world_consistency_summary", "World internals are summarized for reader output."),
        RevealBoundarySpec("RevealState", "full_contract", "node2_raw_reveal_access_zero", "critic_reveal_guard_summary", "Reveal state is never handed raw to Node2."),
        RevealBoundarySpec("ContinuityState", "full_contract", "surface_continuity_summary", "critic_continuity_packet", "Continuity risks remain review artifacts, not Node2 input."),
    )
