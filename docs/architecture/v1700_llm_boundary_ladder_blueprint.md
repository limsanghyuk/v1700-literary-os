# V1700 LLM Boundary Ladder Blueprint

Status: blueprint draft
Created: 2026-06-07
Scope: staged LLM boundary for V1700 post-roadmap planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint adapts the Claude/literary-os LLM-0 to LLM-2.5 relaxation model into V1700's authority system.

It defines staged LLM involvement without allowing provider output, critic output, or autonomous agent output to override canonical story authority.

## 2. Baseline rule

V1700 remains authority-first.

LLM output can be:

- advisory
- candidate-generating
- critic-assisting
- comparison-supporting
- explanation-supporting

LLM output cannot automatically be:

- canonical manuscript state
- formula authority
- memory authority
- release authority
- writer approval substitute

## 3. Boundary ladder

### 3.1 LLM-0 — No live LLM authority

Scope:

- no live provider in core authority
- deterministic formulas and records only
- external LLM may be absent

Allowed:

- static planning
- deterministic evaluation
- non-provider fixtures

Status:

```text
CURRENT_AUTHORITY_BASELINE
```

### 3.2 LLM-1 — Critic assistance only

Scope:

- LLM may support critic suggestions
- LLM may explain candidate weaknesses
- LLM may compare scene options

Allowed surfaces:

- critic panel
- rewrite candidate commentary
- Value Proof Arm B guidance if preregistered
- corpus metadata summarization if source policy allows

Forbidden:

- direct canonical mutation
- hidden user preference update
- formula authority replacement
- unregistered provider context in Value Proof

Required artifacts:

- Value Proof preregistration
- LLM assistance record
- source and prompt record
- provider boundary record

### 3.3 LLM-1.5 — Draft candidate generation

Scope:

- LLM may generate draft candidates
- writer approval required before insertion
- final text remains writer-approved canonical state only

Allowed surfaces:

- rewrite candidate comparison
- alternate dialogue proposal
- scene repair candidate
- synopsis variant candidate

Forbidden:

- automatic finalization
- direct canonical write
- unlogged prompt or context

Entry criteria:

- Value Proof signal positive
- writer approval contract exists
- corpus source policy active
- LLM-1 logs and boundaries validated

### 3.4 LLM-2.0 — Generation-primary candidate mode

Scope:

- LLM may produce larger candidate outputs
- V1700 structure and LearnableCritic supervise outputs
- human approval remains required

Status:

```text
DEFER_PENDING_EVIDENCE
```

Required before consideration:

- successful Value Proof full experiment
- corpus schema and source policy active
- LearnableCritic audit records active
- writer IDE approval workflow active
- multi-agent supervision contracts active

### 3.5 LLM-2.5 — Autonomous generation-evaluation loop boundary

Scope:

- potential future autonomous loop
- not permitted in current V1700 planning state

Status:

```text
DEFER_LONG_RANGE_ONLY
```

Hard requirements before consideration:

- autonomous loop safety policy
- multi-agent scope and disagreement contracts
- rollback mechanism
- rights and source policy
- human override
- release gate and GitNexus evidence

## 4. Required records

Future contract layer should define:

```text
LLMBoundaryRecord
ProviderInvocationRecord
PromptContextRecord
LLMOutputCandidateRecord
LLMCriticAssistRecord
LLMUsageCostRecord
LLMSourceBoundaryRecord
LLMApprovalDecisionRecord
```

## 5. Provider boundary rules

- provider keys never stored in code or documents
- prompts logged without secrets
- provider output labeled by model and configuration
- raw provider output cannot enter core authority without review
- all Value Proof provider use must be preregistered

## 6. Value Proof connection

The boundary ladder is tested first through LLM-1 only.

Value Proof Arm B may use:

- formula guidance
- critic guidance
- corpus metadata guidance
- structured state fields

Only if declared in preregistration.

## 7. Writer IDE connection

The IDE should display LLM outputs as:

- suggestion
- candidate
- comparison
- warning
- explanation

Never as automatic canonical text.

## 8. Blocking failures

- raw provider output enters canonical state
- LLM output overrides formula or Node authority
- hidden provider context is used in Value Proof
- provider output is used without provenance
- LLM-2.0 or LLM-2.5 behavior appears before entry criteria

## 9. Final decision

V1700 may plan for LLM-1 critic assistance first.

LLM-1.5 and above remain deferred until value proof, corpus, LearnableCritic, writer IDE, and multi-agent supervision gates mature.
