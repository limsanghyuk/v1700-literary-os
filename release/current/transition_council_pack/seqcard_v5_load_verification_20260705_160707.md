# SeqCard v5 Load Verification 2026-07-05 160707

Source: `C:\claude\db\seqcard_ko.zip`

## Result

The changed SeqCard ZIP was detected and loaded into the local hub as a new v5 metadata snapshot.

```text
previous_v4_sha256: 89b3ab196c363dec52621ed8129a665a9d81b14978f7eb105f037096826f70b1
current_v5_sha256: cf8ad0f0045d37d6725a44675f7918bccf696ea3749f88d4fb97211d503a70e0
zip_crc_testzip_ok: true
local_only_zip_copy: C:\AI_Codex\local_only\incoming\seqcard_ko_20260705_160707.zip
```

## Loaded Hub Artifacts

```text
release/current/data_foundry_pack/claude_seqcard_ko_snapshot_20260705_160707
release/current/data_foundry_pack/seqcard_snapshot_v5_manifest.json
release/current/data_foundry_pack/seqcard_snapshot_v5_manifest_report.md
release/current/data_foundry_pack/seqcard_corpus_linkage_v5.json
release/current/data_foundry_pack/seqcard_corpus_linkage_v5_report.md
release/current/data_foundry_pack/scene_function_taxonomy_16_v5.json
release/current/data_foundry_pack/scene_function_pair_distribution_v5.json
release/current/data_foundry_pack/episode_arc_inventory_v5.json
release/current/data_foundry_pack/sequence_blueprint_inventory_v5.json
release/current/data_foundry_pack/seqcard_snapshot_v5_delta_from_v4.json
release/current/data_foundry_pack/seqcard_v5_p8_1_schema_mapping.json
release/current/data_foundry_pack/seqcard_v5_p8_1_schema_mapping.md
```

## Inventory

```text
source_zip_entries: 3,301
snapshot_files_total: 2,672
seqcard_jsonl_files: 648
episode_meta_files: 648
episode_arc_files: 648
seqblueprint_files: 648
series_arc_files: 63
seqcard_records: 41,168
seqblueprint_records: 6,146
series_count_by_filename: 33
json_parse_errors: 0
jsonl_parse_errors: 0
```

## Delta From v4

```text
seqcard_jsonl_delta: +71
episode_meta_delta: +71
seqcard_record_delta: +4,002
new_episode_arc_files: 648
new_seqblueprint_files: 648
new_seqblueprint_records: 6,146
```

## Linkage v5

```text
record_count: 648
exact_episode: 476
series_only: 1
unmatched: 171
```

## Safety

```text
raw_text_exported: false
full_jsonl_rows_exported: false
heading_title_intent_gist_values_exported: false
original_extracted_exported: false
dump_txt_exported: false
source_zip_under_release_current: false
provider_called: false
runtime_training_started: false
canonical_mutation_started: false
promotion_claim: false
```

## P8.1 Meaning

SeqCard v5 provides richer metadata for P8.1 cross-level checks. It does not by itself satisfy P8.1, because the required `full_season_*` input files are still missing locally.
