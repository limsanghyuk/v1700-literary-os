# Drama Analysis — New Session Bootstrap

This file is the current human-readable entrypoint. Do not begin a new drama-analysis session from an old handoff document.

## Mandatory authority resolution

1. Read `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`.
2. Read `CURRENT_AUTHORITY_POINTER.json` and follow the authority it declares. Never hardcode V10 or V10.1 in session logic. The current pointer resolves to `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`.
3. Read `DRAMA_ANALYSIS_EXACT_SCHEMA_REGISTRY_V10_1.json` and the current authority mirror.
4. Read `DRAMA_ANALYSIS_CURRENT_OVERLAY_POINTERS_20260814_24WORK.json` for the current CANONICAL THICK and Planner/Runtime authority IDs.
5. Read `DRAMA_ANALYSIS_NEW_WORK_EXECUTION_RUNBOOK.md`, `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md`, and `DRAMA_ANALYSIS_INTEGRATION_RELEASE_RECOVERY_PROTOCOL.md` before starting/resuming long semantic or integration/release work.
6. After selecting a work, read SourceLock plus its current work state/checkpoint before resuming.

## Semantic authoring invariant

The drama script itself is primary authority. Read the source directly and sequentially. One complete episode is the semantic authoring unit. Q1–Q4 and blocks of up to eight episodes are attention, checkpoint, and audit units only; they are not canonical acts and must not be used to semantically compress an episode.

Python may extract, normalize, lock, hash, serialize, validate, compare, and package. Python must not invent SceneCard, SequenceBlueprint, EpisodeArc, CharacterArc, RelationshipArc, edges, payoff meaning, THICK meaning, or other narrative semantics.

Per episode the canonical order is: SourceBoundaryReview → full source read → Stage01 SceneCard + EpisodeMeta → Stage02 SequenceBlueprint + EpisodeArc → Stage03 CharacterArc + RelationshipArc + LocalEdge + PayoffCandidate → Arc Coverage Expansion Pass → light gate → independent source audit → atomic checkpoint. Stage04 CrossEpisodeEdge + FullSeriesArc is promoted only after full-season Stage01–03 is complete and locked.

LocalEdge is same-episode only (`gap_episodes = 0`). Any cross-episode relation belongs to the Stage04 cross channel.

For existing PASS works, V10.1 uses risk-based selective reinforcement rather than mandatory full reanalysis. New semantic layers must be source-grounded and independently useful; do not paraphrase old text merely to game overlap metrics.

## Interruption-safe execution invariant

For THICK/new semantic overlay authoring, use `1 sequence = 1 atomic transaction`:

`SOURCE_READ → SEMANTIC_AUTHORED → FILE_SAVED → AUDIT_PASS → CHECKPOINT_LOCKED`.

At the start of every response, reconcile durable disk state before trusting chat progress reports. Use a single-writer OS/file lock so a late-finishing prior process cannot overlap a new writer. Durable writes use temp → flush/fsync → atomic rename. Do not report an episode or sequence as complete before the checkpoint is locked on disk.

For whole-database integration/release, do not chain integration, promotion, validation, checksum, ZIP, fresh extraction, and postzip validation into one timeout budget. Each phase must leave a durable PASS report. If interrupted, inspect disk state and resume only the first incomplete phase.

## Current overlay closure

- Stage01–04: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`, 98 works / 1,814 episodes / 114,371 SceneCards.
- CANONICAL THICK: `DB98_THICK_24WORK_CANONICAL_AUTHORITY_20260814_V1_GRJB_INTEGRATED`.
- Planner/Runtime V1.1: `DB98_PLANNER_RUNTIME_24WORK_CANONICAL_PROFILE_V1_1_AUTHORITY_20260814_V1_GRJB_INTEGRATED`.
- 24-work strict semantic-independence V3: PASS, blocking errors 0, legacy diagnostic groups 0.
- 24-work exact/provenance/source validation: PASS, 3,573 THICK records, 62,905 SOURCE refs, 17,865 hash checks, errors 0.
- 24-work Planner/Runtime validation: PASS, 434 PlannerInput episode files, 434 Runtime episode files, 27,438 runtime scene records, errors 0.
- New work `그저바라보다가`: 16 episodes / 137 THICK records / 1,168 Runtime scene records; semantic, exact/provenance, Planner/Runtime all PASS.
- Quality homogenization for `그저바라보다가`: PASS; event 131.6, cast-function 58.7, info-shift 1.54/sequence, plant-payoff 1.54/sequence, all at or above the existing-15 Q25 floor.
- Non-target CLEAN V5 immutability: PASS; 26,494 predecessor files checked, missing 0, changed 0 before authority metadata promotion.
- Full database ZIP: `DB98_98WORK_STAGE04_24THICK_CLEAN_V6_GRJB_INTEGRATED_FINAL_20260814.zip`.
- Full database SHA256: `b25ba041d21ab6299e92ac52b7e45dc099708019af6dcc12b97f82aa7974a9cd`.
- Final fresh extraction: PASS; ZIP entries 26,559, checksum errors 0.

Canonical repository: `limsanghyuk/v1700-literary-os`.
