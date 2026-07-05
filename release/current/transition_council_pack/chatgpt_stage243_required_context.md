# ChatGPT Stage243 Required Context

Date: 2026-07-02
Hub root: `C:\AI_Codex\codex-work\gpt`

This file is the compact briefing ChatGPT should receive before discussing Stage243. It summarizes what Codex loaded into the hub from the local evidence handoff. It does not include raw scripts, API keys, tokens, embedding vectors, or adapter weights.

Start here for the full Codex work/method handoff:

```text
release/current/transition_council_pack/chatgpt_latest_hub_loadout.md
release/current/transition_council_pack/stage243_schema_promotion_registry_handoff.md
release/current/transition_council_pack/codex_work_method_handoff_for_chatgpt.md
```

## 1. What Codex Added To The Hub

Markdown documents:

```text
docs/development/local_evidence_handoff_analysis.md
docs/development/stage243_local_evidence_assessment.md
docs/architecture/pass4_to_pass7_contract_blueprint.md
```

JSON reports:

```text
release/current/transition_council_pack/local_evidence_handoff_summary.json
release/current/data_foundry_pack/corpus_ko_manifest_v2_plan.json
release/current/data_foundry_pack/seqcard_corpus_linkage_plan.json
release/current/data_foundry_pack/claude_seqcard_ko_snapshot_20260703_manifest.json
release/current/data_foundry_pack/seqcard_snapshot_v3_manifest.json
release/current/data_foundry_pack/seqcard_corpus_linkage_v3.json
release/current/data_foundry_pack/scene_function_taxonomy_16.json
release/current/data_foundry_pack/scene_function_pair_distribution_v3.json
release/current/data_foundry_pack/seqcard_snapshot_v3_delta_from_v2.json
release/current/data_foundry_pack/schema_registry.json
release/current/measured_learning_pack/promotion_evidence_registry.json
release/current/measured_learning_pack/4070_spe10_pathb_evidence_card.json
release/current/season_wiring_pack/pass_contract_registry_plan.json
```

Latest Claude SeqCard snapshot note:

```text
release/current/data_foundry_pack/claude_seqcard_ko_snapshot_20260703_note.md
```

## 2. Safety Declaration

The loaded hub materials are metadata-only.

```text
raw_text_exported: false
raw_vectors_exported: false
token_exported: false
adapter_weight_exported: false
provider_called: false
runtime_training_started: false
canonical_mutation_started: false
```

## 3. Stage243 Decision

Stage243 can proceed, but only as:

```text
Data Bridge + Learning Bridge + Season Wiring Preflight
```

Stage243 must not be described as live generation readiness or full author replacement.

## 4. Data Bridge Context

`corpus_ko` is real and substantial:

```text
total_files: 13,882
total_bytes: 2,911,793,786
scene_files: 2,559
scene_records: 156,407
chunk_files: 2,497
chunk_records: 254,731
feature_files: 2,497
feature_records: 147,631
```

Boundary:

```text
Use metadata, inventory, schema, and feature summaries.
Do not export raw text, chunks, scripts, source archives, vectors, tokens, or weights.
```

The old `manifest.json` is historical only. It fails strict JSON parsing. Stage243 needs:

```text
manifest_v2.json
```

## 5. SeqCard Context

`seqcard_ko` is the scene function and intent metadata layer.

```text
series_count: 13
episode_count: 290
strict_parsed_scene_records: 19,377
summary_scene_count: 19,376
```

There is one count mismatch to resolve.

Current linkage:

```text
exact_episode_matches: 205 / 290
exact_series_matches: 9 / 13
```

Stage243 needs:

```text
seqcard_corpus_linkage.json
```

Additional current Claude snapshot:

```text
source: C:\claude\db\seqcard_ko.zip
snapshot: release/current/data_foundry_pack/claude_seqcard_ko_snapshot_20260703
seqcard_jsonl_files: 457
episode_meta_json_files: 457
series_arc_json_files: 23
seqcard_records: 29,873
parse_errors: 0
raw original_extracted copied: false
```

Important: the existing linkage baseline used 290 episode records. The new 457-file Claude ZIP snapshot should trigger linkage regeneration before final coverage claims.

SeqCard v3 absorption has now produced:

```text
seqcard_snapshot_v3_manifest.json
seqcard_corpus_linkage_v3.json
scene_function_taxonomy_16.json
scene_function_pair_distribution_v3.json
seqcard_snapshot_v3_delta_from_v2.json
```

Latest filename-stem linkage summary:

```text
exact_episode: 336
series_only: 1
unmatched: 120
```

SeqCard v4 changed ZIP absorption has now produced:

```text
seqcard_snapshot_v4_manifest.json
seqcard_corpus_linkage_v4.json
scene_function_taxonomy_16_v4.json
scene_function_pair_distribution_v4.json
seqcard_snapshot_v4_delta_from_v3.json
```

Latest v4 inventory and linkage:

