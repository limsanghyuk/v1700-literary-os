# Stage144 Proposal - Split CI Runtime Strategy

Stage144 converts the Stage143 CI/runtime readiness marker into a declared and gated operating model.

## Problem

By Stage143 the repository had enough release evidence to justify separate fast, core, full, and release-oriented automation lanes, but the split itself was still implicit.

## Proposal

Add a Stage144 workflow contract that:

- introduces a dedicated `ci-fast` lane
- preserves `ci-core`, `ci-full`, `cd-dry-run`, and `release` as distinct responsibilities
- records the runtime lane matrix as release evidence
- makes the split part of the release gate

## Required Invariants

- Provider calls remain disabled.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight updates remain disabled.
- LOSDB writes remain disabled.
- Migration execution remains disabled.
- Node2 raw reveal access remains zero.
- Raw manuscript leakage remains zero.
