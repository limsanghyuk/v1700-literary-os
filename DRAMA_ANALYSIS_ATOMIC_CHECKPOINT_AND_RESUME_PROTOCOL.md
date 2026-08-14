# Drama Analysis — Atomic Checkpoint & Resume Protocol V2

This protocol is part of the current new-session execution guidance. It does not replace Stage01–04 authority. Resolve `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json` and `CURRENT_AUTHORITY_POINTER.json` first.

## Purpose

Long direct-reading and THICK authoring must remain resumable after response interruption, tool timeout, context growth, session termination, or a late process. The safety mechanism is **sequence-level atomic durability inside a block of at most 8 contiguous episodes**, not an arbitrary sequence-count cap.

## Atomic state machine

For THICK/new semantic overlay work, one sequence is one atomic transaction:

`PENDING → SOURCE_READ → SEMANTIC_AUTHORED → FILE_SAVED → AUDIT_PASS → CHECKPOINT_LOCKED`

Only `CHECKPOINT_LOCKED` is completion. Chat prose or source reading alone is never progress.

## Mandatory reconciliation

Before new semantic authoring:
1. confirm there is no active competing writer;
2. recompute the contiguous valid prefix from semantic specs, atomic records, PASS audits, and checkpoints;
3. verify exact SequenceBlueprint member scenes and active source/provenance hashes;
4. rebuild a completed episode JSONL if its atomic records are complete but assembly is missing;
5. continue only from recomputed `next_seq_id`.

On-disk durable records outrank previous chat text.

## Single-writer invariant

Only one foreground process may write semantic specs, THICK records, audits, episode assemblies, or work_state for a work. Background continuation after the response boundary is forbidden. Late/overrun output goes to quarantine and is not accepted as progress.

## Durable write invariant

Use:

`write temp → flush → fsync → atomic rename → directory fsync`

Do not remove the previous valid checkpoint before its replacement is durable.

## Atomic commit command

The commit path receives model-authored meaning and performs:

`spec atomic write → schema/source checks → semantic-independence checks → THICK atomic write → audit atomic write → checkpoint atomic write`

Python may persist, hash, compare, validate, assemble, and package; it must not generate narrative meaning.

## Block execution model

- One execution block may contain at most **8 contiguous episodes**.
- There is **no fixed 3-sequence response cap**.
- Read and author sequences sequentially; do not load an entire multi-episode source block into one undifferentiated prompt dump.
- Keep individual source reads bounded to the current sequence/member-scene range or a small adjacent chunk.
- After each sequence, lock its atomic transaction before beginning the next.
- When an episode closes, rebuild its episode JSONL from atomic records and write an episode checkpoint.
- When the block closes, run a separate block strong gate and write durable PASS evidence.

If a response ends during a block, the next response reconciles and resumes from `next_seq_id`; already locked sequences are not repeated.

## Reconciliation promotion rule

Files ahead of work_state are neither discarded nor trusted automatically. A contiguous candidate may be accepted only when all of the following pass:
- semantic spec parses;
- THICK exact schema passes;
- independent audit says PASS;
- member scenes exactly match SequenceBlueprint;
- source / SceneCard / SequenceBlueprint / EpisodeArc / SourceLock hashes match;
- scene_notes cover all member scenes exactly;
- no sequence gap exists.

Unverified late writer output remains quarantine comparison evidence.

## Phase separation

Do not combine the entire pipeline into one mega-command. Durable phases are:

`THICK_BLOCK_AUTHORING → BLOCK_GATE → WHOLE_WORK_GATE → R5_BUILD → R8_BUILD → DB_INTEGRATION → CHECKSUM_BUILD → ZIP_BUILD → FRESH_EXTRACTION → HUB_PROMOTION`

Each phase requires durable PASS evidence before transition. A failure in a later phase resumes from that phase and does not invalidate earlier PASS phases.

Block authoring plus its block gate may occur in one assistant response if each sequence and episode is independently durable. Whole-work/R5/R8/integration/release are subsequent phases.

## Progress reporting

Distinguish `SOURCE_READ`, `SEMANTIC_AUTHORED`, `FILE_SAVED`, `AUDIT_PASS`, and `CHECKPOINT_LOCKED`. Do not report semantic completion before checkpoint lock.

For Stage01–04, the complete episode remains the semantic authoring unit under authority. This protocol is an interruption-safety mechanism for THICK/overlay persistence, not a redefinition of Stage01–04 semantics.
