# Local / Remote SeqCard v4 Reconciliation Report

Date: 2026-07-03  
Status: authority reconciliation report  
Scope: Stage243 Data Bridge / SeqCard v4 / local hub vs remote GitHub

## 0. Purpose

This report reconciles the local Codex hub verification report with the remote GitHub SeqCard v4 metadata manifest.

The goal is to avoid treating two different authority states as the same artifact:

```text
Local Hub Authority = C:\AI_Codex\codex-work\gpt\release\current
Remote GitHub Authority = limsanghyuk/v1700-literary-os / corpus-absorption-formula-bridge-handoff
```

## 1. Local Hub Verification Report

The developer reported the following local verification result:

```text
checked_root: C:\AI_Codex\codex-work\gpt\release\current
local_hub_verified: yes
remote_github_verified: no
is_git_repo: false
json_parse: pass
json_files_checked: 1,525
secret_scan: pass
archive_or_model_artifact_scan: pass
raw_source_leakage_scan: pass
provider_call_count: 0
runtime_generation: false
promotion_claim: false
```

The local hub result packet paths reported by the developer:

```text
release/current/transition_council_pack/local_latest_hub_content_check_20260703.json
release/current/transition_council_pack/local_latest_hub_content_check_20260703.md
```

These files are local hub artifacts until separately pushed or loaded into the remote GitHub authority branch.

## 2. Local SeqCard v4 Authority Values

The developer reported the latest local SeqCard v4 core values as:

```text
seqcard_jsonl_files: 577
episode_meta_files: 577
seqcard_records: 37,166
linkage_v4 exact_episode: 456
linkage_v4 unmatched: 120
schema_registry: 2.1-stage243-v4
```

Local authority interpretation:

```text
Local cleaned hub snapshot = verified yes
Local schema registry = 2.1-stage243-v4
Local linkage_v4 = available locally
Remote GitHub verification from this local path = not possible because the checked root is not a Git repository
```

## 3. Remote GitHub SeqCard v4 Manifest Values

The current remote GitHub manifest created from the uploaded ZIP metadata contains:

```text
seqcard_jsonl_files: 577
episode_meta_files: 577
series_count_by_filename: 29
seqcard_records: 37,800
json_parse_errors: 0
jsonl_parse_errors: 0
```

Remote authority interpretation:

```text
Remote manifest = uploaded ZIP snapshot aggregate
Remote manifest is source-archive-derived metadata, not necessarily identical to the locally cleaned hub snapshot
```

## 4. Reconciliation Finding

There is a record-count discrepancy:

```text
remote_uploaded_zip_snapshot_records: 37,800
local_cleaned_hub_snapshot_records: 37,166
difference: 634
```

This difference must not be silently overwritten.

The likely interpretation is:

```text
Remote v4 manifest = aggregate metadata from the uploaded source-bearing ZIP snapshot
Local v4 authority = cleaned metadata-only hub snapshot after exclusion/normalization/linkage rules
```

Because the local report also includes linkage data not present in the remote manifest, the local result should be treated as the stronger current local operational authority for implementation, while the remote manifest remains a source snapshot audit record.

## 5. Development Decision

Use the following authority split until local artifacts are pushed and verified remotely:

```text
For source ZIP audit:
  use seqcard_snapshot_v4_manifest.json

For local implementation planning:
  use local reported v4 cleaned values:
    seqcard_records = 37,166
    linkage_v4 exact_episode = 456
    linkage_v4 unmatched = 120
    schema_registry = 2.1-stage243-v4
```

Do not update the remote v4 manifest to 37,166 unless the local result packet or cleaned manifest is also loaded into remote GitHub.

## 6. Required Next Step

If remote GitHub authority should match the local hub, the next step is:

```text
1. Load or push the local files:
   - local_latest_hub_content_check_20260703.json
   - local_latest_hub_content_check_20260703.md
   - cleaned SeqCard v4 manifest / linkage_v4 / schema_registry 2.1-stage243-v4

2. ChatGPT verifies the files remotely by fetching them from GitHub.

3. Create or update a remote cleaned-snapshot manifest:
   - seqcard_snapshot_v4_cleaned_manifest.json
   - seqcard_corpus_linkage_v4.json
   - schema_registry_2_1_stage243_v4_reference.json or updated schema_registry.json
```

## 7. Safety State

The following remain blocked or false:

```text
raw_text_exported: false
raw_vectors_exported: false
token_exported: false
adapter_weight_exported: false
provider_call_count: 0
runtime_generation: false
promotion_claim: false
Macro Planner Promotion: blocked
Full Author Promotion: blocked
Live Generation Readiness: blocked
```

## 8. Final Decision

The local report is accepted as a verified local authority report.

The remote GitHub authority does not yet contain the local result packet or cleaned v4 linkage artifacts.

Final state:

```text
Local Hub Authority: verified yes
Remote GitHub Authority: partially verified for uploaded ZIP manifest, not verified for local cleaned v4 result packet
SeqCard v4 source snapshot: remote verified
SeqCard v4 cleaned operational snapshot: local verified, remote pending
Next required step: push/load cleaned local artifacts or proceed with ChatGPT direct design using the local values as reported
```
