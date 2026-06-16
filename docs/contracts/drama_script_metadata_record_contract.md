# Drama Script Metadata Record Contract

## Scope

Metadata-only work record for a drama or film script asset set.

## Required Fields

```json
{
  "work_id": "string",
  "work_title": "string",
  "source_media": "film|drama|unknown",
  "source_type": "string",
  "source_reference": "string",
  "has_txt": true,
  "has_scenes": true,
  "has_chunks": true,
  "has_features": true,
  "scene_count": 0,
  "chunk_count": 0,
  "feature_scene_count": 0,
  "parse_methods": {
    "slug": 0
  },
  "qc_flags": ["OK"],
  "rights_status": "user_provided_structured_analysis_db",
  "access_policy": "metadata_only",
  "processing_status": "ready_for_canonical_store"
}
```

## Forbidden Fields

```text
full_text
scene_text
dialogue_text
raw_excerpt
embedding_vector
```
