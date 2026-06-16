# Canonical Record Store Contract

Status: LIGHTWEIGHT_CONTRACT
Created: 2026-06-16
Scope: minimum authoritative record contract for V1700 data ingestion, Writer IDE, Safe/Protected RAG, and formula signal linkage.

## 1. Purpose

Define the minimum canonical record families required before ingesting local DB survey outputs, drama script metadata, FeatureDB candidates, or ChromaDB candidates.

Canonical Record Store is the source of truth. Vector indexes, ChromaDB, and FeatureDB outputs are auxiliary indexes or derived evidence, not authority.

## 2. Non-goals

```text
no raw drama script upload
no full scene text storage
no dialogue text storage
no provider generation
no memory write
no canon mutation by assistant
no active coefficient update
no Page18 runtime opening
no Stage243+ creation
```

## 3. Record families

### WorkRecord

Represents a drama, film, or script work as a metadata-only unit.

Required fields:

```text
record_id
record_type
work_title
work_category
source_inventory_refs
rights_status
processing_status
created_at
updated_at
```

### SourceFileRecord

Represents a local file or archive member without storing copyrighted text.

Required fields:

```text
record_id
record_type
source_name
source_path_ref
extension
size_bytes
sha256
source_risk_class
rights_status
processing_status
```

### SceneRecord

Represents a safe scene-level abstraction.

Required fields:

```text
record_id
record_type
work_record_id
source_file_record_id
scene_order
safe_summary
character_refs
location_hint
narrative_function_tags
rights_status
text_storage_policy
```

Rules:

```text
safe_summary must not contain long copyrighted excerpts
text_storage_policy must be NO_FULL_TEXT
```

### CharacterRecord

Represents a character as a canonical entity.

Required fields:

```text
record_id
record_type
work_record_id
character_name
alias_refs
role_hint
source_refs
processing_status
```

### FormulaSignalRecord

Represents a formula-readable signal derived from metadata, summaries, or approved features.

Required fields:

```text
record_id
record_type
formula_id
source_record_refs
signal_name
signal_value
confidence
evidence_refs
processing_status
```

### FeatureRecord

Represents a Claude FeatureDB or future V1700 feature as a derived non-authoritative value.

Required fields:

```text
record_id
record_type
feature_name
feature_value
feature_type
source_record_refs
feature_origin
feature_db_ref
confidence
processing_status
```

### EmbeddingIndexRecord

Represents ChromaDB or other vector index metadata.

Required fields:

```text
record_id
record_type
index_name
embedding_model
index_path_ref
linked_record_refs
collection_count
item_count
index_health
processing_status
```

Rules:

```text
embedding index is not source of authority
raw vectors are not required in hub
```

### HumanApprovalRecord

Represents approval, rejection, or quarantine decisions.

Required fields:

```text
record_id
record_type
approval_target_ref
approval_status
reviewer_role
reason
created_at
```

## 4. Rights and risk classes

Allowed values:

```text
RIGHTS_UNKNOWN
METADATA_ONLY_ALLOWED
LOCAL_ONLY_RESTRICTED
PUBLIC_DOMAIN_OR_LICENSED
DO_NOT_EXPORT_TEXT
QUARANTINED
```

## 5. Processing statuses

Allowed values:

```text
DISCOVERED
INVENTORIED
SCHEMA_READABLE
SCHEMA_UNREADABLE
DERIVED_METADATA_READY
VALIDATED
QUARANTINED
REJECTED
```

## 6. Boundary invariants

```text
raw copyrighted script text is never stored in hub
local DBs are inspected by metadata-only survey first
ChromaDB / FeatureDB must be audited before reuse
Canonical Record Store remains source of truth
SafeSurfaceRAG and ProtectedAuthorRAG remain separate
```

## 7. Acceptance criteria

```text
minimum_records.json exists
all records have record_id and record_type
all source files have sha256 and source_risk_class
all scene records use NO_FULL_TEXT
all embedding records are marked non-authoritative
rights_status exists on all source-bearing records
```

## 8. Next candidate

```text
fixtures/canonical_record_store/minimum_records.json
tools/canonical_record_store_validator.py
tests/test_canonical_record_store_validator.py
```
