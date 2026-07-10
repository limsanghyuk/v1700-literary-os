# Canonical Record Store Contract

## Purpose

Define the V1700 authority layer for externally acquired script corpora without committing verbatim copyrighted text into the repository.

## Authority Rules

- Canonical Record Store is the metadata and derived-signal authority.
- ChromaDB or any vector index is retrieval infrastructure, not story authority.
- Raw scripts, full scenes, dialogue dumps, and raw vectors must stay outside the hub repository.
- Repository-safe outputs must remain `metadata_only`.

## Required Record Families

```text
source_asset_inventory
canonical_work_registry
rag_index_registry
learning_signal_registry
audit_summary
```

## Required Safety Fields

```text
rights_status
access_policy
processing_status
verbatim_text_exported
raw_vectors_exported
```

## Promotion Rule

A corpus can be marked ready for V1700 RAG and learning integration only when:

- source assets are inventoried
- work-level metadata exists
- feature-derived learning signals exist
- retrieval readiness is recorded
- verbatim text export remains false

## Non-Goals

- storing screenplay text in git
- treating ChromaDB as canonical truth
- automatic model-weight updates
- hidden corpus mutation without audit
