# Workspace Path Policy

## Active GPT/V1700 Repository

The active GPT/V1700 Stage72.1 canonical repository is:

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

## Rationale

`C:\AI_Codex\codex-work` is the global multi-line workspace. It contains model-family folders such as:

```text
C:\AI_Codex\codex-work\gpt
C:\AI_Codex\codex-work\gemini
C:\AI_Codex\codex-work\claude
```

GPT-line active runtime work must live under:

```text
C:\AI_Codex\codex-work\gpt\active
```

Release evidence and historical release snapshots must live under:

```text
C:\AI_Codex\codex-work\gpt\releases
```

The GitNexus generated index for GPT/V1700 must live under:

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index
```

This keeps GPT active runtime, release evidence, generated graph indexes, and historical ledgers inside the GPT model-family workspace instead of mixing them with Gemini, Claude, or global Codex tooling.

## Previous Locations

The Stage72 canonical repository previously moved through temporary construction paths:

```text
C:\AI_Codex\codex-work\v1700_stage72_canonical_repo
C:\AI_Codex\codex-work\gpt\archive\legacy_release_singular_20260512\v1700_stage72_canonical_repo
```

Those are no longer active execution roots.

## Current Rule

Future GPT/V1700 active development should happen under:

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

Release evidence should be copied to:

```text
C:\AI_Codex\codex-work\gpt\releases\v1700\stageXX
```

Packaged ZIP artifacts should be stored in:

```text
C:\AI_Codex\codex-work\gpt\packages
```

