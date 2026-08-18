# Drama Close-Reading Continuous Analysis Protocol v2

Document ID: DRAMA-CLOSE-READING-CONTINUOUS-V2
Status: candidate authority
Purpose: enable a new ChatGPT/Claude/Codex session to analyze a new drama immediately, preserve continuity across episodes and sessions, and prevent semantic automation or false PASS results.

## 1. Operating model

The analysis is a close-reading authorship process, not a metadata conversion job.

```text
source episode
→ direct scene reading
→ Stage01 SceneCard
→ Stage02 SequenceBlueprint
→ Stage03 episode/character/relationship/causality ledgers
→ all-episode Stage04 fan-in
→ independent quality audit
```

Every upper stage must cite real records from the lower stage. An upper stage may not invent a scene, sequence, character appearance, relationship interaction, or payoff.

## 2. Production and delivery units

### User-facing unit

The normal delivery unit is `EP0(n)~EP0(n+1)`. A final unpaired episode may be delivered alone.

### Internal reading unit

Each episode is split into four deterministic quarters. Quarters are anti-automation reading units, not user approval units.

```text
EPn Q1 → Q2 → Q3 → Q4 → episode integration/audit
→ EPn+1 Q1 → Q2 → Q3 → Q4 → episode integration/audit
→ two-episode batch audit/package
```

A quarter PASS unlocks the next quarter; it is not a stopping point. The assistant continues until the requested delivery unit is complete.

## 3. Source intake and locking

Before semantic work:

1. Inventory every episode source file.
2. Detect original encoding without rewriting the original.
3. Identify scene markers and preserve both source marker and ordinal scene number when markers are duplicated or broken.
4. Build a character-name registry before Stage03.
5. Create SourceLock v2.

### SourceLock v2

```json
{
  "work_id": "<stable work id>",
  "episode_no": 1,
  "original_filename": "...",
  "original_encoding": "cp949",
  "original_bytes_sha256": "...",
  "normalized_encoding": "utf-8",
  "normalized_utf8_sha256": "...",
  "scene_count": 57,
  "scene_hash_algorithm": "sha256-normalized-scene-text",
  "scenes": [{"scene_no": 1, "source_marker_no": "1", "heading": "...", "scene_sha256": "..."}],
  "direct_reading_required": true,
  "raw_script_exported": false
}
```

The hash basis must be explicit. Never use one field named `source_sha256` for different byte representations.

## 4. Quarter workflow

Each quarter follows the same loop.

1. Open only the current quarter source span.
2. Read every scene in order.
3. Author Stage01 records directly.
4. While the scenes are fresh, identify partial Stage02 boundaries from changes in goal, obstacle, value, or turn.
5. Run the quarter gate.
6. Re-read and repair every failed scene or sequence.
7. Seal the quarter and update the order ledger.
8. Continue immediately to the next quarter.

### Quarter gate minimum evidence

```json
{
  "episode_no": 1,
  "quarter": "Q1",
  "scene_span": [1, 15],
  "scene_count": 15,
  "source_scene_hashes_verified": true,
  "stage01_coverage": "PASS",
  "stage02_partial_coverage": "PASS",
  "required_keys_errors": 0,
  "enum_errors": 0,
  "field_copy_errors": 0,
  "unreplaced_template_hits": 0,
  "visible_reference_template_hits": 0,
  "normalized_skeleton_dominance_failures": 0,
  "source_grounding_rechecks": [],
  "repairs_applied": [],
  "decision": "PASS_QUARTER_DIRECT_READING",
  "next_allowed": "Q2"
}
```

A quarter audit that contains only scene count, hashes, and a PASS sentence is insufficient.

## 5. Python boundary

### Allowed

- archive extraction and encoding conversion
- scene boundary and ordinal numbering support
- source hashes and SourceLock generation
- schema, type, enum, coverage, partition, count, and reference validation
- duplicate, n-gram, normalized-skeleton, and unreplaced-template detection
- character-presence lookup against already-authored/source-index records
- unchanged JSONL serialization
- manifest, SHA256SUMS, and ZIP packaging

