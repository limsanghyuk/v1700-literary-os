# P8.2 Local Deeper Integrity Execution Report

Date: 2026-07-05
Status: local execution completed; hard-rule remains blocked
Scope: Stage243 P8.2 / 11 deeper integrity checks / metadata-only execution

## Summary

- Overall deeper integrity status: `manual_review_required`
- pass: `0`
- pass_with_warning: `4`
- manual_review_required: `7`
- fail_hard_rule: `0`
- blocked: `0`
- hard_rule_pass: `false`
- gate_a_ready: `false`
- scorecard_preflight_allowed: `false`

## Boundary

- provider_call_count: `0`
- live prose generation: `false`
- canonical mutation: `false`
- training update: `false`
- adapter promotion: `false`
- promotion claim: `false`
- P9 Scorecard Preflight: `not run`

## Check Results

### series_to_season_integrity

- status: `manual_review_required`
- required_next_action: Inspect instantiated FullSeriesArcSpec and SeasonPlan fields before hard-rule pass.
- evidence: `{"series_id_present": true, "season_id_present": true, "target_episode_count": 16, "full_series_arc_spec_ref_present": true, "season_plan_ref_present": true}`
- limitations: `["Fixture exposes references and package identity, but not instantiated season goal, central conflict axis, entry state, or exit state values.", "Metadata-only references cannot prove series-to-season narrative alignment."]`

### season_to_episode_integrity

- status: `manual_review_required`
- required_next_action: Provide or inspect instantiated EpisodeArcChain nodes for the 16-episode candidate.
- evidence: `{"target_episode_count": 16, "episode_arc_chain_ref_status": "present", "seqcard_episode_ids": 648, "episode_arc_files": 648, "seqcard_without_episode_arc": [], "episode_arc_without_seqcard": []}`
- limitations: `["V5 corpus-level EpisodeArc coverage is complete, but the fixture does not expose the actual 16 ordered episode nodes.", "Midpoint, crisis, climax, resolution, and episode transition continuity cannot be proven from counts alone."]`

### episode_to_sequence_integrity

- status: `pass_with_warning`
- required_next_action: Bind fixture episode nodes to concrete sequence blueprint IDs before hard-rule pass.
- evidence: `{"fixture_target_episode_count": 16, "fixture_sequence_blueprint_count": 16, "v5_sequence_count_min": 2, "v5_sequence_count_max": 24, "v5_sequence_count_mean": 9.4846, "seqcard_without_seqblueprint": [], "seqblueprint_without_seqcard": []}`
- limitations: `["Corpus-level episode-to-sequence coverage is complete, but fixture-specific episode-to-sequence IDs are not enumerated."]`

### sequence_to_scene_integrity

- status: `pass_with_warning`
- required_next_action: Bind fixture sequence spans to concrete scene blueprint IDs before hard-rule pass.
- evidence: `{"sequence_blueprint_record_count": 6146, "records_per_episode": {"min": 2, "max": 24, "mean": 9.4846}, "member_scene_warning_count": 0, "member_scene_warning_samples": [], "fixture_scene_blueprint_count": 48}`
- limitations: `["Member-scene metadata has no warning samples, but required transition support is not available as exported fixture instances."]`

### scene_to_renderer_packet_integrity

- status: `pass_with_warning`
- required_next_action: Expose metadata-only scene_id to renderer_packet_id mapping for hard-rule pass.
- evidence: `{"fixture_scene_blueprint_count": 48, "fixture_renderer_prompt_packet_count": 48, "renderer_refs_present": true, "provider_call_allowed": false, "prose_generation_allowed": false, "canonical_mutation_allowed": false}`
- limitations: `["Counts and safety boundary align, but packet-by-scene bijection is not instantiated in exported metadata."]`

### plant_payoff_integrity

- status: `manual_review_required`
- required_next_action: Provide metadata-only plant/payoff ledger IDs and timing links.
- evidence: `{"fixture_declared_status": "not_run", "p8_1_warning_present": true}`
- limitations: `["Plant/payoff ledgers are not exported as instantiated metadata, so orphan plant, payoff-without-plant, timing, and unresolved setup risks cannot be cleared."]`

### character_arc_integrity

- status: `manual_review_required`
- required_next_action: Provide metadata-only character arc transition graph with causal supports.
- evidence: `{"fixture_declared_status": "not_run", "p8_1_warning_present": true}`
- limitations: `["Character state, belief, motivation, and agency transitions are not exported as instantiated metadata."]`

### relationship_arc_integrity

- status: `manual_review_required`
- required_next_action: Provide metadata-only relationship transition graph with supporting event IDs.
- evidence: `{"fixture_declared_status": "not_run", "p8_1_warning_present": true}`
- limitations: `["Relationship state transitions and reversal causes are not exported as instantiated metadata."]`

### causal_spine_integrity

- status: `manual_review_required`
- required_next_action: Provide metadata-only causal edge graph linking episode, sequence, and scene IDs.
- evidence: `{"fixture_declared_status": "not_run", "p8_1_warning_present": true}`
- limitations: `["Causal dependency edges across episodes and sequences are not exported as instantiated metadata."]`

### hook_chain_integrity

- status: `manual_review_required`
- required_next_action: Provide metadata-only hook ledger with downstream consequence IDs.
- evidence: `{"fixture_declared_status": "not_run", "p8_1_warning_present": true}`
- limitations: `["Hook-to-consequence links are not exported as instantiated metadata."]`

### genre_rhythm_integrity

- status: `pass_with_warning`
- required_next_action: Bind candidate season genre mode and per-episode rhythm targets to scene-function metadata.
- evidence: `{"scene_function_records_total": 41168, "core_missing": 0, "all_16_present_in_core": true, "unique_scene_function_pairs": 265, "core2_none_treated_as_missing": true}`
- limitations: `["Scene-function distribution is strong corpus-level rhythm evidence, but candidate-specific genre mode and rhythm target are not instantiated."]`

## Final Decision

P8.2 did execute the 11 deeper integrity checks at the available metadata level. The result does not permit Gate A or P9 because seven checks still require instantiated narrative ledgers or human review before hard-rule pass can be claimed.

Next local requirement: provide metadata-only instantiated ledgers for episode nodes, sequence/scene IDs, plant-payoff links, character/relationship transitions, causal edges, and hook consequences. Until then, P9 remains blocked.
