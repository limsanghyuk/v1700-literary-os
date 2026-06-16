# ChatGPT Project Corpus Data Handoff

## Intent

This document is for a new ChatGPT project session to understand exactly what was built locally and how to continue without re-reading the full conversation.

## What Exists Now

### Local corpus inspection

Safe survey outputs were produced from `C:\AI_Codex\codex-work\gpt\db`.

Important findings:

- `corpus_ko/features/*.json` is the usable feature surface
- `corpus_ko/scenes/*.jsonl` and `chunks/*.jsonl` are present but must remain local-only for raw text
- `corpus_ko/scene_features.db` is empty in the current local state
- `corpus_ko/chroma/chroma.sqlite3` is not a reliable canonical authority by itself

### Repository implementation

Added code:

```text
src/v1700/corpus_absorption/
src/v1700/corpus_formula_bridge/
tools/run_local_corpus_absorption.py
tools/run_local_corpus_formula_bridge.py
tests/test_local_corpus_absorption.py
tests/test_local_corpus_formula_bridge.py
```

Added docs:

```text
docs/contracts/canonical_record_store_contract.md
docs/contracts/drama_script_metadata_record_contract.md
docs/contracts/drama_scene_record_contract.md
docs/contracts/script_feature_record_contract.md
docs/contracts/embedding_record_contract.md
docs/architecture/script_corpus_to_v1700_data_pipeline.md
docs/architecture/corpus_formula_signal_bridge_blueprint.md
docs/reviews/claude_chromadb_featuredb_audit.md
docs/reviews/corpus_absorption_build_report.md
docs/development/current_session_handoff.md
```

### Generated hub-safe outputs

```text
release/current/corpus_ko_absorption_pack/
release/current/corpus_formula_bridge_pack/
fixtures/research/drama_script_metadata_inventory_summary.json
fixtures/research/chromadb_featuredb_audit_summary.json
fixtures/research/script_feature_record_sample.json
fixtures/canonical_record_store/minimum_records.json
```

## Current Numbers

From the current local run:

```text
work_count: 465
rag_ready_count: 455
learning_ready_count: 455
formula_signal_count: 1395
tensor_count: 465
```

## Operating Meaning

The project is no longer at “script archive exists” stage.

It now has:

```text
canonical metadata layer
RAG readiness layer
learning signal layer
formula bridge layer
```

## What The Next Chat Should Do

Do not rebuild raw corpus files into git.

Instead, continue from the generated packs and implement one of:

1. Formula Signal Store fixture and query surface
2. LearnableCritic audited intake from formula signals
3. Writer IDE advisory card renderer from formula signals
4. Value Proof Arm B preregistered formula guidance pack

## Hard Boundaries

Never push:

```text
full scripts
scene text
dialogue text
raw vectors
copyrighted long excerpts
```

Push only:

```text
metadata registries
feature aggregates
formula signals
tensor summaries
audit reports
contracts
architecture docs
```
