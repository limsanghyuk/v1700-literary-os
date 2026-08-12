# Drama Analysis — Atomic Checkpoint & Resume Protocol

This protocol is part of the current new-session execution guidance. It does not replace Stage01–04 authority. Resolve `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json` and `CURRENT_AUTHORITY_POINTER.json` first.

## Purpose

Long direct-reading and THICK authoring sessions must remain resumable after response interruption, tool timeout, context growth, or session termination.

## Atomic state machine

For THICK/new semantic overlay work, one sequence is one atomic transaction:

`PENDING → SOURCE_READ → SEMANTIC_AUTHORED → FILE_SAVED → AUDIT_PASS → CHECKPOINT_LOCKED`

Only `CHECKPOINT_LOCKED` is completion. If a session stops earlier, resume from the last locked checkpoint. Never infer completion from chat prose alone.

## Required checkpoint fields

A checkpoint must record at minimum: work_id, resolved authority IDs/pointers, episode_no, seq_id, seq_index, status, output file path, record SHA256, source SHA256, schema/source/semantic gate results, next episode/sequence, and updated_at.

Write checkpoint to a temporary file first, fsync/close it, then atomically rename it into place. Do not delete the previous checkpoint before the new one is durable.

## Context and tool-call limits

- Do not dump an 8-episode block of source text into one model context.
- Do not dump a full episode packet by default.
- Read only the current sequence member-scene source ranges needed for authoring.
- Do not combine large source output, multi-episode semantic authoring, full-database validation, and ZIP packaging in one tool call.
- Keep semantic authoring, downstream R5/R8 regeneration, validation, and packaging as separate phases.
- Break long shell/Python work by work, episode, or validator type.

## Progress reporting

Distinguish `SOURCE_READ`, `SEMANTIC_AUTHORED`, `FILE_SAVED`, `AUDIT_PASS`, and `CHECKPOINT_LOCKED`. Do not tell the user an episode or sequence is complete until its current checkpoint is locked on disk.

For Stage01–04, the full episode remains the semantic authoring unit under the active authority; this sequence-level atomic protocol is an interruption-safety mechanism for THICK/overlay authoring and checkpoint persistence, not a redefinition of canonical episode semantics.
