# Agent Capability Scope Contract

Status: contract draft
Created: 2026-06-09
Scope: future V1700 supervised multi-agent planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the capability boundary for future V1700 advisory agents.

Agents are scoped specialists. They are not autonomous authority holders, final writers, release authorities, or hidden memory writers.

## 2. Required record

```text
AgentCapabilityScopeRecord
```

## 3. Required fields

```text
agent_id
agent_name
agent_role
capability_scope
allowed_input_types
allowed_output_types
forbidden_actions
source_policy_ref
llm_boundary_ref
approval_policy_ref
canonical_mutation_allowed
review_status
created_at
updated_at
```

## 4. Candidate agent roles

```text
FormulaCritic
CorpusAnalyst
ContinuityCritic
DialogueCritic
EmotionCritic
ReaderSignalCritic
RightsAndSafetyReviewer
PrincipalAuthorityReviewer
```

## 5. Allowed input types

Depending on role, an agent may read:

- FormulaSignalRecord
- WorkRecord
- DramaEntryRecord
- CharacterRecord
- SceneBlueprintRecord
- CausalityMatrixRecord
- DialogueFunctionRecord
- CriticThresholdRecord
- ValueProofFixtureRecord
- LearnableCritic AdvisoryOutputRecord
- SourcePolicyRecord
- WriterSessionRecord
- ApprovalDecisionRecord

## 6. Allowed output types

Agents may output:

- advisory note
- risk warning
- formula explanation
- corpus mapping note
- continuity warning
- dialogue critique
- emotion progression note
- source rights warning
- rewrite candidate critique
- disagreement record

## 7. Forbidden actions

All agents are forbidden from:

- direct canonical mutation
- hidden memory update
- final writer decision
- formula authority replacement
- release authority decision
- hidden coefficient update
- hidden user preference update
- unapproved provider output promotion
- bypassing source policy

## 8. Canonical mutation rule

```text
canonical_mutation_allowed: false
```

No agent may directly write canonical story state. Canonical mutation requires a separate ApprovalDecisionRecord.

## 9. Source policy rule

Every agent that references corpus or external material must include:

```text
source_policy_ref
source_class
rights_status
provenance_ref
```

## 10. LLM boundary rule

If an agent uses LLM output, it must comply with:

```text
docs/architecture/v1700_llm_boundary_ladder_blueprint.md
```

No LLM output may be treated as canonical by the agent.

## 11. Review statuses

```text
DRAFT
ACTIVE_ADVISORY
SUSPENDED
REJECTED
DEPRECATED
```

## 12. Blocking failures

- missing capability scope
- missing forbidden action list
- canonical_mutation_allowed set to true
- source_policy_ref missing for source-dependent agent
- LLM boundary ref missing for LLM-assisted agent
- agent output used as final authority

## 13. Final decision

This contract enables future supervised multi-agent planning.

It does not implement agents and does not grant autonomous authority.
