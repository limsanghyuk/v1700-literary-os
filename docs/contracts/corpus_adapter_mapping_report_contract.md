# Corpus Adapter Mapping Report Contract

Status: contract draft
Created: 2026-06-10
Scope: future corpus adapter mapping report
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the mapping report emitted by a future metadata-only corpus ingestion adapter.

The mapping report explains how source fields were transformed into V1700 narrative corpus schema records.

## 2. Required report record

```text
CorpusAdapterMappingReport
```

## 3. Required fields

```text
report_id
source_bundle_ref
adapter_version
source_policy_ref
schema_ref
mapping_status
mapped_record_count
rejected_record_count
mapped_field_table_ref
rejected_records_report_ref
schema_validation_report_ref
source_review_report_ref
created_at
review_status
```

## 4. Mapping statuses

```text
NOT_RUN
MAPPING_DRAFT
MAPPING_PASS
MAPPING_PASS_WITH_WARNINGS
MAPPING_FAIL
MAPPING_BLOCKED
```

## 5. Required mapping table columns

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

## 6. Required report sections

```text
1. Source bundle summary
2. Source policy reference
3. Schema reference
4. Field mapping table
5. Record mapping summary
6. Rejected record summary
7. Warnings
8. Blocking failures
9. Downstream readiness
10. Final mapping status
```

## 7. Downstream readiness labels

```text
READY_FOR_SCHEMA_VALIDATION
READY_FOR_SOURCE_REVIEW
READY_FOR_FORMULA_SIGNAL_MAPPING
READY_FOR_VALUE_PROOF_FIXTURE
READY_FOR_LEARNABLE_CRITIC_FIXTURE
NOT_READY
```

## 8. Blocking failures

- source_policy_ref missing
- schema_ref missing
- mapped source field lacks target field
- target record type not in schema
- rejected record report missing when rejected_count > 0
- restricted full text mapped to corpus fixture
- provenance dropped during mapping
- mapping status pass despite blocking rejected records

## 9. Final decision

CorpusAdapterMappingReport is required before any adapter output can be accepted as a V1700 corpus fixture.
