# Stage141 Proposal - Prose Generation E2E Harness

Stage141 upgrades the Stage140 product-proof skeleton into a deterministic local prose-generation E2E harness.

## Problem

Stage140 proved that metadata, release assets, sample project contracts, and benchmark skeleton contracts are aligned. The next gap is product proof: the repository still needs an actual rendered scene and critic-validated output that shows the literary pipeline can run end-to-end on public-safe synthetic inputs.

## Proposal

Add a Stage141 harness that:

- loads the synthetic sample project from `samples/korean_drama_family_secret/`
- builds a deterministic `SceneIntentIR`
- renders one or more scenes through Node2
- validates the result through Node3
- emits benchmark-ready evidence under `release/current/` and `benchmarks/longform_output/results/`

## Required Invariants

- Provider calls remain disabled.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight updates remain disabled.
- LOSDB writes remain disabled.
- Migration execution remains disabled.
- Node2 raw reveal access remains zero.
- Raw manuscript leakage remains zero.
