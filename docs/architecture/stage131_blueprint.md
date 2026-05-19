# Stage131 Blueprint: GIG / Gate26 Advisory Absorption

## Purpose

Stage131 resolves the Stage130 deferred Gate26 problem by adding a deterministic advisory governance layer. It does not convert Gate26 into a hard-blocking authority.

## Architecture

```text
Stage130 MultiWork Release
  -> gig_advisory.classifier
  -> gig_advisory.policy
  -> gig_advisory.preflight
  -> stage131.runner
  -> stage131_release_gate
  -> main release gate
```

## Runtime Modules

```text
src/v1700/gig_advisory/
  contracts.py
  classifier.py
  policy.py
  preflight.py
  report.py

src/v1700/stage131/
  stage131_runner.py

src/v1700/gates/
  stage131_release_gate.py
```

## Advisory Case Matrix

| Case | Classification | Action |
| --- | --- | --- |
| GIG-TRUE-001 | true_contradiction | REVIEW_REQUIRED |
| GIG-MYST-001 | intentional_mystery | ALLOW_WITH_LOCK |
| GIG-MIS-001 | character_misunderstanding | ALLOW_WITH_POV_TAG |
| GIG-DELAY-001 | reveal_delay | ALLOW_WITH_REVEAL_BUDGET |

## Hard Invariants

```text
provider_default_calls = 0
live_provider_call_count_in_release_gate = 0
node2_raw_reveal_access = 0
raw_manuscript_provider_leakage = 0
raw_manuscript_cross_project_leakage = 0
credential_leakage = 0
cross_project_write_allowed = false
gate26_hard_block_enabled = false
canon_auto_resolution_count = 0
auto_repair_mutation_count = 0
```

## Release Evidence

```text
release/current/stage131_gig_advisory_report.json
release/current/stage131_release_gate_report.json
release/current/stage131_gig_advisory_pack/
  classifier_report.json
  policy_report.json
  gitnexus_preflight_report.json
  stage131_summary.json
```

## GitNexus Preflight Policy

GitNexus native indexing is attempted before release. If native indexing is unavailable or fails, Stage131 must record the attempt and proceed only if GraphNexus/Python fallback confirms:

- critical symbols exist
- Stage131 gate is registered
- repo doctor recognizes Stage131
- survival matrix preserves provider-zero, Node2 boundary, raw manuscript privacy, MultiWork authority, and branchpoint lineage