### Forbidden

- keyword/theme extraction used to write semantic content
- `make_card`, `derive_*`, `generate_*`, or equivalent meaning-generation functions
- expanding `scene_action` into `information_delta`, `character_decision`, or `dramatic_function`
- creating CharacterArc, RelationshipArc, LocalEdge, PayoffCandidate, or CrossEpisodeEdge meaning
- bulk mutation of semantic fields to satisfy a validator

If a script accepts long semantic prose as hard-coded arguments, provenance must show that the prose was authored outside the script and the script only serialized unchanged records. Prefer authored TSV/JSONL/Markdown source files over semantic prose embedded in Python.

## 6. Stage01 — SceneCard

Canonical exact keys:

```text
work_id, scene_no, heading, title, intent_gist, core, core2, skin, by
```

Allowed `core/core2` values:

```text
ESTABLISH, ORACLE, INTRO, BOND, CONFLICT, REVERSAL, LOSS, PUNISH,
REVELATION, REUNION, RELIEF, ROMANCE, PERIL, RESCUE, DESIRE, HOOK
```

Rules:

- `title` identifies the unique dramatic event of the scene.
- `intent_gist` states what the scene changes or does in the drama, not merely what is visible.
- `heading/skin` preserve surface context; `intent_gist` carries interpretation.
- Exact or normalized template dominance of 15% or more is a failure.
- A scene that cannot be distinguished from another scene after names and enum tokens are masked must be re-read.

## 7. Stage02 — SequenceBlueprint

Exact 18 keys:

```text
seq_id, work_id, episode_no, seq_index, member_scene_nos, scene_span,
scene_budget, sequence_intent, goal, obstacle, value_shift, turn_type,
turn_class, core_mix, pov_char, place_cluster, runtime_share, by
```

Required invariants:

- every scene appears exactly once
- members are continuous and ordered
- `scene_span == [min(member), max(member)]`
- `scene_budget == len(member)`
- `value_shift == {"from": "...", "to": "..."}`
- sum of scene budgets equals episode scene count
- sum of runtime share equals 1.0 within numeric tolerance
- sequence/scene ratio is at least 0.11
- every `core_mix` value appears in a member scene's `core/core2`

### Deterministic turn policy v2

The published strict mapping is:

```text
RISE   ← RISE, BOND, PUNISH
FALL   ← FALL, LOSS
REVEAL ← REVEAL, REVELATION, ORACLE, REVERSAL
STALL  ← STALL, HOOK, CONFLICT
```

Until a complete tested registry is approved, `turn_type` must be limited to values covered by this mapping. Other SceneCard core values may appear in `core_mix`, but must not be used as `turn_type` merely because they are valid CORE_ENUM values.

The validator must check derivation, not only that `turn_class` is one of four strings.

## 8. Episode integration

After Q1~Q4:

1. merge Stage01 in ordinal order
2. rebuild Stage02 boundaries across quarter seams
3. verify no sequence crosses a quarter boundary without a recorded seam review
4. create EpisodeArc
5. create per-episode CharacterArc, RelationshipArc, LocalEdge, and PayoffCandidate
6. run the episode gate
7. seal the episode checkpoint

Q PASS does not imply episode PASS.

## 9. Stage03

### EpisodeArc — exact 13 keys

```text
work_id, episode_no, scene_count, sequence_count, dramatic_question,
act_structure, entry_state, exit_state, turning_point,
central_conflict_axis, episode_function, core_dist, by
```

The act structure follows real sequence hinges. Mechanical setup/expansion/reversal/closure quarter labeling is prohibited.

### CharacterArc — exact 8 keys

```text
work_id, character, episode_no, state_label, state_delta,
trigger_scene_no, by, evidence
```

One record per character×appearance episode, not one season summary. The trigger scene must contain the character. Evidence must describe what the event means for that character.

