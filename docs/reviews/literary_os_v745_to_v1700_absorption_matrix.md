# Literary OS V745 to V1700 Absorption Matrix

Status: review draft
Created: 2026-06-07
Scope: Absorb / reject / defer decisions for limsanghyuk/literary-os V745+ concepts into V1700
Repository: limsanghyuk/v1700-literary-os
External reference: limsanghyuk/literary-os V745 / Phase E planning

## 1. Purpose

This matrix decides how concepts from Claude/literary-os V745 and Phase E planning may be absorbed into V1700.

This is not a merge plan. This is a controlled absorption review.

## 2. Decision labels

- ACCEPT_FOR_V1700_PLANNING
- ACCEPT_FOR_V1700_IMPLEMENTATION_AFTER_ENTRY_GATE
- DEFER_PENDING_EVIDENCE
- REJECT_FOR_AUTHORITY_CONFLICT
- REJECT_FOR_RIGHTS_OR_SOURCE_RISK
- REJECT_FOR_RUNTIME_SCOPE_MISMATCH

## 3. Baseline

V1700 current baseline:

- Page17: PASS_WITH_GITNEXUS_OUTPUT
- Stage242: PASS_WITH_GITNEXUS_OUTPUT
- Page18 implementation: absent
- Stage243+ implementation: absent
- Mode: post-roadmap planning and authority review

Claude/literary-os baseline:

- V745 / v13.0.0 / Phase D Exit
- 97 gates
- 10788+ tests
- 13-step preflight
- Phase E validation-first entry

## 4. Absorption matrix

| Source concept | Source track | Decision | V1700 target | Required artifact | Risk | Notes |
|---|---|---|---|---|---|---|
| RULE-0 preflight | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Post-roadmap development protocol | v1700_post_roadmap_integrity_self_verification_blueprint | Medium | Must adapt to GitNexus and page/stage authority |
| 13-step preflight | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Runtime integrity bridge | v1700_post_roadmap_integrity_self_verification_blueprint | Medium | Should become V1700 document-first preflight before Page18 |
| Survival Matrix | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Release readiness and runtime bridge | future SurvivalMatrixContract | Medium | Useful but needs V1700 contract mapping |
| G_CONNECTIVITY | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | GitNexus + runtime connectivity | future ConnectivityParityReport | Low | Complements GitNexus graph evidence |
| Release block conditions | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Clean release authority | post_roadmap_clean_release_decision | Low | Should be mapped to no hidden warnings / no stale checksum |
| SP-E.0 integrity recovery | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | P1 integrity self-verification | v1700_post_roadmap_integrity_self_verification_blueprint | Low | High priority because V1700 also packages artifacts |
| G_INTEGRITY_MANIFEST | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Release self-check gate | v1700_post_roadmap_integrity_self_verification_blueprint | Low | Should verify SHA256, filelist, inventory, gate files |
| ADR continuity gate | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Roadmap and document continuity | doc_continuity_gate_blueprint | Medium | Translate ADR to V1700 docs/page/stage lineage |
| G_VALUE_PROOF | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Post-roadmap value proof gate | post_roadmap_value_proof_gate_blueprint | Low | Already partially planned in V1700 |
| Value proof MVE | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Minimum experiment fixture | value_proof_minimum_fixture_spec | Medium | Must control length, prompt, token budget, blinded evaluation |
| Preregistration threshold | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Value proof preregistration | value_proof_preregistration_template | Low | Required before any experiment claim |
| LLM-1 critic boundary | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | V1700 LLM boundary ladder | v1700_llm_boundary_ladder_blueprint | Medium | Must preserve Node authority and provider boundaries |
| LLM-1.5 draft generation boundary | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future Page18+ execution engine | future execution engine roadmap | High | Requires value proof first |
| LLM-2.0 generation-primary mode | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future roadmap only | none yet | High | Too early for V1700 current authority state |
| LLM-2.5 autonomous loop | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future roadmap only | none yet | Very high | Not allowed until multi-agent safety and value proof maturity |
| LearnableCritic | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Learnable Critic Bridge | learnable_critic_record_contract | Medium | Must remain advisory and auditable |
| Coefficient gradient update | Claude/literary-os / formula archive | ACCEPT_FOR_V1700_PLANNING | Coefficient audit record | coefficient_audit_record_contract | Medium | No hidden coefficient update |
| RLAIF | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future value proof / critic layer | future RLAIF policy | High | Requires corpus, rights, safety, cost and evaluator policy |
| Corpus 50 works | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Narrative corpus database | narrative_corpus_source_policy, narrative_corpus_schema_v0_1 | Medium | Must use rights-aware metadata approach |
| Corpus 200 works | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future corpus expansion | future corpus scale roadmap | Medium | After schema and pilot records |
| 3-zone UI | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Writer collaborative Narrative IDE | writer_narrative_ide_wireframe_blueprint | Low | Already aligns with V1700 IDE proposal |
| Plugin sandbox | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Page17 plugin/studio boundary | future plugin runtime bridge | Medium | Must not bypass V1700 Page17 authority |
| ZeroTrust / tenant authority | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Productization and release authority | future productization roadmap | Medium | Later P8, not immediate |
| Federated learning | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future learning infrastructure | none yet | High | Not needed before LearnableCritic contracts |
| Disaster recovery gate | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | Release/productization safety | future DR/release blueprint | Low | Useful for later productization |
| B2B SaaS and marketplace | Claude/literary-os | DEFER_PENDING_EVIDENCE | Productization phase | productization_and_release_authority_roadmap | High | Too early before value proof |
| Billing integrity gate | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future product gate | future billing policy | High | Not relevant until productization |
| Phase F multilingual track | Claude/literary-os | DEFER_PENDING_EVIDENCE | Future corpus/product roadmap | future multilingual roadmap | Medium | Requires corpus and value proof maturity |
| Government R&D + studio partnership | Claude/literary-os | ACCEPT_FOR_V1700_PLANNING | External strategy note | future partnership strategy | Medium | Business track separate from Page18 implementation |

