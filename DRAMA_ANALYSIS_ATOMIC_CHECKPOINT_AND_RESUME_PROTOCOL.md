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

## Hard response-boundary enforcement

The 3-sequence response budget is a hard safety limit, not a recommendation. A user request to finish an entire block in one response does not override this interruption-safety limit. Complete the block across successive durable micro-batches.

A semantic writer must not continue producing new sequences after the assistant response has ended. Background or late-finishing continuation is forbidden. A process that was launched in the current response may finish only the already-started atomic sequence transaction; it must not advance to another sequence automatically.

Every response that authors THICK must end in this order:

`finish current atomic transaction → fsync checkpoint → release writer lock → report durable next_seq_id → stop`

The next assistant response must reacquire the writer lock and run reconciliation before reading or authoring the next sequence.

## Reconciliation promotion rule

If interruption leaves semantic specs, atomic records, or audits ahead of `work_state`, do not discard them and do not trust them automatically. Reconciliation may promote only a contiguous prefix of sequence records for which all of the following independently pass:

- semantic spec exists and parses
- THICK record has exact schema
- independent audit exists and says PASS
- SequenceBlueprint member scenes match exactly
- source / SceneCard / SequenceBlueprint / EpisodeArc / SourceLock hashes match the active baseline
- scene_notes cover all member scenes exactly
- no sequence gap exists before the candidate record

After promotion, reassemble any completed episode file and atomically rewrite `work_state`. The recomputed durable `next_seq_id` is the only valid resume point.

## Long-task phase separation

Do not combine semantic authoring, episode assembly, whole-block strong validation, PlannerInput/R8 generation, database promotion, checksums, ZIP creation, or fresh-extraction validation into one long command. Each phase must produce a durable PASS report before the next phase begins. If a later phase times out, resume from the first phase without a durable PASS report rather than rerunning earlier completed phases.

## Progress reporting

Distinguish `SOURCE_READ`, `SEMANTIC_AUTHORED`, `FILE_SAVED`, `AUDIT_PASS`, and `CHECKPOINT_LOCKED`. Do not tell the user an episode or sequence is complete until its current checkpoint is locked on disk.

If a response ends unexpectedly, the next response starts with reconciliation and reports the durable state rather than repeating already locked work.

For Stage01–04, the full episode remains the semantic authoring unit under the active authority. This sequence-level atomic/micro-batch protocol is an interruption-safety mechanism for THICK/overlay authoring and checkpoint persistence, not a redefinition of canonical episode semantics.
