# P8.3 Metadata-Only Instantiated Ledger Design Report

Date: 2026-07-05  
Status: P8.3 remote design artifacts loaded  
Scope: Stage243 / P8.2 manual_review_required resolution / ledger schema and template

## 0. Executive Summary

P8.2 local execution completed the 11 deeper integrity checks at the available metadata level.

Current result:

```text
overall_deeper_integrity_status: manual_review_required
pass: 0
pass_with_warning: 4
manual_review_required: 7
fail_hard_rule: 0
blocked: 0
hard_rule_pass: false
gate_a_ready: false
scorecard_preflight_allowed: false
```

The next step is not P9.

The next step is P8.3: define and build metadata-only instantiated ledgers that can resolve the seven manual_review_required findings.

## 1. Created Artifacts

Created:

```text
release/current/season_wiring_pack/full_season_instantiated_ledger_schema_p8_3.json
release/current/season_wiring_pack/full_season_instantiated_ledger_fixture_p8_3.json
```

The schema defines the metadata-only ledger shape.

The fixture is template-only and must not be treated as evidence of hard-rule pass.

## 2. Why P8.3 Is Required

P8.2 showed that the project has corpus-level evidence and reference-level integrity, but the candidate package does not yet expose enough instantiated metadata to prove narrative integrity.

The unresolved areas are:

```text
series_to_season_integrity
season_to_episode_integrity
plant_payoff_integrity
character_arc_integrity
relationship_arc_integrity
causal_spine_integrity
hook_chain_integrity
```

These cannot be cleared by aggregate counts alone.

They require metadata-only ledgers containing IDs, references, transition links, and support relationships.

## 3. Ledger Families

P8.3 defines these ledger families:

```text
episode_node_ledger
sequence_binding_ledger
scene_binding_ledger
renderer_packet_binding_ledger
plant_payoff_ledger
character_arc_transition_ledger
relationship_arc_transition_ledger
causal_edge_ledger
hook_consequence_ledger
genre_rhythm_target_ledger
```

## 4. What The Ledger Must Prove

The ledger must prove, using only metadata:

```text
1. Season-level intent is instantiated into ordered episode nodes.
2. Episode nodes bind to sequence IDs.
3. Sequence IDs bind to scene IDs.
4. Scene IDs bind to renderer packet IDs.
5. Plant/payoff links have timing and location references.
6. Character transitions have causal support.
7. Relationship transitions have event support.
8. Causal edges connect episode, sequence, and scene events.
9. Hooks point to downstream consequences.
10. Genre rhythm targets are bound to scene-function evidence.
```

## 5. Boundary

P8.3 remains metadata-only. It must not perform source-content export, provider execution, live generation, canonical mutation, training update, adapter promotion, promotion claim, or P9 Scorecard execution.

## 6. Current Status After P8.3 Remote Design

```text
P8.3 schema: created
P8.3 template fixture: created
P8.3 local ledger build: required
Gate A: blocked
P9: blocked
Promotion: blocked
```

## 7. Next Required Step

Codex-local must populate or generate a metadata-only instantiated ledger result using the P8.3 schema.

Required local output:

```text
release/current/season_wiring_pack/full_season_instantiated_ledger_result_p8_3.json
release/current/transition_council_pack/p8_3_local_instantiated_ledger_build_report_20260705.md
```

After that, rerun:

```text
P8.2 deeper integrity check
full_season_hard_rule_self_check_v2 update or v3 creation
P8.1 validation if hard-rule state changes
```

P9 may be considered only if hard_rule_pass and gate_a_ready become true.
