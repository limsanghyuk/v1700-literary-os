# Stage137 Proposal - MigrationManager

## Summary

Stage137 upgrades Stage136 schema-ready bindings into a deterministic migration plan without permitting migration execution or LOSDB writes.

## Problem

Stage136 proves schema authority, but Stage138 storage contracts still need an ordered migration plan with rollback anchors and human approval checkpoints before any storage work can begin.

## Proposal

Add a MigrationManager that turns Stage136 schema bindings into dry-run migration steps, approval checkpoints, and rollback-ready metadata.

## Success Criteria

- Stage136 baseline gate passes.
- Every Stage136 binding is covered by exactly one planned migration step.
- Review-only bindings route through a human approval checkpoint.
- Every migration step carries rollback metadata.
- LOSDB writes remain disabled.
- Migration execution remains disabled.
- Stage137 release gate passes.
