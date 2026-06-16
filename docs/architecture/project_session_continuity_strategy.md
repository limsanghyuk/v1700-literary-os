# Project Session Continuity Strategy

Status: ACTIVE_STRATEGY
Created: 2026-06-16
Scope: reduce long-chat weight and make multiple sessions in the same project share information through durable artifacts.

## 1. Problem

A single project can contain many planning, proposal, design, and implementation sessions. If one chat window is kept open for too long, it becomes heavy and loses operational clarity.

## 2. Core principle

Do not treat a long chat as the source of truth.

Use the repository hub as the source of truth:

```text
chat session = transient working surface
hub artifact = durable project memory
local codex output = executable local evidence
handoff document = cross-session bridge
```

## 3. Information sharing model

Same-project sessions should share information through these layers:

| Layer | Role | Reliability |
|---|---|---|
| Project instructions | stable operating policy | medium-high |
| Uploaded files | explicit evidence | high if cited |
| Hub repository docs | durable source of truth | high |
| Handoff files | session-to-session bridge | high if maintained |
| Chat memory | convenience context | medium |
| Raw conversation transcript | not assumed available | low unless exported |

## 4. Required hub artifacts

```text
docs/development/current_session_handoff.md
docs/development/session_handoff_protocol.md
docs/development/local_codex_execution_handoff.md
docs/roadmaps/v1700_document_index.md
docs/roadmaps/v1700_priority_development_sequence.md
docs/roadmaps/v1700_dependency_graph.md
fixtures/development/session_handoff_template.json
```

## 5. Session lifecycle

### Start of a new session

The assistant should first read:

```text
docs/development/current_session_handoff.md
docs/roadmaps/v1700_document_index.md
docs/roadmaps/v1700_priority_development_sequence.md
docs/roadmaps/v1700_dependency_graph.md
```

Then continue from `current_next_node` rather than asking the user to restate the project history.

### During a session

Only create durable artifacts for decisions that affect development order, schema, contracts, evidence, local execution, or safety boundaries.

### End of a session

Update:

```text
docs/development/current_session_handoff.md
fixtures/development/session_handoff_template.json
```

If new artifacts were created, also update:

```text
docs/roadmaps/v1700_document_index.md
docs/roadmaps/v1700_priority_development_sequence.md
docs/roadmaps/v1700_dependency_graph.md
```

## 6. Compression rule

Every long discussion should be compressed into four durable fields:

```text
decision
artifact_created
current_boundary
next_node
```

## 7. Boundary invariants

```text
Page18 implementation: NOT_OPENED unless explicitly approved
Stage243+: NOT_CREATED unless explicitly approved
Provider generation: DISABLED unless explicitly approved
Memory write: DISABLED unless explicitly approved
Canon mutation: DISABLED unless explicitly approved
Weight update: DISABLED unless explicitly approved
Raw copyrighted script text: DO_NOT_PUSH_TO_HUB
```

## 8. Recommended operating pattern

```text
1. Work in short sessions.
2. At each session end, write a handoff artifact.
3. Start each new session from the handoff and roadmap index.
4. Never depend on the chat window alone.
5. Treat hub docs and local Codex survey outputs as shared memory.
```

## 9. Current next node

```text
canonical_record_store_contract
```
