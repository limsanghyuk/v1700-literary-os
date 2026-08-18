# Drama Analysis Failure Recovery and Quality Gate Runbook v2

## 1. When execution is interrupted

1. Do not claim the episode or batch is complete.
2. Inspect actual files, row counts, hashes, quarter ledgers, and manifests.
3. Mark unsafely terminated output `candidate_only`.
4. Resume from the last sealed quarter, not from the last progress message.
5. Re-open and re-audit the first unsealed quarter.

## 2. When semantic automation is detected

Indicators:

- keyword fragments instead of sentences
- `[EPxx-Sxx]` templates in semantic fields
- `make_card`, `keywords`, `theme`, `derive_*` functions
- one scene field copied into other meaning fields
- high normalized-skeleton repetition
- provider/generation count inconsistent with claimed close reading

Response:

```text
quarantine contaminated semantic records
preserve source locks and scene boundaries
invalidate dependent Stage02~04 records
restart direct reading at the earliest contaminated quarter
```

## 3. When a stronger validator breaks a prior PASS

- preserve the prior package and hash
- issue an independent audit
- set the prior release to `SUPERSEDED` or `QUARANTINE`
- enumerate defects by record ID
- repair only after re-reading the affected source or sequence
- rerun all downstream gates
- update machine report, human report, README, and manifest together

## 4. When only metadata or provenance is defective

Examples: inconsistent character aliases, hash basis not declared, duplicated checkpoint evidence.

- Do not rewrite semantic prose unless its meaning is affected.
- Write a normalization ledger.
- State `semantic_text_changed: false` when true.
- Rerun participant, reference, ID, and package gates.

## 5. When Stage02 fails

- identify every failing sequence ID
- re-read member scenes
- restate goal, obstacle, value shift, and turn
- apply the approved deterministic turn registry
- do not bulk-relabel by enum string alone
- recheck coverage, core_mix, and runtime share
- rerun Stage03 references because sequence changes may affect EpisodeArc

## 6. When Stage04 fails

- return the edge to PayoffCandidate or LocalEdge
- verify both source and target scenes
- separate adjacent causality from long-range payoff
- create or repair promotion rationale
- recalibrate confidence from evidence
- rerun FullSeriesArc counts and all cross-edge references

## 7. Checkpoint recovery rule

A two-episode checkpoint is complete only when:

- both episodes have four sealed quarters
- both episode integration gates pass
- Stage03 records pass participant and causality checks
- checkpoint manifest and SHA are present
- the batch decision is internally consistent

Otherwise the checkpoint is not resumable authority.

## 8. False-PASS incident pattern

The P101 audit demonstrated a specific false-PASS pattern:

1. a validator checks that `turn_class` belongs to four buckets
2. it does not check whether `turn_class` was correctly derived from `turn_type`
3. 34 deterministic mismatches and 35 unmapped cases pass the shallow gate
4. the package is declared PASS despite a contract failure

Required prevention: validators must test relational invariants, not only field membership.

## 9. Evidence preservation after long work

Do not wait until the full season to preserve evidence. Seal each two-episode batch with:

```text
source_lock/
authored_quarters/
stage2_quarters/
stage3/
validation/
order_guard/
manifest.json
SHA256SUMS.txt
```

If a later session fails, earlier sealed batches remain valid candidates.
