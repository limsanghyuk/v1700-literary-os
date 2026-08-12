# DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1 — Hub Mirror

This is the GitHub bootstrap mirror of the packaged V10.1 authority. It is not a competing authority. `CURRENT_AUTHORITY_POINTER.json` decides which authority is active; historical V10/provider manuals do not override the active pointer.

## 1. Primary authority and authorship

The original drama script is primary authority. Semantic records must be produced by direct reading of the source. Existing analysis may be used for location, boundary, provenance, comparison, and audit, but must not silently substitute for new source reading when new meaning is authored.

Python is permitted for source extraction/normalization, SourceLock, canonical ordinal processing, hashes, JSON/JSONL serialization, schema/coverage/reference checks, duplicate-pattern detection, manifests, validation, and packaging. Python must not generate narrative meaning for SceneCard, SequenceBlueprint, EpisodeArc, CharacterArc, RelationshipArc, LocalEdge, PayoffCandidate, CrossEpisodeEdge, FullSeriesArc, or THICK.

## 2. Semantic unit and reading order

One complete episode is the semantic authoring unit. Read each episode sequentially and completely before the episode is promoted. Q1→Q2→Q3→Q4 may be used as attention/checkpoint aids but are not canonical acts. Blocks of up to eight episodes are management and strong-audit units, not semantic compression units.

Canonical episode flow:

`SourceBoundaryReview → full source read → Stage01 SceneCard + EpisodeMeta → Stage02 SequenceBlueprint + EpisodeArc → Stage03 CharacterArc + RelationshipArc + LocalEdge + PayoffCandidate → Arc Coverage Expansion Pass → light self-check → independent source audit → atomic checkpoint`

Stage04 is performed only after full-season Stage01–03 is complete and locked:

`CrossEpisodeEdge + FullSeriesArc → Stage04 audit → promotion decision`.

## 3. Stage01–04 contracts

The exact current field registry is `DRAMA_ANALYSIS_EXACT_SCHEMA_REGISTRY_V10_1.json`.

- SceneCard: 9 keys.
- EpisodeMeta: 5 keys.
- SequenceBlueprint: 18 keys.
- EpisodeArc: 13 keys.
- CharacterArc: 8 keys.
- RelationshipArc: 9 keys.
- Local/Cross Edge: 12 keys.
- PayoffCandidate: 7 keys.
- FullSeriesArc: 17 keys.

`CORE_ENUM` remains the canonical 16-type taxonomy. `turn_class` is `RISE | FALL | REVEAL | STALL`. `value_shift` is structured `{from,to}`. `turning_point` must reference an actual sequence. Recommended sequence density is approximately 0.12–0.17, with 0.11 as the lower operational bound.

## 4. Edge boundary

`LocalEdge` is same-episode only: `src_episode_no == tgt_episode_no`, `gap_episodes == 0`, causal. Adjacent-episode relations are still cross-episode and belong in the Stage04 cross channel. Do not store an EPn→EPn+1 bridge in LocalEdge.

## 5. V10.1 additions

V10.1 does not migrate the core Stage01–04 record shape. It adds three operating/evidence layers:

1. **Arc Coverage Expansion Pass** after initial CharacterArc/RelationshipArc authoring: inspect supporting characters and relationships for actual state changes before Stage04.
2. **Provider Selective Adoption Ledger**: external/provider analysis is candidate evidence; selectively adopt only source-supported improvements.
3. **Functional Holdout**: test whether a proposed layer improves retrieval/planning/function rather than merely adding text.

For existing PASS works, V10.1 does **not** require blanket full reanalysis. Use risk-based selective reinforcement when a concrete defect is demonstrated.

## 6. SourceLock, audits, lineage

SourceLock fixes source identity, canonical storage hashes, episode/scene boundaries, source anomalies, and excluded noncanonical files. Quarter/read checkpoints are evidence of reading progress, not substitutes for full-episode semantic understanding.

Authoring and independent audit must be separable. Failed or superseded work is preserved through lineage/quarantine rather than silently overwritten. Never claim a missing audit or direct-reading attestation retroactively.

A progress report must distinguish: source read, semantic authored, file saved, audit passed, checkpoint locked. Do not report a stage or episode as completed if its current file/checkpoint does not exist.

## 7. THICK / Planner / Runtime overlay boundary

Stage01–04 remain the base semantic authority. Current THICK and Planner/Runtime are overlays resolved separately from `DRAMA_ANALYSIS_CURRENT_OVERLAY_POINTERS_20260812.json`.

Current THICK V3 semantic-independence policy blocks Stage02-exact event reuse, Stage01/02-exact cast-function reuse, and generic cast templates. Duplicate cast functions are blocking for strict repaired/new V3 works. Source-verified factual inheritance is dispositioned; it is not paraphrased just to lower overlap metrics.

PlannerInput R5 is an N-episode planning-boundary packet built only from state available through N−1. Future/target material is holdout. Runtime R8 is deterministic projection from CANONICAL THICK plus same-episode R5; it is not an independent semantic-authoring layer.

## 8. New session invariant

Always start from `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`, then resolve `CURRENT_AUTHORITY_POINTER.json`. Never begin from a historical handoff or hardcode a version number. The current resolved authority is V10.1, but the resolution procedure is intentionally version-independent so that a later pointer update automatically becomes authoritative.
