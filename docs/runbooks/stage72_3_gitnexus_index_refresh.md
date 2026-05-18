# Stage72.3 GitNexus Index Refresh

Stage72.3 uses a stage-matched GitNexus alias:

```text
v1700_stage72_3_ascii
```

Index mirror:

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii
```

Refresh flow:

```powershell
robocopy "C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator" `
  "C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii" `
  /MIR /XD __pycache__ .pytest_cache .mypy_cache .ruff_cache node_modules .git .gitnexus .venv venv `
  /XF *.pyc *.pyo

gitnexus analyze "C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii" --force --skip-git
```

The old `v1700_stage72_2_ascii` index is historical and should not be used as the current Stage72.3 baseline.
