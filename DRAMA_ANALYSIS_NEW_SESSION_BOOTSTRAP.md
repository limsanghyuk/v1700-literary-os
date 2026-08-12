# Drama Analysis — New Session Bootstrap

This file is the current human-readable entrypoint. Do not begin a new drama-analysis session from an old handoff document.

## Mandatory authority resolution

1. Read `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`.
2. Read `CURRENT_AUTHORITY_POINTER.json` and follow the authority it declares. Never hardcode V10 or V10.1 in session logic. The current pointer resolves to `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`.
3. Read `DRAMA_ANALYSIS_EXACT_SCHEMA_REGISTRY_V10_1.json` and the current authority mirror.
4. Read `DRAMA_ANALYSIS_CURRENT_OVERLAY_POINTERS_20260812.json` for the current CANONICAL THICK and Planner/Runtime authority IDs.
5. After selecting a work, read SourceLock plus its current work state/checkpoint before resuming.

## Semantic authoring invariant

The drama script itself is primary authority. Read the source directly and sequentially. One complete episode is the semantic authoring unit. Q1–Q4 and blocks of up to eight episodes are attention, checkpoint, and audit units only; they are not canonical acts and must not be used to semantically compress an episode.

Python may extract, normalize, lock, hash, serialize, validate, compare, and package. Python must not invent SceneCard, SequenceBlueprint, EpisodeArc, CharacterArc, RelationshipArc, edges, payoff meaning, THICK meaning, or other narrative semantics.

Per episode the canonical order is: SourceBoundaryReview → full source read → Stage01 SceneCard + EpisodeMeta → Stage02 SequenceBlueprint + EpisodeArc → Stage03 CharacterArc + RelationshipArc + LocalEdge + PayoffCandidate → Arc Coverage Expansion Pass → light gate → independent source audit → atomic checkpoint. Stage04 CrossEpisodeEdge + FullSeriesArc is promoted only after full-season Stage01–03 is complete and locked.

LocalEdge is same-episode only (`gap_episodes = 0`). Any cross-episode relation belongs to the Stage04 cross channel.

For existing PASS works, V10.1 uses risk-based selective reinforcement rather than mandatory full reanalysis. New semantic layers must be source-grounded and independently useful; do not paraphrase old text merely to game overlap metrics.

## Current overlay closure

- CANONICAL THICK: `DB98_THICK_12WORK_CANONICAL_AUTHORITY_20260812_V3`.
- Planner/Runtime V1.1: `DB98_PLANNER_RUNTIME_12WORK_CANONICAL_PROFILE_V1_1_AUTHORITY_20260812_V3`.
- Strict semantic-independence V3 repaired targets: `강남엄마따라잡기`, `가을동화`.
- 12-work exact/provenance/source validation: PASS, 1,795 THICK records, 27,123 SOURCE refs, 8,975 hash checks, errors 0.
- 12-work Planner/Runtime validation: PASS, 12,979 runtime scene records, errors 0.

Canonical repository: `limsanghyuk/v1700-literary-os`.
