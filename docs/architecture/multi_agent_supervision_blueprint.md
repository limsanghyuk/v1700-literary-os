# Multi-Agent Supervision Blueprint

Status: blueprint draft
Created: 2026-06-07
Scope: V1700 multi-agent planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines a future supervised multi-agent layer for V1700.

Agents are advisory specialists. They are not autonomous authority holders and cannot override canonical story authority.

## 2. Candidate agents

- Formula Critic
- Corpus Analyst
- Continuity Critic
- Dialogue Critic
- Emotion Critic
- Reader Signal Critic
- Rights and Safety Reviewer
- Principal Authority Reviewer

## 3. Agent capability scope

Every agent requires:

```text
agent_id
agent_role
allowed_inputs
allowed_outputs
forbidden_actions
source_policy_ref
approval_policy_ref
review_status
```

## 4. Agent outputs

Allowed output types:

- advisory note
- warning
- comparison
- candidate critique
- source risk note
- formula explanation
- corpus mapping note
- disagreement record

Forbidden output types:

- direct canonical mutation
- hidden memory update
- final writer decision
- formula authority replacement
- release authority decision

## 5. Disagreement preservation

If agents disagree, preserve disagreement.

Required record:

```text
AgentDisagreementRecord
```

Fields:

```text
disagreement_id
agent_refs
subject_record_id
claim_a
claim_b
supporting_evidence_refs
severity
recommended_resolution
final_reviewer_decision
```

## 6. Supervision model

```text
agent produces scoped advisory output
other agents may disagree
disagreement is recorded
Principal Authority Reviewer reviews only if needed
writer or designated authority approves canonical change
```

## 7. Integration targets

- Writer Narrative IDE
- LearnableCritic bridge
- Formula-to-corpus mapping
- Value Proof fixture
- corpus source policy
- LLM boundary ladder

## 8. Required future contracts

```text
docs/contracts/agent_capability_scope_contract.md
docs/contracts/agent_disagreement_record_contract.md
```

## 9. Blocking failures

- agent has no capability scope
- agent mutates canonical state
- agent uses unknown source class
- agent hides disagreement
- agent overrides writer approval
- agent promotes LLM output to authority

## 10. Final decision

Multi-agent supervision is accepted for planning only.

No autonomous agent authority is allowed before Page18 Entry Criteria and future contracts are approved.
