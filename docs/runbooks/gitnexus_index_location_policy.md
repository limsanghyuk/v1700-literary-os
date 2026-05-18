# GitNexus Index Location Policy

## Decision

The GitNexus index folder should be located under the GPT workspace:

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index
```

It should not be kept directly under:

```text
C:\AI_Codex\codex-work\gitnexus_index
```

## Reason

`C:\AI_Codex\codex-work` is a multi-model workspace. It contains GPT, Gemini, Claude, and shared Codex infrastructure. A GitNexus index created for GPT/V1700 is not global infrastructure; it is generated state tied to the GPT repository.

Therefore the correct ownership boundary is:

```text
gpt owns gpt/gitnexus_index
gemini should own gemini/gitnexus_index if needed later
claude should own claude/gitnexus_index if needed later
```

## Current Registered Index

```text
Alias: v1700_stage72_3_ascii
Path:  C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_3_ascii
```

Current stats:

```text
160 files
1179 symbols
1841 edges
15 clusters
45 flows
```

The older `v1700-stage72-1-gpt` index remains registered as historical Stage72.1 evidence.
