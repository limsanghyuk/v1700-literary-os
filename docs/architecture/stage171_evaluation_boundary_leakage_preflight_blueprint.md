# Stage171 Blueprint — Evaluation Boundary and Leakage Preflight

## Architecture

```text
Stage170 evidence
→ inherited stage gate matrix
→ boundary invariant matrix
→ Node2 surface projection scan
→ forbidden operation registry
→ controlled negative fixture quarantine
→ leakage-zero snapshot
→ Stage172 entry criteria
```

## Required evidence files

```text
release/current/stage171_evaluation_boundary_leakage_preflight_pack/inherited_stage_gate_matrix.json
release/current/stage171_evaluation_boundary_leakage_preflight_pack/boundary_invariant_matrix.json
release/current/stage171_evaluation_boundary_leakage_preflight_pack/node2_surface_projection_scan.json
release/current/stage171_evaluation_boundary_leakage_preflight_pack/forbidden_operation_registry.json
release/current/stage171_evaluation_boundary_leakage_preflight_pack/controlled_negative_fixture_quarantine.json
release/current/stage171_evaluation_boundary_leakage_preflight_pack/leakage_zero_snapshot.json
release/current/stage171_evaluation_boundary_leakage_preflight_pack/stage172_entry_criteria.json
```

## Boundary rule

Controlled negative fixture artifacts may contain blocked tokens only as quarantined test evidence. Node2 surface projection artifacts must contain zero forbidden surface tokens.
