# Codex Local Gumiho Segmentation Handoff

Date: 2026-07-10  
Status: local metadata-only segmentation preflight complete; Stage01 blocked pending approved segmentation ledger  
Scope: `내여자친구는구미호` / Korean drama 04 / SeqCard Stage01 readiness

## 0. Purpose

Codex locally inspected the Korean drama source package for `내여자친구는구미호`, extracted HWP text locally, and prepared a safe segmentation review path without exporting raw drama text to the hub.

This handoff lets ChatGPT understand the local result and continue design work without needing the raw script, HWP files, ZIP, token arrays, embeddings, or generated prose.

## 1. Local Source

```text
source_zip: C:\AI_Codex\codex-work\gpt\db\Scripts\한국드라마04\내여자친구는구미호.zip
zip_sha256: 661ae78b05daa9dfa6e2ae3e5e490d811d133da7b9e99311c3988e1ba19feca1
episode_count: 16
hwp_integrity: pass
raw_text_exported_to_hub: false
```

The extracted local text exists only under the local SeqCard workspace and is not included in this hub handoff.

## 2. Local Work Performed

```text
1. HWP source extraction and source lock
2. Analysis preflight
3. Candidate-only scene segmentation
4. Segmentation review queue generation
5. Approved segmentation ledger template generation
6. Approved segmentation ledger validator/applicator creation
7. Blank template validation
```

## 3. Local Tools Added

```text
C:\AI_Codex\codex-work\gpt\tools\extract_gumiho_hwp_sources.py
C:\AI_Codex\codex-work\gpt\tools\build_gumiho_segmentation_candidates.py
C:\AI_Codex\codex-work\gpt\tools\build_gumiho_segmentation_review_queue.py
C:\AI_Codex\codex-work\gpt\tools\prepare_gumiho_segmentation_approval_template.py
C:\AI_Codex\codex-work\gpt\tools\validate_apply_gumiho_segmentation_ledger.py
```

These tools are local execution helpers. They are not evidence of Stage01 completion.

## 4. Hub-Loaded Metadata-Only Results

```text
release/current/data_foundry_pack/gumiho_segmentation_candidate_validation_20260710.json
release/current/data_foundry_pack/gumiho_segmentation_review_queue_validation_20260710.json
release/current/data_foundry_pack/gumiho_approved_segmentation_ledger_template_summary_20260710.json
release/current/data_foundry_pack/gumiho_approved_segmentation_ledger_validation_20260710.json
```

## 5. Key Validation Result

```text
candidate_segments: 252
review_queue_items: 252
approved_ledger_rows: 252
pending_rows: 252
error_count: 0
warning_count: 252
raw_text_exported: false
provider_call_count: 0
runtime_generation: false
canonical_stage01_allowed: false
```

## 6. Gate Decision

```text
Stage01 SceneCard: blocked
Reason: no approved scene boundary ledger exists yet
```

Codex must not assign canonical `scene_no` from candidate segments automatically. The candidate segmentation exists only to support review. A human or authorized local review process must approve, merge, split, reject, or reopen each candidate before canonical Stage01 work begins.

## 7. Next Required Step

Create a completed approved segmentation ledger from the local template:

```text
C:\AI_Codex\codex-work\gpt\db\seqcard_ko\segmentation_review\내여자친구는구미호_approved_segmentation_ledger_template_20260710.csv
```

Then run:

```text
python C:\AI_Codex\codex-work\gpt\tools\validate_apply_gumiho_segmentation_ledger.py --ledger <completed-ledger.csv-or-jsonl>
```

If validation passes, Codex will create:

```text
C:\AI_Codex\codex-work\gpt\db\seqcard_ko\segmentation_review\내여자친구는구미호_canonical_segmentation_ledger_20260710.jsonl
```

Only then may Stage01 SceneCard generation begin.

## 8. Boundary

Do not perform:

```text
raw dialogue export
raw scene/chunk text export
embedding/vector export
provider call
runtime generation
training update
promotion claim
automatic Stage01 promotion
Stage02/03/04 derivation from pending segments
```

## 9. ChatGPT Project Use

ChatGPT should use this handoff to understand:

```text
1. The local source is available and integrity-checked.
2. The work is pre-Stage01, not Stage01-complete.
3. The blocker is approved scene segmentation, not extraction failure.
4. The next design step is a review protocol or local reviewer workflow, not creative analysis.
```

