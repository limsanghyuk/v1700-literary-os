# Corpus Adapter Mapping Table Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: future corpus adapter field mapping table, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines the structure of a future corpus adapter mapping table.

The table explains how source fields from approved structured analysis records map to V1700 corpus fixture records.

## 2. Future path

```text
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/corpus_adapter_mapping/mapping_table.md
```

## 3. Required table columns

```text
source_field_name
source_field_description
target_record_type
target_field_name
transformation_rule
required_or_optional
source_policy_requirement
validation_status
warning_note
```

## 4. JSON table shape

```json
{
  "mapping_table_id": "corpus_adapter_mapping_table_v0_1",
  "adapter_version": "0.1",
  "source_policy_ref": "docs/policies/narrative_corpus_source_policy.md",
  "schema_ref": "docs/architecture/narrative_corpus_schema_v0_1.md",
  "review_status": "DRAFT",
  "mappings": []
}
```

## 5. Mapping row example

```json
{
  "source_field_name": "Master_Theme",
  "source_field_description": "structured theme metadata from approved analysis source",
  "target_record_type": "CorePhilosophyRecord",
  "target_field_name": "master_theme",
  "transformation_rule": "copy_metadata_label",
  "required_or_optional": "required_if_present",
  "source_policy_requirement": "metadata_only_or_user_provided_structured_analysis",
  "validation_status": "MAPPING_DRAFT",
  "warning_note": "must not include full expressive passage"
}
```

## 6. Recommended seed mappings

```text
Drama_Entry -> DramaEntryRecord
Master_Theme -> CorePhilosophyRecord.master_theme
Conflict_Axis -> CorePhilosophyRecord.conflict_axis
Character -> CharacterRecord
Key_Object -> KeyObjectRecord
Causality_Matrix -> CausalityMatrixRecord
Trigger -> CausalityMatrixRecord.trigger_summary
Resolution -> CausalityMatrixRecord.resolution_summary
Residue -> CausalityMatrixRecord.residue_summary
Dialogue_Tone -> DialogueFunctionRecord.dialogue_tone
Critic_Thresholds -> CriticThresholdRecord
Scene_Blueprint -> SceneBlueprintRecord
Style_Module -> StyleModuleRecord
```

## 7. Transformation rules

Allowed initial rules:

```text
copy_metadata_label
normalize_identifier
summarize_user_provided_metadata
split_list_field
map_enum_label
link_record_reference
reject_unmapped_field
quarantine_source_field
```

## 8. Validation statuses

```text
MAPPING_DRAFT
MAPPING_VALIDATED
MAPPING_VALIDATED_WITH_WARNINGS
MAPPING_REJECTED
MAPPING_BLOCKED
```

## 9. Blocking failures

- source field maps to no target
- target record type not in schema
- transformation rule missing
- source policy requirement missing
- field mapping drops provenance
- mapping allows restricted full text into fixture

## 10. Final decision

Corpus adapter mapping table must exist before a future adapter scaffold can produce accepted corpus fixture records.
