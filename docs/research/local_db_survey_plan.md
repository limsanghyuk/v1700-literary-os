# Local DB Survey Plan

Status: LOCAL_ACTION_PLAN
Created: 2026-06-13
Target: developer-provided local workspace path

## 1. Purpose

Survey local database assets that may contain Claude-built ChromaDB, FeatureDB, script metadata, or related indexing outputs, then produce metadata-only artifacts that can be safely inspected.

## 2. Boundary

The local path is not directly accessible from ChatGPT. The survey must be executed locally by the developer/user.

## 3. Do not export

```text
full drama scripts
full scene text
long dialogue excerpts
copyrighted source text
raw embedding vectors unless explicitly needed
private keys or credentials
```

## 4. Safe outputs

```text
file inventory: path, extension, size, sha256
sqlite schema: table names, column names, row counts
chroma metadata: collection/table/index counts if readable
feature DB schema: feature names, types, counts
sample records: metadata-only, no source text
health report: readable/corrupt/missing
```

## 5. Local script

Use:

```text
python tools/local_db_inventory.py --root <LOCAL_WORKSPACE_PATH> --out .local_db_survey
```

Expected outputs:

```text
.local_db_survey/local_db_inventory_summary.json
.local_db_survey/local_db_file_inventory.csv
.local_db_survey/local_sqlite_schema_summary.json
.local_db_survey/local_db_survey_report.md
```

## 6. Integration path

After local execution, upload only the generated `.local_db_survey` outputs, not the raw database or script text, unless a separate rights review approves it.

## 7. V1700 use

The safe outputs will inform:

```text
canonical_record_store_contract
script_feature_record_contract
chromadb_featuredb_audit
script_corpus_to_v1700_data_pipeline
safe_rag / protected_rag split
```
