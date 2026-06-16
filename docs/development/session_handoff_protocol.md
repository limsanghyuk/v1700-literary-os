# Session Handoff Protocol

Status: ACTIVE_PROTOCOL
Created: 2026-06-16
Scope: operational protocol for continuing V1700 work across multiple short sessions.

## 1. Purpose

Prevent long-session overload by converting each session into compact, durable, hub-readable state.

## 2. Start-session checklist

At the beginning of a new session, inspect the following hub files:

```text
docs/development/current_session_handoff.md
docs/roadmaps/v1700_document_index.md
docs/roadmaps/v1700_priority_development_sequence.md
docs/roadmaps/v1700_dependency_graph.md
fixtures/development/session_handoff_template.json
```

## 3. Working-session checklist

During a session, record only durable decisions:

```text
new artifact path
new contract/schema decision
new fixture/result artifact
local execution requirement
boundary change request
blocked or deferred action
next node change
```

## 4. End-session checklist

Before closing or moving to a new chat, update:

```text
docs/development/current_session_handoff.md
fixtures/development/session_handoff_template.json
```

If new roadmap-level artifacts were added, update:

```text
docs/roadmaps/v1700_document_index.md
docs/roadmaps/v1700_priority_development_sequence.md
docs/roadmaps/v1700_dependency_graph.md
```

## 5. Handoff fields

Each handoff must include:

```text
session_date
branch
last_commit
created_artifacts
current_readiness
next_node
active_boundaries
local_codex_actions
known_blockers
safe_upload_rule
```

## 6. Minimal next-session prompt

Use this prompt at the start of a new session:

```text
Read the current session handoff, document index, priority sequence, and dependency graph from the hub. Continue from next_node without reopening Page18 or Stage243 unless explicitly approved.
```

## 7. Local Codex integration

For local-only data, Codex should run scripts locally and return metadata-only outputs.

Use:

```text
docs/development/local_codex_execution_handoff.md
tools/local_db_inventory.py
```

## 8. Prohibited session carryover assumptions

Do not assume:

```text
all prior chat text is available
all prior rationale is remembered
raw local DBs are accessible
raw copyrighted corpus can be pushed
CI passed if workflow_runs is empty
```

## 9. Current state

```text
current_readiness: READY_FOR_CANONICAL_RECORD_STORE_CONTRACT
next_node: canonical_record_store_contract
```
