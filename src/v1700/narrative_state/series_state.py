from __future__ import annotations

from .contracts import NarrativeFieldSpec, NarrativeStateContract


def build_series_state_contract() -> NarrativeStateContract:
    return NarrativeStateContract(
        name="SeriesState",
        scope="series",
        purpose="Defines project-level continuity and identity anchors for the entire series.",
        write_policy="read_only_contract_until_stage150_memory_body",
        fields=(
            NarrativeFieldSpec("series_id", "string", True, "Stable identifier for the series.", "project manifest"),
            NarrativeFieldSpec("title", "string", True, "Human-readable series title.", "project manifest"),
            NarrativeFieldSpec("format", "string", True, "Story format such as drama or novel.", "project manifest"),
            NarrativeFieldSpec("theme_brief", "string", True, "Concise thematic spine for the work.", "project manifest"),
            NarrativeFieldSpec("episode_order", "list[string]", True, "Canonical ordered episode identifiers.", "episode manifests"),
            NarrativeFieldSpec("timeline_anchor", "string", True, "Default chronology anchor for continuity checks.", "series continuity packet"),
        ),
    )


def build_character_state_contract() -> NarrativeStateContract:
    return NarrativeStateContract(
        name="CharacterState",
        scope="character",
        purpose="Captures the canonical public state of a character without enabling hidden-memory mutation.",
        write_policy="read_only_contract_until_human_approval_layer",
        fields=(
            NarrativeFieldSpec("character_id", "string", True, "Stable character identifier.", "character roster"),
            NarrativeFieldSpec("display_name", "string", True, "Reader-facing character name.", "character roster"),
            NarrativeFieldSpec("role", "string", True, "Narrative role within the work.", "character roster"),
            NarrativeFieldSpec("goal_vector", "list[string]", True, "Current explicit goals and motivations.", "series/episode planning packet"),
            NarrativeFieldSpec("relationship_edges", "list[object]", True, "Declared relationships to other characters.", "relationship ledger"),
            NarrativeFieldSpec("knowledge_boundary", "string", True, "What the character can know within approved reveals.", "reveal contract"),
        ),
    )


def build_world_state_contract() -> NarrativeStateContract:
    return NarrativeStateContract(
        name="WorldState",
        scope="world",
        purpose="Defines the stable setting, institutions, and rule anchors that prose must preserve.",
        write_policy="read_only_contract_until_project_manifest_body",
        fields=(
            NarrativeFieldSpec("world_id", "string", True, "Stable world identifier.", "world packet"),
            NarrativeFieldSpec("era", "string", True, "Temporal setting or historical layer.", "world packet"),
            NarrativeFieldSpec("locations", "list[object]", True, "Canonical locations available to scenes.", "world packet"),
            NarrativeFieldSpec("institutions", "list[object]", True, "Organizations and families with continuity value.", "world packet"),
            NarrativeFieldSpec("rule_constraints", "list[string]", True, "Setting rules that scenes must not violate.", "world packet"),
            NarrativeFieldSpec("public_facts", "list[string]", True, "Surface-safe facts available to reader-facing output.", "world packet"),
        ),
    )
