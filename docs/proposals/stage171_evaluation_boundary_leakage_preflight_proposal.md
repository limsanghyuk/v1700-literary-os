# Stage171 Proposal — Evaluation Boundary and Leakage Preflight

## Purpose

Stage171 verifies that Page05 evaluation remains a deterministic local evaluation layer and does not leak hidden payloads, raw reveal state, provider handles, mutation commands, credentials, or write authority.

## Scope

- inherited Stage167~170 gate matrix
- boundary invariant matrix
- Node2 surface projection scan
- forbidden operation registry
- controlled negative fixture quarantine
- leakage-zero snapshot
- Stage172 entry criteria

## Non-goals

- no provider judge
- no generation runtime
- no write path
- no memory write
- no canon mutation
- no runtime training
- no automatic repair apply

## Acceptance criteria

Stage171 passes only when all inherited gates pass, all boundary invariants are frozen, Node2 surface scan has zero forbidden hits, controlled negative fixtures are quarantined, and Stage172 entry criteria are true.
