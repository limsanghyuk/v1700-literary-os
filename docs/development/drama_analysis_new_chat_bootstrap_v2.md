# New-Chat Bootstrap — Start a New Drama Analysis Immediately

Use this document when a new conversation must begin analysis without relying on prior chat memory.

## 1. Read these files in order

```text
1. docs/external/claude_drama_analysis_method_manual_stage01_04_v1.md
2. docs/development/DRAMA_ANALYSIS_PROTOCOL_CURRENT.md
3. docs/development/drama_close_reading_continuous_analysis_protocol_v2.md
4. docs/contracts/drama_analysis_stage01_04_release_contract_v2.md
5. docs/runbooks/drama_analysis_failure_recovery_and_quality_gate_v2.md
```

For a continuing work, read its latest release manifest, audit, character-name registry, source-lock registry, and order ledger.

## 2. Immediate preflight

Without asking repeated questions when source files are already present:

1. list episodes and source files
2. detect encoding and scene markers
3. count ordinal scenes
4. create SourceLock v2
5. create canonical character-name registry
6. identify requested delivery span
7. split the first episode into Q1~Q4
8. set `next_allowed = EP01_Q1` or the manifest-defined resume point

Do not begin Stage04. Do not generate semantic records with Python.

## 3. Execution command

Use the following operational instruction:

```text
Analyze the drama by direct close reading under the current Stage01~04 protocol.
The user-facing delivery unit is two episodes, but each episode must be processed
Q1→Q2→Q3→Q4→episode integration, then the next episode, then a two-episode batch gate.
Read and author semantic records directly. Python may only support extraction, hashing,
validation, unchanged serialization, manifests, and packaging. Build Stage01 and partial
Stage02 inside each quarter. After the episode, build Stage03. Defer Stage04 until every
episode passes. Do not stop after a quarter and do not claim PASS without embedded evidence.
```

## 4. Required first-batch output

```text
source_lock/
character_registry/
authored_quarters/EP01_Q1~Q4
authored/EP01
authored_seq/EP01
stage3/EP01
validation/EP01
order_guard/EP01
then the same for EP02
batch_manifest_EP01_02.json
SHA256SUMS.txt
```

## 5. Progress messages

Progress messages may say what has actually been saved, but they are never authority.

Recommended:

```text
EP01 Q1 source-grounded records saved and quarter gate passed; continuing to Q2.
```

Prohibited before batch closure:

```text
EP01~EP02 complete
final PASS
canonical
```

## 6. Resume rule

If the conversation stops:

- inspect the manifest and actual files
- ignore unsupported progress claims
- resume only from `next_allowed`
- re-audit the last unsealed quarter

## 7. End-of-work rule

After the final episode:

1. inspect all PayoffCandidates
2. author the Stage04 promotion ledger and CrossEpisodeEdges
3. author FullSeriesArc
4. run structural and semantic audits
5. package unique checkpoints once
6. produce human and machine reports with the same decision
7. leave status as `PASS_CANDIDATE` until reviewer/user approval

## 8. Minimum first response in a new chat

The agent should report only verified preflight facts:

```text
source episode count
source encoding and scene-marker status
first two-episode delivery span
first episode quarter ranges
next_allowed state
```

It must then execute the analysis rather than repeatedly restating the method.
