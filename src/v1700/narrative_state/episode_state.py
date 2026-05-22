from __future__ import annotations

from .contracts import ContinuityRule, NarrativeFieldSpec, NarrativeStateContract


def build_episode_state_contract() -> NarrativeStateContract:
    return NarrativeStateContract(
        name="EpisodeState",
        scope="episode",
        purpose="Defines the canonical state envelope for a single episode or chapter.",
        write_policy="read_only_contract_until_stage147_project_manifest_body",
        fields=(
            NarrativeFieldSpec("episode_id", "string", True, "Stable episode identifier.", "episode manifest"),
            NarrativeFieldSpec("series_id", "string", True, "Parent series identifier.", "series state"),
            NarrativeFieldSpec("order_index", "integer", True, "Canonical sequence number.", "episode manifest"),
            NarrativeFieldSpec("premise", "string", True, "Episode-level dramatic premise.", "episode planning packet"),
            NarrativeFieldSpec("scene_order", "list[string]", True, "Approved ordered scene identifiers.", "scene packet set"),
            NarrativeFieldSpec("continuity_anchor", "string", True, "Primary continuity checkpoint for the episode.", "continuity packet"),
        ),
    )


def build_continuity_state_contract() -> NarrativeStateContract:
    return NarrativeStateContract(
        name="ContinuityState",
        scope="continuity",
        purpose="Declares cross-scene and cross-episode continuity checkpoints without auto-repair authority.",
        write_policy="read_only_contract_until_stage149_gate_allows_memory_entry",
        fields=(
            NarrativeFieldSpec("continuity_id", "string", True, "Stable continuity packet identifier.", "continuity packet"),
            NarrativeFieldSpec("timeline_position", "string", True, "Normalized chronology position.", "continuity packet"),
            NarrativeFieldSpec("open_threads", "list[string]", True, "Outstanding promises that later scenes must respect.", "continuity packet"),
            NarrativeFieldSpec("resolved_threads", "list[string]", True, "Promises already closed with evidence.", "continuity packet"),
            NarrativeFieldSpec("contradiction_watchlist", "list[string]", True, "Known continuity risks requiring human review.", "contradiction classifier"),
            NarrativeFieldSpec("repair_policy", "string", True, "Documents that repair stays manual and approval-first.", "stage145 constitution"),
        ),
    )


def build_continuity_rules() -> tuple[ContinuityRule, ...]:
    return (
        ContinuityRule("chronology_preserved", "Timeline anchors must never move implicitly between scenes.", True, "continuity state contract"),
        ContinuityRule("character_knowledge_preserved", "Character knowledge cannot exceed reveal-authorized boundaries.", True, "character + reveal state"),
        ContinuityRule("world_rule_preserved", "Setting rules remain stable across all episodes.", True, "world state contract"),
        ContinuityRule("promise_tracking_preserved", "Open and resolved threads must remain explicitly declared.", True, "continuity state contract"),
        ContinuityRule("repair_manual_only", "Continuity fixes remain human-approved and are not auto-applied.", True, "stage145 constitution"),
        ContinuityRule("provider_zero_preserved", "No continuity step may trigger live provider calls.", True, "release gate invariants"),
    )
