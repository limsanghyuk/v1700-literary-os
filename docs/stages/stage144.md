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

## Roadmap Status

Stage144 is the current roadmap terminus for the Stage140-144 product-proof line.
