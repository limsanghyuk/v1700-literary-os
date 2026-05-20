# Stage136 Proposal - SchemaRegistry

## Summary

Stage136 upgrades Stage135 candidate-only output into deterministic, migration-ready schema definitions without introducing LOSDB writes or migration execution.

## Problem

Stage135 proves that candidate data can be recorded safely, but future stages still need a stable schema authority before any migration manager or storage contract can be introduced.

## Proposal

Add a SchemaRegistry that maps every Stage135 candidate decision to an explicit schema definition and validates every candidate against that schema catalog.

## Success Criteria

- Stage135 baseline gate passes.
- Every Stage135 candidate binds to exactly one Stage136 schema.
- Schema count is at least three: accepted, rejected, review-only.
- LOSDB writes remain disabled.
- Migration execution remains disabled.
- Provider calls remain zero.
- Stage136 release gate passes.
