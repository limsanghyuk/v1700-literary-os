# ChatGPT Latest Hub Loadout

Date: 2026-07-02
Hub root: `C:\AI_Codex\codex-work\gpt`

This document is the latest ChatGPT-facing explanation of what Codex loaded into the hub, how the work was performed, and which artifacts should be used for Stage243 reasoning.

## 1. Current Purpose

The user supplied the latest Claude drama-analysis package at `C:\claude\db\seqcard_ko.zip`. Codex stored the ZIP locally and copied the Stage243-relevant authored outputs into the hub while preserving the Page18 safety boundary.

The goal was not to expose raw drama scripts. The goal was to preserve Claude's analysis products and make their status understandable to ChatGPT.

## 2. Source And Snapshot

Source:

```text
C:\claude\db\seqcard_ko.zip
```

Hub snapshot:

```text
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_snapshot_20260703
```

Snapshot manifest:

```text
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_snapshot_20260703_manifest.json
```

Snapshot note:

```text
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_snapshot_20260703_note.md
```

Integrity reports:

```text
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_zip_integrity_report_20260703.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_zip_integrity_report_20260703.json
```

SeqCard v3 metadata-only absorption outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v3_manifest.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v3_manifest_report.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_corpus_linkage_v3.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_corpus_linkage_v3_report.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\scene_function_taxonomy_16.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\scene_function_pair_distribution_v3.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v3_delta_from_v2.json
```

SeqCard v4 changed ZIP absorption outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_snapshot_20260703_194028
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_snapshot_20260703_194028_manifest.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_snapshot_20260703_194028_note.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v4_manifest.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v4_manifest_report.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_corpus_linkage_v4.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_corpus_linkage_v4_report.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\scene_function_taxonomy_16_v4.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\scene_function_pair_distribution_v4.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v4_delta_from_v3.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_zip_integrity_report_20260703_194028.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_zip_integrity_report_20260703_194028.md
```

SeqCard v5 EpisodeArc/SequenceBlueprint absorption outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\claude_seqcard_ko_snapshot_20260705_160707
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v5_manifest.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v5_manifest_report.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_corpus_linkage_v5.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_corpus_linkage_v5_report.md
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\scene_function_taxonomy_16_v5.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\scene_function_pair_distribution_v5.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\episode_arc_inventory_v5.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\sequence_blueprint_inventory_v5.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_snapshot_v5_delta_from_v4.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_v5_p8_1_schema_mapping.json
C:\AI_Codex\codex-work\gpt\release\current\data_foundry_pack\seqcard_v5_p8_1_schema_mapping.md
```

P8.1 local validation outputs:

```text
C:\AI_Codex\codex-work\gpt\tools\validate_full_season_p8_1.py
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\full_season_candidate_package_fixture_v1.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\full_season_candidate_package_schema_v1.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\full_season_hard_rule_self_check_v1.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\full_season_validation_protocol_p8_1.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\full_season_validation_result_p8_1.json
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\p8_1_local_validation_execution_report_20260705.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\p8_1_local_validation_rerun_report_20260705.md
```

Promotion/evidence registry outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\measured_learning_pack\promotion_evidence_registry.json
C:\AI_Codex\codex-work\gpt\release\current\measured_learning_pack\promotion_evidence_registry_report.md
```

Pass4-Pass7 preflight outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\pass4_retrievalpacket_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\pass5_draftpacket_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\pass6_gateresult_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\pass7_panelresult_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\pass4_to_pass7_preflight_report.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\pass4_to_pass7_preflight_report.md
```

Macro Planner Candidate preflight outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_candidate_season_arc_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_candidate_episode_arc_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_candidate_scene_grid_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_candidate_plant_payoff_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_candidate_character_arc_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_candidate_preflight_report.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_candidate_preflight_report.md
```

