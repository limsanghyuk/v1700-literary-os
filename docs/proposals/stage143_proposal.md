# Stage143 Proposal - User CLI/API Minimum Docs

Stage143 converts the Stage142 benchmark-ready repository into a minimum user-facing documentation surface.

## Problem

Stage142 proves the runtime and benchmark pack are stable, but the repository still lacks a minimum user contract that explains how a human should invoke the CLI and what a future local API surface will look like.

## Proposal

Add a Stage143 documentation layer that:

- records CLI help, flags, and sample outputs as release evidence
- publishes a public-safe minimum API contract as documentation-only surface
- adds user-facing markdown under `docs/user/`
- emits a Stage144 readiness marker for CI/runtime split work

## Required Invariants

- Provider calls remain disabled.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight updates remain disabled.
- LOSDB writes remain disabled.
- Migration execution remains disabled.
- Node2 raw reveal access remains zero.
- Raw manuscript leakage remains zero.