```text
source_zip_sha256: 89b3ab196c363dec52621ed8129a665a9d81b14978f7eb105f037096826f70b1
seqcard_jsonl_files: 577
episode_meta_files: 577
seqcard_records: 37,166
series_count_by_filename: 29
exact_episode: 456
series_only: 1
unmatched: 120
```

Use v4 as the current SeqCard local hub baseline. v3 remains a prior comparison point.

SeqCard v5 changed ZIP absorption adds EpisodeArc and SequenceBlueprint layers:

```text
source_zip_sha256: cf8ad0f0045d37d6725a44675f7918bccf696ea3749f88d4fb97211d503a70e0
seqcard_jsonl_files: 648
episode_meta_files: 648
episode_arc_files: 648
seqblueprint_files: 648
seqcard_records: 41,168
seqblueprint_records: 6,146
series_count_by_filename: 33
exact_episode: 476
series_only: 1
unmatched: 171
```

Use v5 as the current local hub baseline. It can strengthen P8.1 cross-level validation, but it does not replace the missing `full_season_*` validation input files.

Stage243 schema/evidence registry status:

```text
schema_registry.json: upgraded to v2.2-stage243-v5
promotion_evidence_registry.json: created
Pass4-Pass7 preflight fixtures: created
Macro Planner Candidate fixtures: created
Blind Structural Evaluation fixture: created
Multi-candidate Blind Structural Evaluation set: created
P8.1 local validation result: pass_with_warning
Macro Planner Promotion: blocked
Full Author Promotion: blocked
Live Generation Readiness: blocked
```

P8.1 rerun status after syncing the four remote full-season inputs:

```text
json_parse_pass: true
schema_validation_pass: true
schema_error_count: 0
cross_level_integrity_pass: true
integrity_error_count: 0
integrity_warning_count: 11
boundary_invariants_pass: true
overall_validation_status: pass_with_warning
hard_rule_pass_from_self_check: false
gate_a_ready_after_validation: false
scorecard_preflight_allowed: false
```

Interpretation:

```text
The missing-input blocker is resolved.
Gate A is still blocked because hard_rule_pass is false.
P9 Scorecard Preflight remains blocked.
```

## 6. 4070 Learning Context

`4070_oneclick` contains SP-E.10 Path B v3 evidence:

```text
R1 W0 0.580 -> W1 0.600 CI 0.5393 adopt
R2 W0 0.596 -> W1 0.620 CI 0.5598 adopt
R3 W0 0.616 -> W1 0.644 CI 0.5846 adopt
R4 W0 0.640 -> W1 0.708 CI 0.6516 adopt
R5 W0 0.712 -> W1 0.808 CI 0.7592 adopt
```

Decision:

```text
SP-E.10 Path B v3 = KEEP as show/tell craft-axis evidence.
Macro planner promotion = BLOCKED.
Full author promotion = BLOCKED.
```

## 7. Season Wiring Context

Existing contracts:

```text
Pass1 premise -> WorkSpec
Pass2 causality -> Beat[]
Pass3 scene brief -> SceneBrief[]
Pass4 RetrievalPacket fixture
Pass5 DraftPacket fixture-only envelope
Pass6 GateResult fixture
Pass7 PanelResult fixture
Macro Candidate SeasonArc fixture
Macro Candidate EpisodeArc fixture
Macro Candidate SceneGrid fixture
Macro Candidate Plant/Payoff fixture
Macro Candidate CharacterArc fixture
Blind Structural Evaluation fixture
Macro planner scoring rubric
```

Missing promotion evidence:

```text
Real held-out metadata-only structure packs beyond fixture examples
Hard-rule and weighted-score threshold separation
Gate B human review protocol
Remote authority confirmation if GitHub is the chosen authority
```

Stage243 now has a fixture-only multi-candidate/held-out evaluation set. It still must not claim Macro Planner promotion until real held-out metadata-only packs and a human-reviewed Gate B protocol exist.

## 8. Current Completed Local Tasks

Completed metadata-only local tasks:

```text
1. manifest_v2.json
2. seqcard_corpus_linkage.json
3. seqcard_corpus_linkage_v3.json
4. schema_registry.json v2-stage243-v3
5. pass_contract_registry.md
6. page18_boundary_hardening.md
7. 4070_evidence_card.md
8. promotion_evidence_registry.json
9. Pass4-Pass7 preflight fixtures
10. Macro Planner Candidate contract fixtures
11. Blind Structural Evaluation fixture
12. Multi-candidate Blind Structural Evaluation fixture set
```

Safe next local tasks:

```text
1. Build real held-out metadata-only structure packs
2. Separate hard-rule failures from weighted-score thresholds
3. Define Gate B human review protocol
4. Confirm remote authority reflection if GitHub/remote is chosen as authority
```

Do not ask for:

```text
raw scripts
full JSONL rows containing text
API keys
local token files
embedding arrays
adapter weights
source archives
```

## 9. One-Line Summary

GPT V1700 is no longer asking whether local data exists. It is now entering the stage where local data must be safely linked into an authoring closed loop through explicit metadata-only contracts.