### RelationshipArc — exact 9 keys

```text
work_id, char_a, char_b, episode_no, relation_state, relation_delta,
trigger_scene_no, evidence, by
```

One record per relationship pair×interaction episode. Both characters must occur in the trigger scene.

### LocalEdge — exact 12 keys

```text
edge_id, work_id, edge_type, src_episode_no, src_scene_no,
tgt_episode_no, tgt_scene_no, gap_episodes, label, confidence, note, by
```

- `edge_type = causal`
- gap is 0 or 1
- label equals target scene core
- direct spillover to the next episode belongs here, not Stage04
- minimum eight substantive edges per episode is the default floor

### PayoffCandidate — exact 7 keys

```text
candidate_id, work_id, episode_no, scene_no,
edge_type_guess, description, by
```

Candidates are hypotheses, not confirmed payoffs. Normally record two to five per episode; exceeding the range requires an explicit density rationale.

## 10. Stage04 — full-series fan-in

Stage04 starts only after all episodes pass Stage01~03.

1. review every PayoffCandidate in episode order
2. locate an actual later target scene
3. compare source and target SceneCards and, when necessary, original source
4. reject unresolved or merely adjacent causal candidates
5. promote only verified callback, plant_payoff, or subplot_counterpoint edges
6. write a promotion ledger
7. build FullSeriesArc
8. run full-series validation

### Promotion ledger

```text
candidate_id, final_edge_id, source_episode, source_scene,
target_episode, target_scene, guessed_type, final_type,
source_evidence, target_evidence, promotion_rationale,
confidence_basis, reviewer
```

Any guessed-type→final-type change without rationale is a failure.

### Confidence calibration

Do not assign one constant confidence to all edges.

```text
0.98–1.00: explicit repeated object/dialogue/action and explicit resolution
0.93–0.97: direct causal setup/payoff with strong textual evidence
0.87–0.92: clear callback or subplot continuation with minor inference
0.80–0.86: interpretive counterpoint; requires reviewer note
below 0.80: do not promote without human review
```

## 11. Two-episode checkpoint structure

```text
checkpoint_evidence/
  batches/
    EP01_02/
      source_lock/
      authored_quarters/
      stage2_quarters/
      stage3/
      validation/
      order_guard/
      manifest.json
      SHA256SUMS.txt
```

Store a checkpoint once. Do not copy the same evidence into every episode folder. The final package references immutable batch checkpoints by hash and embeds or release-links each unique checkpoint.

## 12. Anti-gaming and semantic audit

Automatic checks:

- exact duplicates
- normalized skeleton dominance after masking names, numbers, scene IDs, and enums
- unreplaced variables
- visible scene-reference templates
- field-copy and scene-action embedding
- reference integrity
- participant presence
- false source/target core labels
- ID collisions
- report/validation disagreement

Manual semantic audit minimum:

- first, middle, and last scene of every episode
- every EpisodeArc turning point
- every CharacterArc/RelationshipArc trigger flagged by participant checks
- both endpoints of every Stage04 edge
- a stratified sample from each quarter

A machine PASS without semantic sampling is `STRUCTURAL_PASS_ONLY`, not canonical PASS.

## 13. Status model

```text
DRAFT            incomplete authorship
CANDIDATE        complete enough to audit
QUARANTINE       known contamination or invalid provenance
PASS_CANDIDATE   all current gates pass; awaiting user/reviewer approval
CANONICAL        approved and immutable except by superseding release
SUPERSEDED       replaced by a later audited release
```

## 14. Continuity across sessions

At the end of every completed batch, write:

- current completed episode span
- next allowed episode/quarter
- unresolved warnings
- checkpoint path and SHA
- canonical character-name registry
- source-lock registry
- Stage04 deferred-candidate count
- exact validator version

A new session must never infer completion from conversational progress messages. It must inspect the checkpoint manifest and resume from `next_allowed`.
