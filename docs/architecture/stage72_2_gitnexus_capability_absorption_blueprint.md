# Stage72.2 GitNexus Capability Absorption Blueprint

## Purpose

Stage72.2 upgrades Stage72.1 from a restored GraphNexus architecture into an operational structure-memory system.

The source proposal is:

```text
C:\Users\User\Downloads\지피티\개발 문서 개발자용\깃넥서스 기능 추가 적용.docx
```

The document's core decision is accepted with one correction: GitNexus external indexing is no longer incomplete on this machine. GitNexus is installed, Codex MCP setup has run, and the GPT-local Stage72.2 index is registered as `v1700_stage72_2_ascii`.

## Current Baseline

```text
Active repo:
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator

GitNexus index:
C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_2_ascii

GitNexus alias:
v1700_stage72_2_ascii
```

Validated baseline:

```text
GitNexus: installed
GraphNexus release gate: pass
Release gate: pass
pytest: 15 passed
Node2 raw reveal access: 0
Provider default calls: 0
```

## Architectural Decision

GitNexus remains an external optional sidecar. V1700 must not vendor GitNexus source code.

V1700 absorbs GitNexus capabilities as internal GraphNexus abstractions:

```text
GitNexus query          -> GraphNexusQuery
GitNexus context        -> GraphNexusContext
GitNexus impact         -> GraphNexusImpact
GitNexus detect_changes -> GraphNexusDetectChanges
GitNexus route map      -> GraphNexusRouteMap
GitNexus tool map       -> GraphNexusToolMap
GitNexus shape check    -> GraphNexusShapeCheck
GitNexus generated skills -> V1700 StageSkill / NodeSkill / SceneSkill
GitNexus Code Wiki      -> V1700 Architecture Wiki / StageLineage Wiki / Narrative Wiki
```

## Core Principle

GraphNexus is the product-level architecture.

GitNexus is a sidecar provider that can enrich GraphNexus when available.

Python fallback remains mandatory so the system can run on clean or restricted machines.

## Proposed Modules

```text
src/v1700/graph_nexus/tools/
  query.py
  context.py
  impact.py
  detect_changes.py
  route_map.py
  tool_map.py
  shape_check.py
  skill_generator.py
  wiki_generator.py

src/v1700/sidecars/gitnexus/
  cli_adapter.py
  mcp_adapter.py
  index_status.py
  stale_index_detector.py
  result_normalizer.py
```

## Internal Contracts

Stage72.2 should introduce stable dictionaries/dataclasses for these packets:

```text
GraphNexusQueryRequest
GraphNexusQueryResult
GraphNexusContextRequest
GraphNexusContextPacket
GraphNexusImpactRequest
GraphNexusImpactReport
GraphNexusDetectChangesReport
GraphNexusRouteMap
GraphNexusToolMap
GraphNexusShapeCheckReport
GeneratedStageSkill
GeneratedNodeSkill
GeneratedSceneSkill
GeneratedWikiPage
```

## Data Flow

```text
developer intent
  -> GraphNexus tool request
  -> GitNexus CLI/MCP adapter if available
  -> Python fallback if unavailable
  -> normalized GraphNexus packet
  -> Node authority filter
  -> release gate / developer report / wiki / skill artifact
```

## Node Authority Rules

Node1 may use structural graph context for story architecture decisions.

Node2 may only receive surface-safe packets:

```text
Node2GraphSurfacePacket
opaque forbidden reveal labels
relationship pressure
style drift warnings
sensory anchors
```

Node2 must never receive raw reveal contents, canon secrets, full graph internals, or unchecked GitNexus output.

Node3 receives contradiction risks, blast-radius risks, leakage risks, and shape-check failures.

## Safety Boundaries

The following features are restricted:

```text
cypher        -> read-only diagnostic mode only
rename        -> migration plan only, no automatic execution
embeddings    -> opt-in only, disabled in default gate
group sync    -> deferred until multi-machine standardization
auto-reindex  -> deferred; use stale-index detection and manual reindex suggestion first
```

## Acceptance Criteria

Stage72.2 passes only if:

```text
GitNexus installed path is detected or Python fallback is used
GraphNexus query/context/impact/detect_changes have deterministic outputs
route_map and tool_map identify runtime/gate/test paths
shape_check rejects raw reveal leakage into Node2
generated skills are written as reviewable markdown, not hidden state
wiki pages are deterministic and source-linked
release gate remains provider-call-free
pytest remains green
GitNexus index stays under gpt/gitnexus_index
```
