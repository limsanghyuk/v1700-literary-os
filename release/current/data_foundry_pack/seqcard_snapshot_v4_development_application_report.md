# SeqCard Snapshot v4 Development Application Report

Date: 2026-07-03  
Status: metadata-only application report  
Scope: Stage243 Data Bridge / Macro Planner Candidate preparation

## 0. Executive Decision

SeqCard v4 has been inspected as a metadata-only snapshot candidate.

The new snapshot materially strengthens the Stage243 Data Bridge and improves Macro Planner Candidate fixture coverage.

It does not promote Macro Planner, Full Author, or Live Generation readiness.

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

## 1. Snapshot Summary

```text
source_file: seqcard_ko.zip
sha256: 89b3ab196c363dec52621ed8129a665a9d81b14978f7eb105f037096826f70b1
size_bytes: 18,256,665
zip_crc: pass
entries: 1,824
files: 1,820
uncompressed_size_bytes: 52,458,135
```

Metadata counts:

```text
seqcard_jsonl_files: 577
episode_meta_files: 577
series_count_by_filename: 29
seqcard_records: 37,800
json_parse_errors: 0
jsonl_parse_errors: 0
```

## 2. Safety Review

The uploaded archive is source-bearing because it contains `original_extracted` and dump text files.

```text
original_extracted_files_present: 608
dump_txt_files_present: 2
source_bearing_archive: true
hub_raw_archive_allowed: false
```

Only aggregate metadata and safe manifest values may be used in the hub.

The following remain false:

```text
raw_text_exported: false
raw_vectors_exported: false
token_exported: false
adapter_weight_exported: false
provider_called: false
runtime_generation: false
promotion_claim: false
```

No `.safetensors` files were present. No risk patterns were found in the safe scan scope.

## 3. Delta from v3

Baseline v3:

```text
series_count_by_filename: 22
seqcard_jsonl_files: 457
episode_meta_files: 457
seqcard_records: 29,873
```

Current v4:

```text
series_count_by_filename: 29
seqcard_jsonl_files: 577
episode_meta_files: 577
seqcard_records: 37,800
```

Delta:

```text
series_added_count: 7
seqcard_jsonl_files_added: 120
episode_meta_files_added: 120
seqcard_records_added: 7,927
record_growth_ratio: approximately 26.5%
```

Added series by filename:

```text
W: 16
그들이사는세상: 16
밀회: 16
스카이캐슬: 20
시크릿가든: 20
스토브리그: 16
추적자: 16
```

## 4. Core Distribution

```text
CONFLICT: 6,170
PERIL: 4,845
REVELATION: 4,303
ESTABLISH: 3,122
BOND: 2,887
LOSS: 2,863
DESIRE: 2,429
HOOK: 2,310
RELIEF: 1,802
ORACLE: 1,478
ROMANCE: 1,282
REVERSAL: 1,113
PUNISH: 1,062
RESCUE: 707
REUNION: 469
INTRO: 324
```

All 16 core scene-function taxonomy values are present.

## 5. Core2 Distribution

```text
CONFLICT: 4,041
PERIL: 3,145
HOOK: 2,921
BOND: 2,910
DESIRE: 2,231
REVELATION: 2,109
LOSS: 1,963
RELIEF: 1,862
ORACLE: 1,293
ESTABLISH: 1,025
ROMANCE: 970
PUNISH: 854
REVERSAL: 671
RESCUE: 324
INTRO: 228
REUNION: 155
```

The `core` and `core2` distributions should be used for scene-function pair analysis, not for raw-text reproduction.

## 6. Development Application

SeqCard v4 should be applied to development as follows:

### 6.1 Data Bridge

Update the active metadata snapshot reference from v3 to v4.

Required hub artifacts:

```text
seqcard_snapshot_v4_manifest.json
seqcard_snapshot_v4_delta_from_v3.json
seqcard_snapshot_v4_development_application_report.md
```

### 6.2 Macro Planner Candidate Fixtures

SeqCard v4 improves coverage for:

```text
season arc fixture diversity
episode arc fixture diversity
scene grid fixture diversity
plant/payoff fixture examples
character arc fixture examples
negative control construction
heldout structure fixture generation
```

### 6.3 Evaluation Hard-Rule Gate

The added data increases the need for a hard-rule gate because weighted scores alone can hide structural failures.

The next design work should create:

```text
macro_planner_hard_rule_gate.json
macro_planner_disqualification_rules.json
macro_candidate_scorecard_schema.json
macro_candidate_final_verdict_fixture.json
macro_planner_evaluation_v2_report.md
```

## 7. Promotion Interpretation

SeqCard v4 supports the Macro Planner Prototype data band because it has 37,800 scene/function records, which lies within the previously proposed 20,000-50,000 prototype range.

However, it does not reach the Macro Planner Promotion Candidate data band, which previously required approximately:

```text
50-100 works
1,000-2,000 episodes
70,000-150,000 scene function records
```

Therefore:

```text
Macro Planner Prototype Data Support = strengthened
Macro Planner Promotion Candidate = not yet proven
Macro Planner Promotion = blocked
Full Author Promotion = blocked
Live Generation Readiness = blocked
```

## 8. Final Decision

SeqCard v4 should be adopted as the current metadata-only development snapshot for Stage243 planning and Macro Planner Candidate fixture preparation.

It must not be adopted as raw training input, live generation evidence, or promotion evidence by itself.

Final state:

```text
SeqCard v4 metadata-only snapshot = adopted for planning
Stage243 Data Bridge = strengthened
Macro Planner Candidate fixtures = should use v4
Macro Planner Promotion = blocked
Full Author Promotion = blocked
Live Generation Readiness = blocked
```
