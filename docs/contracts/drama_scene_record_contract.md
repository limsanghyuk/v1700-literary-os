# Drama Scene Record Contract

## Purpose

Describe the minimum repository-safe scene abstraction used by V1700 without storing verbatim scene text.

## Required Fields

```json
{
  "scene_id": "string",
  "work_id": "string",
  "scene_no": 0,
  "parse_method": "string",
  "summary": "optional short summary",
  "character_refs": ["string"],
  "location_hint": "optional",
  "conflict_hint": "optional",
  "rights_safe_excerpt_policy": "metadata_only"
}
```

## Policy

- If a source scene file contains `text`, that field must be consumed for counting or feature extraction only.
- Repository outputs may retain counts, IDs, methods, and derived metrics, but not raw scene bodies.
