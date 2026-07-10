# ChatGPT / Codex Work Division Protocol

Date: 2026-07-03  
Status: operating protocol  
Scope: Stage243 and later GPT V1700 Literary OS development

## 0. Purpose

This document fixes the working rule between ChatGPT and Codex for GPT V1700 Literary OS development.

The goal is to prevent confusion between:

```text
1. work ChatGPT can perform directly
2. work that must be performed on the local developer machine by Codex
3. work that must be verified and then loaded into the hub
4. work that must remain blocked for safety or authority reasons
```

This protocol applies to Stage243 and later planning, schema, data bridge, season wiring, evaluation, and promotion-evidence work.

## 1. Core Principle

```text
ChatGPT does the work it can do directly.
Codex performs only the work that requires local filesystem, local DB, local validation, local scans, or local git operations.
Every result must be explicitly checked, classified, and loaded or referenced in the hub before the next development step.
```

No task should be delegated to Codex merely by habit. Delegation requires a concrete reason.

## 2. Work ChatGPT Should Perform Directly

ChatGPT should directly perform the following whenever possible:

```text
planning decisions
architecture proposals
roadmap design
schema design
JSON contract design
promotion gate design
hard-rule gate design
evaluation rubric design
blocker interpretation
safety boundary interpretation
remote GitHub document creation
remote GitHub document update
hub-facing proposal/report generation
comparison and audit of already loaded metadata-only documents
next-step decision reports
```

Examples:

```text
macro_planner_hard_rule_gate.json design
macro_candidate_scorecard_schema.json design
promotion gate interpretation
Macro Planner / Full Author promotion decision analysis
Stage243 roadmap update
Page18~28 traceability review
```

## 3. Work Codex Should Perform Locally

Codex should be requested only when the task requires the developer machine or local filesystem.

Codex-local work includes:

```text
C:\AI_Codex local file inspection
large ZIP/archive inventory
local DB survey
local JSON/JSONL strict parse
local CRC/hash verification
local secret/token/private-key scan
local raw text/vector/archive leakage scan
local file generation under C:\AI_Codex
local git status / commit / push verification
copying metadata-only artifacts from local hub to a Git clone
checking whether C:\AI_Codex\codex-work\gpt is a Git repository
validating generated fixtures against local registry files
```

Codex should not be used to decide literary authority, promotion, or roadmap direction unless ChatGPT first defines the criteria.

## 4. Required Split Before Each Task

Before each new development task, the work must be split into three sections:

```text
A. ChatGPT-direct work
B. Codex-local work
C. Hub load / verification work
```

### A. ChatGPT-direct work

Use this when the task can be completed from conversation context, existing hub files, uploaded metadata, or remote GitHub documents.

### B. Codex-local work

Use this only when local files, local DB, local scans, or local git state are required.

### C. Hub load / verification work

Use this when outputs must be written to the hub, linked from handoff documents, parsed, scanned, or verified remotely.

## 5. Result Confirmation Protocol

Every completed step must produce a result packet with these fields:

```json
{
  "task_name": "string",
  "performed_by": "ChatGPT | Codex | Both",
  "execution_location": "remote_github | local_hub | local_only | conversation",
  "created_artifacts": [],
  "updated_artifacts": [],
  "verification": {
    "json_parse": "pass | fail | not_applicable",
    "secret_scan": "pass | fail | not_applicable",
    "raw_text_exported": false,
    "raw_vectors_exported": false,
    "provider_call_count": 0,
    "runtime_generation": false,
    "promotion_claim": false
  },
  "authority_status": {
    "local_hub_verified": "yes | no | not_applicable",
    "remote_github_verified": "yes | no | not_applicable",
    "promotion_status": "blocked | candidate | pass | not_applicable"
  },
  "next_required_step": "string"
}
```

## 6. Local vs Remote Authority Rule

Always separate the two states:

```text
Local Hub Authority = files verified in C:\AI_Codex local hub
Remote GitHub Authority = files verified in limsanghyuk/v1700-literary-os branch
```

A local completion report is not automatically a remote GitHub completion.

Correct wording:

```text
local completed / remote not yet verified
local completed / remote verified
remote created / local sync not verified
```

Incorrect wording:

```text
completed everywhere
officially loaded
merged
pushed
```

unless both local and remote evidence have been checked.

## 7. Safety Invariants

The following must remain false unless explicitly and safely promoted by an approved future stage:

```json
{
  "provider_default_calls": 0,
  "runtime_training_enabled": false,
  "canonical_mutation_allowed": false,
  "raw_text_exported": false,
  "raw_vectors_exported": false,
  "token_exported": false,
  "adapter_committed": false,
  "page18_runtime_opened": false,
  "stage244_automatic_creation": false,
  "promotion_claim": false
}
```

## 8. Promotion Interpretation Rule

ChatGPT is responsible for interpreting promotion status.

Codex may generate evidence packets, parse reports, and fixture validation results, but promotion decisions must be made against the hub-defined gates:

```text
Macro Planner Promotion
Full Author Promotion
Live Generation Readiness
```

Default current state:

```text
Macro Planner Promotion = blocked
Full Author Promotion = blocked
Live Generation Readiness = blocked
```

Fixture creation is not promotion.

Preflight pass is not promotion.

Metadata-only evidence is not live generation readiness.

## 9. Required Hub Load Rule

After each major task, one of the following must happen:

```text
1. ChatGPT writes the artifact directly to remote GitHub.
2. Codex writes the artifact locally and reports exact paths plus verification.
3. User or Codex pushes metadata-only artifacts to GitHub and ChatGPT verifies them remotely.
```

Every major task must update or reference one of the handoff/loadout documents:

```text
release/current/transition_council_pack/chatgpt_latest_hub_loadout.md
release/current/transition_council_pack/chatgpt_stage243_required_context.md
release/current/transition_council_pack/codex_work_method_handoff_for_chatgpt.md
release/current/transition_council_pack/stage243_schema_promotion_registry_handoff.md
release/current/transition_council_pack/chatgpt_codex_work_division_protocol.md
```

If the handoff document exists only locally, the response must say:

```text
local handoff updated / remote handoff not verified
```

## 10. Stage243 Current Next-Step Rule

For the current Stage243 flow:

```text
If the task is hard-rule design, scorecard schema, final verdict design, or promotion interpretation, ChatGPT should do it directly.

If the task is validating local fixtures, scanning files, parsing local JSON, checking archive leakage, or checking git status, Codex should do it locally.

If the task is remote hub creation or remote verification, ChatGPT can do it directly through GitHub connector.
```

## 11. Final Operating Decision

The operating decision is:

```text
ChatGPT will no longer defer design work to Codex by default.
Codex will be used only for local execution and validation tasks.
Both sides must produce explicit artifacts and verification evidence.
Every step must be loaded, referenced, or explicitly marked as local-only before the next step begins.
```
