# Stage73 Filename Migration Note

Generated at: 2026-05-12T08:39:11.547343+00:00

## Canonical artifact names

The canonical full-workspace integrated repository for this release is:

```text
V1700_stage73_full_workspace_integrated_repository.zip
V1700_stage73_full_workspace_integrated_repository.sha256.txt
V1700_stage73_full_workspace_integrated_repository_filelist.txt
```

## Historical aliases that must remain recognizable

The following names refer to earlier packaging attempts or intermediate releases and must be recognized during future development, audits, and lineage reconstruction:

```text
v1700_stage72_3.zip
gpt1700_stage72_3_foundation_lineage_governance_full_integrated_repository.zip
gpt_v1700_stage72_3_1_full_workspace_integrated_repository.zip
gpt_v1700_stage72_3_1_full_workspace_integrated_repository.sha256.txt
gpt_v1700_stage72_3_1_full_workspace_integrated_repository_filelist.txt
```

## Internal migration

```text
gpt/releases/v1700/stage72_3_1/
→ gpt/releases/v1700/stage73/

STAGE72_3_1_FULL_WORKSPACE_RELEASE_REPORT.md
→ STAGE73_FULL_WORKSPACE_RELEASE_REPORT.md

stage72_3_1_full_workspace_release_report.json
→ stage73_full_workspace_release_report.json

stage72_3_1_full_workspace_manifest.json
→ stage73_full_workspace_manifest.json
```

## Policy

Future development should treat **Stage73** as the canonical release label.  
Previous Stage72.3 and Stage72.3.1 names are not discarded; they are retained as lineage aliases so the system, developer, and AI agent can reconstruct how Stage73 emerged from the Stage72.3 packaging/evidence-dependency correction.

