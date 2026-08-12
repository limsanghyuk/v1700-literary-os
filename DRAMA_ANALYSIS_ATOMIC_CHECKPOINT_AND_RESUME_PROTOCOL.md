# Drama Analysis — Atomic Checkpoint & Resume Protocol

This protocol is part of the current new-session execution guidance. It does not replace Stage01–04 authority. Resolve `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json` and `CURRENT_AUTHORITY_POINTER.json` first.

## Purpose

Long direct-reading and THICK authoring sessions must remain resumable after response interruption, tool timeout, context growth, session termination, or a previous tool process finishing slightly after the assistant response stops.

## Atomic state machine

For THICK/new semantic overlay work, one sequence is one atomic transaction:

`PENDING → SOURCE_READ → SEMANTIC_AUTHORED → FILE_SAVED → AUDIT_PASS → CHECKPOINT_LOCKED`

Only `CHECKPOINT_LOCKED` is completion. If a session stops earlier, never infer completion from chat prose alone.

## Mandatory turn-start reconciliation

Before any new semantic authoring:

1. Check whether another writer process is active.
2. Recompute state from durable semantic specs, atomic THICK records, audits, and the checkpoint.
3. If a complete semantic spec exists without a locked record, validate and commit that pending spec before authoring anything new.
4. Reassemble a completed episode file if all atomic sequence records exist but the episode file is missing.
5. Continue only from the recomputed `next` sequence.

The on-disk records are stronger evidence than the previous chat message.

## Single-writer invariant

Only one process may write semantic specs, THICK records, audits, episode assemblies, or work_state for a work at a time. Use an OS/file lock that is automatically released when the process exits. If the writer lock is busy, the new process must stop with a distinct `WRITER_BUSY` status and must not write concurrently.

This prevents a new session/turn from racing an older tool process that is still completing its final transaction.

## Durable write invariant

Write semantic specs, audits, THICK records, episode assemblies, and checkpoints by:

`write temp → flush → fsync → atomic rename → directory fsync`

Do not delete the previous valid checkpoint before the replacement is durable.

## Atomic commit command

For newly authored THICK semantics, prefer one commit process that receives the model-authored JSON and performs:

`spec atomic write → schema/source checks → semantic-independence gate → THICK record atomic write → audit atomic write → episode assemble if closed → checkpoint atomic write`

Python may persist and validate the model-authored meaning but must not generate that meaning.

## Context and response budget

For THICK/new overlay authoring, use conservative micro-batches:

- Maximum 3 newly authored sequences per assistant response.
- Maximum about 8,000 source characters per individual tool output.
- Soft ceiling about 30,000 source characters across one assistant response.
- Never print a multi-sequence full-source packet.
- Never load an 8-episode source block into one model context.
- Do not dump a full episode packet by default; read only the current sequence member-scene ranges, in chunks if needed.
- Keep semantic authoring, R5/R8 regeneration, full-database validation, and packaging in separate phases.

The assistant should intentionally end the response at a durable micro-batch checkpoint instead of continuing until the platform forcibly interrupts the turn.

## Progress reporting

Distinguish `SOURCE_READ`, `SEMANTIC_AUTHORED`, `FILE_SAVED`, `AUDIT_PASS`, and `CHECKPOINT_LOCKED`. Do not tell the user an episode or sequence is complete until its current checkpoint is locked on disk.

If a response ends unexpectedly, the next response starts with reconciliation and reports the durable state rather than repeating already locked work.

For Stage01–04, the full episode remains the semantic authoring unit under the active authority. This sequence-level atomic/micro-batch protocol is an interruption-safety mechanism for THICK/overlay authoring and checkpoint persistence, not a redefinition of canonical episode semantics.
