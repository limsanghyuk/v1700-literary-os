# Drama Analysis — New Work Execution Runbook

This runbook is execution guidance under the current authority pointers. It does not replace them.

## 0. Resolve authority first

Read, in order:
1. `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`
2. `CURRENT_AUTHORITY_POINTER.json`
3. the authority and exact-schema registry named by that pointer
4. the current THICK/Planner/Runtime overlay pointer
5. `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md`
6. the target work SourceLock, work_state, and last durable checkpoint

Never hardcode a historical authority version. Resolve the current pointer every session.

## 1. Mandatory recovery preflight

Before new writing, reconcile durable disk state. Do not trust the previous chat progress message as the source of truth.

- Refuse to write if a previous writer process still owns the work lock.
- Compare semantic specs, atomic records, audits, episode assemblies, and work_state.
- Commit any valid pending semantic spec before writing a new one.
- Reassemble any completed episode whose episode file is missing.
- Resume only from the recomputed `next` sequence.

## 2. Determine target state

### Work has no Stage01–04
Follow the active Stage01–04 authority from direct source reading through Stage04 and validation before THICK.

### Work already has PASS Stage01–04 but no THICK
Do not blanket reauthor Stage01–04. Verify SourceLock/current work state and use existing SequenceBlueprint only as sequence boundaries. Re-read source directly and author THICK independently under the current strict new-work profile.

## 3. Stage01–04 invariant

One complete episode is the semantic authoring unit. Q1–Q4 and up-to-eight-episode blocks are attention/checkpoint/audit units only. LocalEdge is same-episode only; cross-episode relations belong to Stage04.

Python may extract, normalize, lock, hash, serialize, validate, compare, and package. Python must not generate narrative meaning.

## 4. THICK strict new-work profile

For each sequence, directly read its member-scene source ranges. Author sequence-specific cast desire/function, causal event chain, real information-state changes, source-supported plant/payoff, and one scene-note record per member scene.

Blocking patterns include Stage02-exact event reuse, Stage01/02-exact cast-function reuse, cast functions composed only of copied Stage01 sentences, generic cast templates, duplicate cast functions inside a sequence, and unresolved SOURCE/evidence for newly authored meaning.

Do not paraphrase merely to lower overlap metrics.

## 5. Interruption-safe execution

For THICK/new overlay authoring: `1 sequence = 1 atomic transaction`.

`SOURCE_READ → SEMANTIC_AUTHORED → spec atomic write → AUDIT_PASS → THICK record atomic write → episode assemble if closed → CHECKPOINT_LOCKED`

Use one commit process for persistence/validation after the model has authored the semantic JSON. Do not report completion before the checkpoint is durable.

### Response budget

- Maximum 3 newly authored sequences per assistant response.
- Source output should be chunked to roughly 8,000 characters or less per tool output.
- Soft source ceiling per response: roughly 30,000 characters.
- Multi-sequence full-source dumps are forbidden.
- Intentionally finish each response at a locked micro-batch checkpoint rather than running until forced interruption.

## 6. PlannerInput R5

Episode N may use only state available through N-1. EP01 has no previous exit state, prior character/relationship state, unresolved threads, or debt. Future/target source and analysis are holdout and must be blocked from generator input.

## 7. Runtime R8

R8 is deterministic projection from current CANONICAL THICK plus same-episode R5. It is not an independent semantic-authoring layer. If THICK changes, affected Runtime is stale and must be regenerated.

## 8. Promotion gate

Run exact schema, source/evidence, semantic-independence, R5/R8 parity, manifest/work_state, non-target immutability, package integrity, fresh extraction, and packaged validator checks. Promote only when blocking errors are zero. Preserve previous authority and artifacts through lineage/supersession; do not silently overwrite history.
