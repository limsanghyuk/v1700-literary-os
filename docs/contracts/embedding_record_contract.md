# Embedding Record Contract

## Purpose

Describe repository-safe metadata for vector retrieval infrastructure.

## Required Fields

```json
{
  "work_id": "string",
  "scene_count": 0,
  "chunk_count": 0,
  "scene_index_ready": true,
  "chunk_index_ready": true,
  "vector_store_kind": "ChromaDB",
  "vector_binding_mode": "shared_corpus_index",
  "embedding_cache_available": true,
  "retrieval_policy": "metadata_authority_plus_external_vector_index",
  "text_policy": "verbatim_forbidden_in_repo_outputs"
}
```

## Policy

- embeddings are retrieval infrastructure only
- raw vectors are not committed
- any answer or promotion decision must route through canonical metadata and governance rules