Blind Structural Evaluation outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_scoring_rubric.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\blind_structural_evaluation_fixture.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_evaluation_report.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_evaluation_report.md
```

Multi-candidate Blind Structural Evaluation outputs:

```text
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\blind_structural_evaluation_multicandidate_set.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\negative_control_macro_fixtures.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\heldout_season_structure_fixtures.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_metric_thresholds.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_multicandidate_evaluation_report.json
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack\macro_planner_multicandidate_evaluation_report.md
```

Codex/ChatGPT work split and developer brief:

```text
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\chatgpt_codex_work_division_protocol.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\codex_chatgpt_work_split_20260703.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\developer_brief_codex_work_20260703.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\hub_load_verification_20260703.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\seqcard_v4_load_verification_20260703_194028.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\local_latest_hub_content_check_20260703.json
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\local_latest_hub_content_check_20260703.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\claude_drama_reflection_docx_analysis_20260705.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\developer_hub_latest_state_survey_20260705.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\seqcard_v5_load_verification_20260705_160707.md
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\p8_1_local_validation_rerun_report_20260705.md
```

Schema/promotion handoff:

```text
C:\AI_Codex\codex-work\gpt\release\current\transition_council_pack\stage243_schema_promotion_registry_handoff.md
```

Local ZIP copy:

```text
C:\AI_Codex\local_only\incoming\seqcard_ko_20260703_latest.zip
```

## 3. What Codex Copied

Included:

```text
AUTHORING_SPEC.md
_ALL_series_arc.json
authored/*.seqcard.jsonl
authored/*.episode_meta.json
authored/*series_arc.json
authored/*.py
```

Excluded:

```text
original_extracted/**
authored/_dump*.txt
raw extracted episode text
```

## 4. Method

Codex used a conservative local-evidence method:

```text
1. Inspect source directory inventory.
2. Separate authored analysis products from raw extracted text.
3. Copy only Stage243-relevant authored outputs.
4. Generate a metadata-only manifest.
5. Parse all copied JSON/JSONL evidence.
6. Scan copied files for secret, token, private-key, and model-artifact leakage patterns.
7. Update the ChatGPT handoff documents with the new result.
```

Codex did not:

```text
paste raw drama text
copy original_extracted text files
copy _dump text files
export embedding vectors
export API keys or tokens
export adapter weights
call providers
start training
mutate canonical runtime state
```

## 5. Result

Current 2026-07-03 ZIP snapshot inventory:

```text
source_zip_entries: 1,415
source_zip_sha256: be257bb255bfa3014bf2d051ab073cceff53e8fb730e27d222aebc306b311f13
copied_files_total: 941
copied_bytes_total: 12,879,804
seqcard_jsonl_files: 457
episode_meta_json_files: 457
series_arc_json_files: 23
python_scripts: 3
markdown_files: 1
seqcard_records: 29,873
parse_errors: 0
```

Latest changed ZIP snapshot, loaded as v4:

```text
source_zip_entries: 1,824
source_zip_sha256: 89b3ab196c363dec52621ed8129a665a9d81b14978f7eb105f037096826f70b1
seqcard_jsonl_files: 577
episode_meta_json_files: 577
series_arc_json_files: 29
seqcard_records: 37,166
series_count_by_filename: 29
jsonl_parse_errors: 0
json_parse_errors: 0
linkage_v4_exact_episode: 456
linkage_v4_series_only: 1
linkage_v4_unmatched: 120
```

Previous local-directory snapshot, now superseded:

```text
copied_files_total: 815
copied_bytes_total: 11,944,757
seqcard_jsonl_files: 420
episode_meta_json_files: 390
seqcard_records: 27,884
```

Verification:

```text
JSON/JSONL parse: OK
ZIP CRC/integrity: OK
source ZIP SHA256 matches local incoming copy: true
snapshot hashes match allowed ZIP entries: true
SeqCard v3 manifest/linkage/taxonomy JSON parse: OK
schema_registry v2 / promotion_evidence_registry JSON parse: OK
schema/promotion handoff loaded for ChatGPT: true
Pass4-Pass7 preflight fixtures: created and JSON parse OK
Macro Planner Candidate fixtures: created and JSON parse OK
Multi-candidate Blind Structural Evaluation set: created and JSON parse OK
Negative/control and held-out fixture files: created and JSON parse OK
raw original_extracted copied: false
dump txt copied: false
secret/token/private-key/model-artifact scan: OK
provider_called: false
runtime_training_started: false
```

## 6. Stage243 Meaning

This snapshot changes the SeqCard evidence state.

Earlier Stage243 linkage was based on an older effective baseline:

```text
seqcard episode records: 290
seqcard_corpus_linkage.json basis: 290 episode records
```

The previous Claude local-directory snapshot contained:

```text
seqcard_jsonl_files: 420
seqcard_records: 27,884
```

The latest 2026-07-03 ZIP snapshot contains:

```text
seqcard_jsonl_files: 457
seqcard_records: 29,873
```

Therefore:

```text
The previous seqcard_corpus_linkage.json remains useful as a prior baseline.
It should not be treated as final coverage for the latest Claude ZIP snapshot.
Use seqcard_corpus_linkage_v4.json for the latest filename-stem linkage baseline.
```

## 7. Related Hub Artifacts

Read these in order:

```text
release/current/transition_council_pack/chatgpt_latest_hub_loadout.md
release/current/transition_council_pack/codex_work_method_handoff_for_chatgpt.md
release/current/transition_council_pack/page18_boundary_hardening.md
release/current/data_foundry_pack/claude_seqcard_ko_snapshot_20260703_manifest.json
release/current/data_foundry_pack/claude_seqcard_ko_snapshot_20260703_note.md
release/current/data_foundry_pack/claude_seqcard_ko_zip_integrity_report_20260703.md
release/current/data_foundry_pack/seqcard_snapshot_v3_manifest.json
release/current/data_foundry_pack/seqcard_corpus_linkage_v3.json
release/current/data_foundry_pack/scene_function_taxonomy_16.json
release/current/data_foundry_pack/scene_function_pair_distribution_v3.json
release/current/data_foundry_pack/seqcard_snapshot_v3_delta_from_v2.json
release/current/measured_learning_pack/promotion_evidence_registry.json
release/current/transition_council_pack/stage243_schema_promotion_registry_handoff.md
release/current/season_wiring_pack/pass4_to_pass7_preflight_report.md
release/current/data_foundry_pack/manifest_v2.json
release/current/data_foundry_pack/schema_registry.json
release/current/season_wiring_pack/pass_contract_registry.md
release/current/measured_learning_pack/4070_evidence_card.md
```

## 8. Current Recommendation

Stage243 can still proceed as:

```text
Data Bridge + Learning Bridge + Season Wiring Preflight
```

But SeqCard linkage coverage should be recalculated before any stronger claim about full season wiring readiness.
