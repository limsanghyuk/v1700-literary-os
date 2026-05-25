# Stage164 Blueprint — Surface Draft Dry-Run Renderer

## Inputs

- Stage163 deterministic render plan
- Stage162 render packet store
- Page04 rendering contract

## Outputs

- surface draft units
- dry-run render trace
- surface boundary snapshot
- Node2 surface draft projection matrix
- rendering side-effect-free policy
- deterministic surface draft checksum
- Stage165 entry criteria

## Algorithm

1. Load and validate the Stage163 render plan.
2. Create one deterministic surface draft unit per render plan node.
3. Build a trace step for each draft unit.
4. Reject forbidden hidden/provider/write/raw payload tokens.
5. Generate checksum and release evidence.

## Invariants

Provider generation, runtime rendering, writes, training, memory mutation, and canon mutation remain disabled.
