# Drive Corpus/Scripts Registry Report

Updated: 2026-06-19  
Branch: `corpus-absorption-formula-bridge-handoff`  
Status: `PASS_WITH_WARNINGS`

## Purpose

This report records a metadata-only Google Drive discovery pass for corpus/scripts candidates. It is intended for the web project and future local Codex runs so they can distinguish confirmed local corpus DB evidence from Drive-side archive or folder candidates.

No Drive file contents, corpus prose, script bodies, credentials, or protected attachment contents were downloaded or exported.

## Decision

```text
No confirmed raw corpus/scripts archive was found.
The safe current artifact is a Drive corpus/scripts registry seed.
The local corpus_ko generated packs remain the current evidence authority.
```

## Archive Search Result

The Drive search checked raw archive MIME candidates and extension-style name candidates:

```text
.zip
.tar
.gz
.7z
.rar
```

Result:

```text
raw archive MIME candidates: 0
.zip search: Google Docs sidecars only, such as .zip.sha256, .zip.filelist, .zip.sha256sums
.tar/.gz/.7z/.rar search: no confirmed raw archive candidates
```

Warning:

```text
A differently named archive may still exist outside the searched result window.
An exact Drive URL/title fragment or a full paginated Drive inventory would be required to prove absence.
```

## Golden Corpus Candidates

Two `golden_corpus` folders were found. Both currently show a `node2_rewrite` child folder, and both inspected `node2_rewrite` folders listed zero children.

```text
golden_corpus -> node2_rewrite: empty in inspected listing
golden_corpus -> node2_rewrite: empty in inspected listing
```

Related Google Docs named `V1650_STAGE25_8_GOLDEN_CORPUS_LONG_SEASON_REGRESSION.md` were also found, but only metadata was recorded.

## Scripts Candidates

Several folders named `scripts` were found. Inspected examples appear to be project-specific utility folders rather than corpus/script archive containers:

```text
zotero/scripts: zotero.py
brainstorming/scripts: frame-template, server.cjs, start-server.sh, helper.js, stop-server.sh
sentry/scripts: sentry_api.py
android-emulator-qa/scripts: ui_pick.py, ui_tree_summarize.py
```

Additional `scripts` folder IDs remain as top-search candidates in the machine-readable registry for later metadata-only inspection.

## Registry File

Machine-readable registry:

```text
release/current/drive_corpus_scripts_registry.json
```

The registry records:

```text
archive discovery result
golden_corpus candidate folders
scripts candidate folders
inspected child summaries
uninspected top-search scripts folder IDs
safety policy
hub integration decision
recommended next actions
```

## Authority Relationship

```text
Local corpus DB: current generated evidence source
Drive registry: discovery/planning evidence
Drive archive: not confirmed
Drive folder candidates: not promoted to corpus authority
```

Current local generated evidence remains:

```text
C:\AI_Codex\codex-work\gpt\db\corpus_ko
release/current/local_corpus_db_survey_report.json
release/current/corpus_ko_absorption_pack/corpus_absorption_report.json
release/current/corpus_formula_bridge_pack/corpus_formula_bridge_report.json
release/current/formula_signal_store_pack/formula_signal_store_report.json
```

## Next Actions

1. If the intended archive exists, provide the exact Drive URL or title fragment.
2. If no archive is required, continue treating the local `corpus_ko` packs as current evidence and this Drive registry as the Drive candidate map.
3. Before any Drive corpus content ingestion, create a metadata-only import plan and rights/safety review.

## Rule

```text
Web defines.
Local Codex proves.
Hub records.
Only recorded evidence promotes the next implementation step.
```
