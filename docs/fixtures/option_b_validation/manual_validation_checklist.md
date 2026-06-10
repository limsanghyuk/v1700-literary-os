# Option B Manual Validation Checklist

Status: checklist draft
Created: 2026-06-10
Scope: manual validation checklist for Page18 Option B fixture bundle
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This checklist allows a human reviewer to validate Option B fixtures before automated validator implementation exists.

It does not claim PASS. It provides a review procedure.

## 2. Fixture bundle

```text
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. JSON parse checklist

```text
[ ] mapping_table.json parses
[ ] narrative corpus fixture parses
[ ] formula catalog fixture parses
[ ] formula signal fixture parses
[ ] rejected records fixture parses
```

## 4. Source and rights checklist

```text
[ ] every accepted corpus record has source_class
[ ] every accepted corpus record has rights_status
[ ] every accepted corpus record has provenance_ref
[ ] every accepted corpus record is metadata-only
[ ] no unlicensed full text appears in accepted fixtures
[ ] restricted full text appears only as rejected/quarantined negative-path example
[ ] unknown source appears only as rejected/quarantined negative-path example
```

## 5. Corpus fixture checklist

```text
[ ] WorkRecord exists
[ ] DramaEntryRecord exists
[ ] CorePhilosophyRecord exists
[ ] at least two CharacterRecord entries exist
[ ] RelationshipGraphRecord exists
[ ] at least two SceneBlueprintRecord entries exist
[ ] at least two CausalityMatrixRecord entries exist
[ ] DialogueFunctionRecord exists
[ ] CriticThresholdRecord exists
[ ] scene records include conflict_type
[ ] scene records include emotional_start_tag and emotional_end_tag
[ ] causality records include trigger_summary, resolution_summary, residue_summary
```

## 6. Formula catalog checklist

```text
[ ] Narrative State Tensor formula exists
[ ] Emotional Momentum formula exists
[ ] Character Interaction Matrix formula exists
[ ] DRSE formula exists
[ ] Narrative Fitness Score formula exists
[ ] every formula has formula_id
[ ] every formula has formula_group
[ ] every formula has lineage_ref
[ ] every formula has input_schema_refs
[ ] every formula has output_schema_refs
[ ] every formula has boundary_rule_refs
```

## 7. Formula signal checklist

```text
[ ] every signal has formula_signal_id
[ ] every signal has formula_id
[ ] every signal has source_record_ids
[ ] every signal references existing corpus records
[ ] every signal references existing formula records
[ ] every signal has signal_type_label
[ ] all signals are FIXTURE_SIGNAL or explicitly non-proof labels
[ ] no signal is treated as performance proof
[ ] Value Proof remains preregistration-required
[ ] LearnableCritic remains audit-required
```

## 8. Mapping table checklist

```text
[ ] every mapping row has source_field_name
[ ] every mapping row has target_record_type
[ ] every mapping row has target_field_name
[ ] every mapping row has transformation_rule
[ ] every mapping row has source_policy_requirement
[ ] no mapping row permits restricted full text into accepted fixture
```

## 9. Rejected records checklist

```text
[ ] missing source class example exists
[ ] missing rights status example exists
[ ] missing provenance example exists
[ ] unknown source example exists
[ ] restricted full text example exists
[ ] schema target not found example exists
[ ] required field missing example exists
[ ] unmappable field structure example exists
[ ] quarantine_required is true for unknown source
[ ] quarantine_required is true for restricted full text
[ ] rejected records are not referenced by formula signals
```

## 10. Manual decision fields

Reviewer should record:

```text
reviewer_role:
review_date:
manual_status:
warning_count:
blocking_failure_count:
notes:
```

Allowed manual status:

```text
NOT_REVIEWED
PASS
PASS_WITH_WARNINGS
FAIL
BLOCKED
```

## 11. Final rule

Manual validation may support planning, but automated validator result is still required before fixture bundle acceptance.
