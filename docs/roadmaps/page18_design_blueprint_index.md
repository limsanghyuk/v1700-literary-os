# Page18 Design Blueprint Index

Status: index draft
Created: 2026-06-10
Scope: index of Page18-adjacent design documents, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This index connects the additional Page18-adjacent design documents created after Page18 Entry Criteria.

It does not open Page18 and does not create Stage243+.

## 2. Current state

```text
Page18 implementation: absent
Stage243+ implementation: absent
Page18 Entry Criteria state: DECISIONS_PENDING
```

## 3. Core design additions

### 3.1 Limited scope selection

```text
docs/architecture/page18_limited_scope_options_blueprint.md
```

Purpose:

Defines the four allowed limited Page18 scopes and recommends Option B as first entry candidate.

### 3.2 Corpus ingestion adapter

```text
docs/architecture/corpus_ingestion_adapter_blueprint.md
```

Purpose:

Defines metadata-only corpus adapter planning.

### 3.3 Formula signal runtime bridge

```text
docs/architecture/formula_signal_runtime_bridge_blueprint.md
```

Purpose:

Defines how normalized formulas emit traceable FormulaSignalRecord outputs.

### 3.4 Value Proof experiment engine

```text
docs/architecture/value_proof_experiment_engine_blueprint.md
```

Purpose:

Defines controlled preregistered experiment infrastructure.

### 3.5 Writer IDE MVP interaction flow

```text
docs/architecture/writer_ide_mvp_interaction_flow_blueprint.md
```

Purpose:

Defines a non-canonical writer review MVP flow.

### 3.6 LearnableCritic audit engine

```text
docs/architecture/learnable_critic_audit_engine_blueprint.md
```

Purpose:

Defines audit-first coefficient diff and rollback validation.

## 4. Recommended implementation order after entry criteria

If Page18 later becomes allowed, recommended order is:

```text
1. Corpus ingestion adapter scaffold
2. Formula signal runtime bridge scaffold
3. Narrative corpus minimum fixture validation
4. Value Proof engine scaffold
5. LearnableCritic audit fixture validator
6. Writer IDE static review flow
```

## 5. Why Option B first

Option B is preferred because it is:

- metadata-only
- deterministic
- rights-policy governed
- directly connected to uploaded DB and formula materials
- useful for Value Proof
- useful for LearnableCritic
- useful for Writer IDE
- lower risk than live generation

## 6. Non-negotiable exclusions

Still excluded:

- autonomous writing engine
- LLM-2.0 generation-primary mode
- LLM-2.5 autonomous loop
- unlicensed full-text ingestion
- hidden coefficient learning
- automatic canonical mutation

## 7. Final decision

The next design layer is now connected.

However, implementation remains blocked until Page18 Entry Criteria is updated out of DECISIONS_PENDING.