## 5. Formula archive absorption notes

| Formula group | Decision | Target V1700 artifact | Notes |
|---|---|---|---|
| DRSE | ACCEPT_FOR_V1700_PLANNING | formula_catalog_normalization_report | Needs mapping to corpus state records |
| Narrative State Tensor | ACCEPT_FOR_V1700_PLANNING | formula_to_corpus_mapping_blueprint | Should map to scene/character/emotion records |
| Narrative Fitness Score | ACCEPT_FOR_V1700_PLANNING | Value Proof metrics / LearnableCritic | Must not substitute human blind evaluation |
| Gradient coefficient update | ACCEPT_FOR_V1700_PLANNING | coefficient_audit_record_contract | Requires seed, diff, rollback |
| Emotional Momentum | ACCEPT_FOR_V1700_PLANNING | corpus schema and critic bridge | Maps to scene emotion transitions |
| CIM / interaction matrix | ACCEPT_FOR_V1700_PLANNING | narrative_corpus_schema_v0_1 | Maps to CharacterRecord and relationship links |
| RAG/BM25/RRF fusion | ACCEPT_FOR_V1700_PLANNING | corpus retrieval policy | Must respect source rights |
| Fourier tension curve | ACCEPT_FOR_V1700_PLANNING | value proof metrics and scene analysis | Needs clear measurement definition |
| Governance / hub/package authority formulas | ACCEPT_FOR_V1700_PLANNING | integrity self-verification | Aligns with release authority planning |

## 6. Database archive absorption notes

| DB group | Decision | Target V1700 artifact | Notes |
|---|---|---|---|
| K-Drama Master DB row dumps | ACCEPT_FOR_V1700_PLANNING | narrative_corpus_schema_v0_1 | Use as schema seed, subject to source policy |
| Cinematic Sovereign DB dump | ACCEPT_FOR_V1700_PLANNING | narrative_corpus_schema_v0_1 | Extends schema to film/cinematic structures |
| Drama_Entry structure | ACCEPT_FOR_V1700_PLANNING | DramaEntryRecord | Must normalize against WorkRecord |
| Master_Theme / Conflict_Axis | ACCEPT_FOR_V1700_PLANNING | CorePhilosophyRecord | Maps to formula and value proof axes |
| Character / Key_Object | ACCEPT_FOR_V1700_PLANNING | CharacterRecord / KeyObjectRecord | Should support graph links |
| Causality_Matrix / Trigger / Resolution / Residue | ACCEPT_FOR_V1700_PLANNING | CausalityMatrixRecord | Important for causality and payoff analysis |
| Dialogue_Tone / Style_Module | ACCEPT_FOR_V1700_PLANNING | DialogueFunctionRecord / StyleModuleRecord | Useful for writer IDE right panel |
| Critic_Thresholds | ACCEPT_FOR_V1700_PLANNING | CriticThresholdRecord | Useful for LearnableCritic initial thresholds |
| Scene_Blueprint / Scene_Blueprint_V8 | ACCEPT_FOR_V1700_PLANNING | SceneBlueprintRecord | Should feed value proof fixture design |
| Tragic_Engine | ACCEPT_FOR_V1700_PLANNING | GenreEngineRecord | Needs genre-specific mapping |

## 7. Rejected or deferred items

Rejected now:

- direct code merge from Claude/literary-os into V1700
- immediate Page18 implementation
- immediate Stage243+ creation
- LLM-2.0 generation-primary authority
- LLM-2.5 autonomous loop authority
- unlicensed full-text corpus ingestion

Deferred pending evidence:

- RLAIF implementation
- federated learning integration
- B2B SaaS / marketplace / billing gates
- multilingual production track
- full execution engine runtime

## 8. Immediate accepted planning queue

Accepted next planning documents:

```text
docs/reviews/formula_catalog_normalization_report.md
docs/architecture/v1700_post_roadmap_integrity_self_verification_blueprint.md
docs/policies/narrative_corpus_source_policy.md
docs/architecture/narrative_corpus_schema_v0_1.md
docs/architecture/formula_to_corpus_mapping_blueprint.md
docs/architecture/v1700_llm_boundary_ladder_blueprint.md
```

## 9. Final decision

Claude/literary-os V745 concepts are valuable but must be absorbed selectively.

The strongest immediate absorptions are:

1. SP-E.0 integrity self-verification
2. G_VALUE_PROOF
3. LLM-1 critic boundary
4. LearnableCritic with audit/rollback
5. corpus schema and rights-aware metadata strategy
6. 3-zone writer IDE model

The strongest immediate block is:

```text
No Page18 implementation until entry criteria are completed.
```
