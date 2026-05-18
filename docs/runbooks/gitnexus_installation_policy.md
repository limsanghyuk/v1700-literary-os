# GitNexus Installation Policy

## Decision

GitNexus should not be copied into this repository as source code.

GitNexus is an external developer tool and MCP/CLI sidecar. It should be installed on the developer machine and invoked against the GPT/V1700 repository or its generated index mirror.

## Installed Status: 2026-05-12

GitNexus has been installed and validated on this machine.

```text
Node.js:   v24.15.0
npm/npx:   11.12.1
GitNexus:  1.6.4
CLI:       C:\Users\User\AppData\Roaming\npm\gitnexus.cmd
```

Installation command:

```powershell
$env:GITNEXUS_SKIP_OPTIONAL_GRAMMARS = "1"
npm install -g gitnexus
gitnexus setup
```

`gitnexus setup` configured Codex MCP support and installed 7 Codex skills.

## Current GPT/V1700 GitNexus Index

The active GPT/V1700 repository is:

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

The generated GitNexus index mirror is:

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii
```

GitNexus registry alias:

```text
v1700_stage72_3_ascii
```

Successful current index:

```text
Stage72.3 values are regenerated during release validation.
```

## Location Rule

`gitnexus_index` belongs under:

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index
```

It should not remain directly under:

```text
C:\AI_Codex\codex-work\gitnexus_index
```

Reason: this index is generated state for the GPT/V1700 codebase. Keeping it under `gpt` preserves the model-family boundary between GPT, Gemini, Claude, and shared Codex infrastructure.

## Refresh Flow

```powershell
robocopy "C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator" `
  "C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii" `
  /MIR /XD __pycache__ .pytest_cache .mypy_cache .ruff_cache node_modules .git .gitnexus .venv venv `
  /XF *.pyc *.pyo

gitnexus analyze "C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii" `
  --force --skip-git
```

Query examples:

```powershell
gitnexus query -r v1700_stage72_3_ascii Node2ProseCompiler
gitnexus impact -r v1700_stage72_3_ascii --include-tests Node2ProseCompiler
```
