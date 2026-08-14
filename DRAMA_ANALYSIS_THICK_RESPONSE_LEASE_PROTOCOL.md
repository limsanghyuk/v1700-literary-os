# Drama Analysis — THICK Block-Atomic Execution Protocol V2

This protocol supplements `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md` and supersedes the temporary 3-sequence response cap introduced after the repeated `국희` interruption.

## Decision

The 3-sequence hard cap was an over-constrained mitigation. The actual failure mechanism was not sequence count itself; it was combining semantic authoring, later derivation, integration, packaging, and promotion into one long execution flow, plus allowing late writer output to appear after the response boundary.

The current execution boundary is therefore the developer-defined block: **up to 8 contiguous episodes**. There is no arbitrary per-response sequence-count cap inside that block, provided every sequence is committed atomically and the writer remains single-process and foreground-only.

## Atomic sequence transaction

Every new THICK sequence must complete this transaction before the next sequence begins:

`SOURCE_READ -> SEMANTIC_AUTHORED -> spec atomic write -> exact/source checks -> THICK record atomic write -> independent audit PASS -> checkpoint atomic write`

Only `CHECKPOINT_LOCKED` counts as progress. Source reading, chat prose, temporary files, or semantic drafts without a locked transaction do not advance `locked_sequences` or `next_seq_id`.

## Block guard

A block guard records:
- `work_id`
- `block_episode_start` / `block_episode_end`
- `max_block_episodes = 8`
- exact ordered `expected_seq_ids`
- `block_expected_sequences`
- `block_committed_sequences`
- whole-work `locked_sequences_total`
- `last_locked_seq_id` / `next_seq_id`
- current phase and durable block-gate evidence

The guard must reject:
- a sequence that is not the exact durable `next_seq_id`;
- a block spanning more than 8 episodes;
- non-contiguous episode blocks;
- a commit without parseable spec, THICK record, and PASS audit;
- block completion before all expected sequences are locked;
- phase transition without durable PASS evidence.

## Episode and block checkpoints

When all sequences for an episode are locked, rebuild that episode JSONL only from current atomic records and write an episode checkpoint. When all episodes in the block are closed, run the block strong gate. Only a PASS block gate may close the block.

If execution stops at any point, reconcile from the contiguous prefix of valid atomic records and resume from the computed `next_seq_id`. Completed earlier sequences and episodes are not repeated.

## No late/background writer

Semantic writers must not continue asynchronously after the assistant response ends. A late-finishing or overrun semantic file is not automatically progress. Preserve it in quarantine. It may be used as comparison evidence only after the relevant source is re-read and the sequence is revalidated and newly committed through the active block guard.

## Phase separation

The following are separate durable phases:

`THICK_BLOCK_AUTHORING -> BLOCK_GATE -> WHOLE_WORK_GATE -> R5_BUILD -> R8_BUILD -> DB_INTEGRATION -> CHECKSUM_BUILD -> ZIP_BUILD -> FRESH_EXTRACTION -> HUB_PROMOTION`

A phase may use multiple commands, but the next phase starts only after a durable PASS report exists. Do not place all phases in one mega-script or background process.

Block-level THICK authoring and its block gate may be completed in one assistant response when the context remains bounded, because every sequence and episode is independently durable. R5/R8, database promotion, and release packaging remain later phases.

## Progress authority

Durable disk/guard state outranks chat text. If they disagree, the contiguous atomic checkpoint state is authoritative.

See `DRAMA_ANALYSIS_REPEAT_INTERRUPTION_INCIDENT_20260814.md` for the incident and the correction history. `tools/drama_analysis_phase_guard.py` implements this V2 block-atomic policy.
