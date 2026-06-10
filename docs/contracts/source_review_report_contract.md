# Source Review Report Contract

Status: contract draft
Created: 2026-06-10
Scope: future source and rights review report for corpus fixtures
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the structure of a future source review report for V1700 corpus fixtures.

The report verifies that every fixture record has an allowed source class, rights status, and provenance reference.

## 2. Required report record

```text
SourceReviewReport
```

## 3. Required fields

```text
report_id
fixture_path
source_policy_ref
review_status
source_class_counts
rights_status_counts
quarantined_record_refs
restricted_record_refs
missing_provenance_refs
allowed_record_refs
blocking_failure_count
created_at
reviewer_role
```

## 4. Source classes

Allowed source classes:

```text
USER_PROVIDED_STRUCTURED_ANALYSIS_DB
USER_OWNED_SOURCE
PUBLIC_DOMAIN_SOURCE
LICENSED_SOURCE
METADATA_ONLY_ANALYSIS_RECORD
```

Blocked or quarantined source classes:

```text
RESTRICTED_COPYRIGHTED_FULL_TEXT
UNKNOWN_OR_UNRESOLVED_SOURCE
```

## 5. Required output sections

```text
1. Fixture path
2. Source policy reference
3. Source class distribution
4. Rights status distribution
5. Allowed records
6. Quarantined records
7. Restricted records
8. Missing provenance
9. Final source review decision
```

## 6. Review decision values

```text
SOURCE_REVIEW_NOT_RUN
SOURCE_REVIEW_PASS
SOURCE_REVIEW_PASS_WITH_WARNINGS
SOURCE_REVIEW_FAIL
SOURCE_REVIEW_BLOCKED
```

## 7. Blocking failures

- source_policy_ref missing
- any record missing source_class
- any record missing rights_status
- any record missing provenance_ref
- restricted full text used without explicit approval
- unknown source used outside quarantine
- source class contradicted by payload type

## 8. Relation to Page18 Option B

A Page18 Option B corpus adapter scaffold must not consume a fixture unless SourceReviewReport is at least:

```text
SOURCE_REVIEW_PASS_WITH_WARNINGS
```

Warnings must be preserved.

## 9. Final decision

Source review is mandatory before any corpus fixture is used by formula mapping, Value Proof, LearnableCritic, Writer IDE, or multi-agent supervision.
