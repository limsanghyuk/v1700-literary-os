# English Path GitNexus Validation

## Verdict

Replacing the Korean model-family folder with the English `gpt` folder resolves the GitNexus direct analysis failure.

## Current Active Path

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

## Current GitNexus Index Path

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii
```

## Result

Direct GitNexus analysis under the English GPT path passed.

Current registered GitNexus alias:

```text
v1700_stage72_3_ascii
```

Current index:

```text
160 files
1179 symbols
1841 edges
15 clusters
45 flows
```

The active path also passed:

```text
python tools/run_stage72_2_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```

Pytest result:

```text
20 passed
```

## Recommendation

For GitHub, GitNexus, MCP tooling, CI, and cross-platform automation, use:

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

The GitNexus index should remain under:

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index
```

It should not live directly under `C:\AI_Codex\codex-work`.
