# Local Codex Execution Handoff

Status: EXECUTION_HANDOFF
Created: 2026-06-13
Audience: local Codex / developer runtime

## 1. Objective

Inspect the developer's local DB workspace and generate metadata-only outputs that can be safely uploaded for assistant analysis.

## 2. Why this is needed

The assistant cannot directly access local Windows paths. Local Codex or the developer must execute the survey script on the local machine.

## 3. Preflight

From the repository root, confirm:

```powershell
python --version
python tools/local_db_inventory.py --help
```

## 4. Execution command

Run this from the repository root, replacing `<LOCAL_WORKSPACE_PATH>` with the local DB workspace path:

```powershell
python tools/local_db_inventory.py --root "<LOCAL_WORKSPACE_PATH>" --out ".local_db_survey"
```

For the current user-requested local target, use the path provided by the user in the local shell command. Keep it out of public commits unless required.

## 5. Expected outputs

```text
.local_db_survey/local_db_inventory_summary.json
.local_db_survey/local_db_file_inventory.csv
.local_db_survey/local_sqlite_schema_summary.json
.local_db_survey/local_db_survey_report.md
```

## 6. Optional packaging command

```powershell
Compress-Archive -Path .local_db_survey\* -DestinationPath local_db_survey_outputs.zip -Force
```

## 7. Upload back to assistant

Upload:

```text
local_db_survey_outputs.zip
```

or upload the four generated survey files individually.

## 8. Safety rules

Do not upload raw databases or raw script files until the assistant has reviewed the metadata-only survey.

Do not include:

```text
full scripts
scene text
dialogue text
long copyrighted excerpts
raw vector dumps
API keys
private credentials
```

## 9. What Codex should not do

```text
Do not rebuild ChromaDB yet.
Do not modify source DB files.
Do not delete local DB artifacts.
Do not normalize copyrighted text into repository files.
Do not push raw corpus files to GitHub.
```

## 10. What Codex may do

```text
Run metadata inventory.
Read SQLite schemas in read-only mode.
Hash files.
Count rows and tables.
Record extension distributions.
Mark text-bearing files as source-risk.
Package safe survey outputs.
```

## 11. Follow-up after assistant review

The assistant will use the uploaded survey outputs to create:

```text
docs/reviews/claude_chromadb_featuredb_audit.md
docs/contracts/drama_script_metadata_record_contract.md
docs/contracts/script_feature_record_contract.md
docs/architecture/script_corpus_to_v1700_data_pipeline.md
fixtures/research/chromadb_featuredb_audit_summary.json
```
