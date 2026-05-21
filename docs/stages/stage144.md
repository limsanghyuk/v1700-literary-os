# V1700 Literary OS - Stage144

> Split CI Runtime Strategy

## Goal

Stage144 turns the Stage143 readiness marker into an implemented workflow contract. The repository now declares separate fast, core, full, dry-run, and release lanes while preserving all provider-zero and write-zero constraints.

## What Stage144 Adds

- `ci-fast` for current-stage invariant checks
- `ci-core` for active-lineage pytest and staged gates
- `ci-full` for scheduled full-suite sweeps
- `cd-dry-run` for package rehearsal
- `release` for tagged canonical package publication

## Invariants

- No provider calls
- No runtime training
- No active meta-learning
- No model weight updates
- No LOSDB writes
- No migration execution
- No Node2 raw reveal access

## Evidence

- `release/current/stage144_split_ci_runtime_strategy_report.json`
- `release/current/stage144_release_gate_report.json`
- `release/current/stage144_release_asset_manifest.json`
- `release/current/stage144_split_ci_runtime_strategy_pack/`

## Integrity Status

Stage144 release integrity now treats the source ledger as a blocking release condition. `FILELIST.txt` and `SHA256SUMS.txt` must match the current checkout, every listed file must exist, every listed digest must match current content, and no checksum entry may point outside `FILELIST.txt`.

`SHA256SUMS.txt` is excluded from `FILELIST.txt` by policy to avoid self-referential checksum drift. The release asset integrity gate verifies that exclusion explicitly.

Current generated release evidence remains listed in `FILELIST.txt`, but `release/current/**/*_report.json` and `release/current/**/*_summary.json` files are not content-digest blocking while gates execute because they are rewritten by the gate commands themselves.

Text-file digests are computed after CRLF-to-LF normalization so the same ledger is valid on Windows and Linux checkouts.

## Workflow Contract Status

Stage144 validates the declared split across `ci-fast`, `ci-core`, `ci-full`, `cd-dry-run`, and `release`. The contract checks required triggers, required Stage144 commands, dry-run artifact naming, canonical release ZIP naming, sidecar generation, and GitHub release publication wiring.

## Roadmap Status

Stage144 is the current roadmap terminus for the Stage140-144 product-proof line.
