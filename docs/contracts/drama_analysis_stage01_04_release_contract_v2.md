# Drama Analysis Stage01~04 Release Contract v2

Status: candidate contract

## Release object

A drama-analysis release is valid only when all required records, evidence, and decisions agree.

## Required top-level content

```text
authored/                 Stage01 SceneCards + episode metadata
authored_seq/             Stage02 SequenceBlueprints
authored_arc/             EpisodeArc + FullSeriesArc
authored_chararc/         per-episode CharacterArc
authored_relarc/          per-episode RelationshipArc
authored_edges/           LocalEdge, PayoffCandidate, CrossEpisodeEdge
source_lock/              SourceLock v2
checkpoint_evidence/      unique two-episode checkpoints
validation/               machine and semantic audit outputs
manifests/                counts, lineage, supersession, package inventory
SHA256SUMS.txt
README.md
```

## Gate order

```text
G0 source/identity lock
G1 quarter direct-reading gate
G2 episode integration gate
G3 two-episode batch gate
G4 Stage03 participant/causality gate
G5 full-series Stage04 promotion gate
G6 anti-gaming and semantic sample gate
G7 package/SHA/report consistency gate
G8 reviewer approval → canonical
```

A later gate cannot repair a failed earlier gate by summary or aggregation.

## Deterministic hard failures

- missing or extra schema keys
- wrong types or enum values
- missing, duplicated, or out-of-order scenes
- invalid Stage02 turn_type→turn_class derivation
- invented core_mix values
- runtime shares that do not sum to 1.0
- missing or fictional scene/sequence references
- CharacterArc trigger without character
- RelationshipArc trigger without both characters
- LocalEdge label different from target core
- CrossEpisodeEdge without a source candidate or promotion evidence
- direct adjacent causality misfiled as Stage04
- ID collision
- unreplaced template variable
- normalized semantic template dominance ≥15%
- report/validation decision disagreement
- Python semantic generation
- raw script export in release
- missing or failing SHA manifest

## Required decision fields

```json
{
  "decision": "PASS_CANDIDATE|FAIL|QUARANTINE",
  "canonical_promotion_allowed": false,
  "structural_errors": [],
  "semantic_audit_errors": [],
  "warnings": [],
  "repairs_applied": [],
  "validator_versions": {},
  "source_lock_version": "2.0",
  "checkpoint_manifest_sha256": "...",
  "package_sha256": "..."
}
```

`canonical_promotion_allowed` remains false until reviewer/user approval, even when every automated gate passes.

## Stage01 contract

Exact keys:

```text
work_id, scene_no, heading, title, intent_gist, core, core2, skin, by
```

`core/core2` must use only the approved 16-value CORE_ENUM. Scene numbers are continuous ordinal values; source marker numbers are preserved separately when needed.

## Stage02 contract

Exact 18 keys:

```text
seq_id, work_id, episode_no, seq_index, member_scene_nos, scene_span,
scene_budget, sequence_intent, goal, obstacle, value_shift, turn_type,
turn_class, core_mix, pov_char, place_cluster, runtime_share, by
```

The validator must check the deterministic turn mapping itself, not only bucket membership.

## Stage03 contract

- EpisodeArc: exact 13 keys and complete sequence-span tiling.
- CharacterArc: exact 8 keys, character×episode records, real trigger participation.
- RelationshipArc: exact 9 keys, pair×episode records, both participants present.
- LocalEdge: exact 12 keys, causal, gap 0/1, target-core label.
- PayoffCandidate: exact 7 keys, hypothesis only.

## Stage04 contract

- Begins only after every episode passes Stage01~03.
- Every final edge has a real source candidate and later target.
- Direct adjacent causality remains a gap=1 LocalEdge.
- Guessed-type→final-type changes require a promotion rationale.
- Confidence is evidence-calibrated; a constant value across all edges is a warning or failure depending on scale.

## Evidence contract

Each quarter audit must include coverage, anti-gaming results, partial Stage02 coverage, source rechecks, repairs, decision, and next-allowed state. Each two-episode checkpoint is stored once and addressed by SHA. Duplicate evidence copied into multiple episode folders is prohibited in v2 releases.

## Supersession

A stronger validator may invalidate an earlier PASS. The new release must record:

```text
supersedes
superseded_reason
old_decision
new_decision
repair_scope
```

Never silently edit a historical PASS into a new result.
