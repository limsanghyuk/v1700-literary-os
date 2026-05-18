# Stage121 — Cross-Lineage Formula Reconciliation & Absorption Preflight

Stage121 keeps `Stage120 Gate25 NIE v1.0 Integrity FIXED` as the official trunk and treats `V545`, `V546`, and `V555` as reference branches only.

## Purpose

Stage121 does not merge candidate code. It produces machine-readable ledgers for formula relationships, packaging cleanliness, release gate authority, direct-merge blocks, and Stage122~126 absorption planning.

## Key decisions

- Stage120 remains the primary trunk.
- V545/V546/V555 direct merge is blocked.
- Stage120 Gate25 remains the primary release authority.
- V525 Gate25 is recorded as `Gate25-v2` candidate only.
- V545 Gate28 is a Stage123 secondary quality gate candidate.
- V555 Gate29 is a Stage124 predictive advisory/block gate candidate.
- Stage125 will introduce a Gate25/28/29 governor only after Gate28 and Gate29 have been safely absorbed.

## Required evidence

- `manifests/stage121_formula_ledger.json`
- `manifests/stage121_lineage_relationship_map.json`
- `manifests/stage121_conflict_matrix.json`
- `manifests/stage121_absorption_candidate_registry.json`
- `manifests/stage121_gate_authority_map.json`
- `release/current/stage121_cross_lineage_preflight_report.json`
- `release/current/stage121_formula_conflict_report.json`
- `release/current/stage121_packaging_cleanliness_report.json`
- `release/current/stage121_release_gate_report.json`

## Invariants

- provider default calls = 0
- live provider calls in release gate = 0
- Node2 raw reveal access = 0
- raw manuscript provider leakage = 0
- credential leakage = 0
- candidate direct merge = blocked
- internal `FILELIST.txt` and `SHA256SUMS.txt` required for release ZIP
