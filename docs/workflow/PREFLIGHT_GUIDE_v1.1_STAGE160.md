# V1700 Stage Development Preflight Guide V1.1

Document ID: V1700-PREFLIGHT-001  
Updated: 2026-05-25  
Applies to: all V1700 Stage development, integrity repair, release closure, and workflow upgrades

This guide adapts the `literary-os` workflow V1.1 into V1700 Stage language.

## Philosophy

Passing tests alone is not enough.

New logic must:

- preserve lineage and branchpoint survival
- remain visible to release gates and repo doctor
- keep provider-zero and privacy-zero invariants intact
- produce clean release evidence and release assets

## Fixed Sequence

### Step 1. Confirm repository state

- check the current branch
- pull or fetch the latest `main`
- identify the active Stage and latest relevant tag

### Step 2. Confirm working context

- read `docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md`
- read the Stage proposal and blueprint
- read the latest session note when relevant

### Step 3. Run the mandatory predevelopment check

```text
python tools/run_mandatory_predevelopment_check.py
```

### Step 4. Refresh GitNexus or record fallback

```text
gitnexus.cmd status
gitnexus.cmd analyze --force
```

If GitNexus cannot be used, the fallback must still be documented in the report.

### Step 5. Inspect the target scope

Review:

- target symbols
- target process or Stage flow
- manifest and release evidence that the new logic must touch
- upstream and downstream impact

### Step 6. Review invariant impact

Every change must be checked against:

- provider-zero
- write-zero
- training-zero
- raw manuscript leakage zero
- credential leakage zero
- branchpoint lineage preserved

### Step 7. Confirm design artifacts first

Before implementation, confirm or update:

- proposal
- blueprint
- developer handoff notes when the work changes the release path

### Step 8. Confirm required implementation surfaces

Most Stage work must account for some or all of these:

- source modules
- tests
- manifests
- release reports
- release gate registration
- repo doctor awareness
- package manifest and checksums

### Step 9. Implement in small steps

Prefer small, reviewable changes that keep the branch runnable.

### Step 10. Run the stage-specific gate

Run the relevant Stage gate and report generator for the work you changed.

### Step 11. Run the repository-wide gates

```text
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

### Step 12. Run tests

Run the most relevant pytest pack first, then the broader regression pack required by the Stage.

### Step 13. Re-index after material changes

If code, manifests, gates, or release logic changed materially:

```text
gitnexus.cmd analyze --force
```

### Step 14. Build release authority artifacts

Generate or refresh:

- canonical ZIP
- `.sha256` sidecar
- `SHA256SUMS.txt`

### Step 15. Re-verify extracted release state

Validate that a fresh extraction or fresh clone still reflects the active Stage across:

- README
- live manifest
- package manifest
- changelog
- release assets

## Blocking Conditions

Development must stop and be corrected if any of these fail:

- stage gate fails
- main release gate fails
- repo doctor fails
- GitHub CI fails after push
- manifests or docs disagree about the active Stage
- release ZIP and sidecar SHA disagree
- release assets are incomplete

## V1700 Translation Notes

The source `literary-os` document uses a versioned `V###` release model.  
V1700 uses `Stage###` naming, but the control points are equivalent:

- `V### branch` becomes `stageNNN-topic`
- `release gate` remains the pass/block authority
- `ZIP + SHA256` remains the official delivery model
- `GitHub main` remains the single stable baseline
