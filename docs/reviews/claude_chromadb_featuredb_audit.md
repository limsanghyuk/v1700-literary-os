# Claude ChromaDB / FeatureDB Audit

## Current Audit Basis

This audit is based on the local `corpus_ko` workspace using metadata-only inspection and repository-safe derived outputs.

## Confirmed Findings

- `features/*.json` is the most complete learning-ready feature surface currently available.
- `scenes/*.jsonl` and `chunks/*.jsonl` exist per work, but repository outputs must not preserve their raw `text` fields.
- `chroma/chroma.sqlite3` is readable only in immutable mode and exposes minimal migration metadata in the current local state.
- `scene_features.db` exists but is currently empty in the inspected local state.
- `manifest.json`, `sources.json`, `qc_report.json`, and `nkg_summary.json` remain useful authority-side metadata sources.

## Operational Interpretation

```text
Feature authority: features/*.json
Scene/chunk structure authority: scenes/*.jsonl and chunks/*.jsonl for counts and IDs only
Vector retrieval authority: external Chroma artifacts, metadata-only in repo
Canonical authority in repo: generated metadata registries
```

## Recommended V1700 Handling

- trust neither ChromaDB nor FeatureDB blindly
- do not discard them
- absorb them into a canonical metadata layer
- keep verbatim text and vectors out of the hub
- treat RAG as advisory retrieval, not canonical truth
