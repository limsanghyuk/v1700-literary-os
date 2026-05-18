# Stage72.2 Roadmap

## Phase 0: Baseline Lock

Goal: freeze the current working state before adding capability.

Tasks:

```text
Verify active path: C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
Verify GitNexus index path: C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_2_ascii
Run gitnexus list
Run graph nexus release gate
Run release gate
Run pytest
Write baseline evidence to releases/v1700/stage72_2
```

Exit:

```text
GitNexus alias v1700_stage72_2_ascii exists
GraphNexus release gate pass
pytest 15 passed or better
```

## Phase 1: GitNexus Adapter Layer

Goal: create a controlled boundary around GitNexus CLI/MCP output.

Modules:

```text
src/v1700/sidecars/gitnexus/cli_adapter.py
src/v1700/sidecars/gitnexus/index_status.py
src/v1700/sidecars/gitnexus/stale_index_detector.py
src/v1700/sidecars/gitnexus/result_normalizer.py
```

Exit:

```text
adapter detects installed GitNexus
adapter detects registered alias
adapter can run query/impact with timeout
fallback is used when GitNexus is absent
```

## Phase 2: Query, Context, Impact, Detect Changes

Goal: expose the four most important GitNexus capabilities through V1700 GraphNexus.

Modules:

```text
src/v1700/graph_nexus/tools/query.py
src/v1700/graph_nexus/tools/context.py
src/v1700/graph_nexus/tools/impact.py
src/v1700/graph_nexus/tools/detect_changes.py
```

Tools:

```text
tools/run_graph_nexus_query.py
tools/run_graph_nexus_context.py
tools/run_graph_nexus_impact.py
tools/run_graph_nexus_detect_changes.py
```

Exit:

```text
query returns related stages/files/tests
context returns 360-degree symbol packet
impact returns upstream/downstream risk packet
detect_changes maps changed files to affected nodes and tests
```

## Phase 3: Route Map, Tool Map, Shape Check

Goal: convert graph context into developer-operational maps and safety gates.

Modules:

```text
src/v1700/graph_nexus/tools/route_map.py
src/v1700/graph_nexus/tools/tool_map.py
src/v1700/graph_nexus/tools/shape_check.py
```

Exit:

```text
route_map shows runtime flow and graph/narrative flow
tool_map links tools, gates, tests, release scripts
shape_check rejects invalid Node2 packets and raw reveal leakage
```

## Phase 4: Skills and Wiki Generation

Goal: preserve context in durable human/agent-readable artifacts.

Modules:

```text
src/v1700/graph_nexus/tools/skill_generator.py
src/v1700/graph_nexus/tools/wiki_generator.py
```

Generated outputs:

```text
docs/generated/skills/stage_skill_*.md
docs/generated/skills/node_skill_*.md
docs/generated/skills/scene_skill_*.md
docs/generated/wiki/architecture_wiki.md
docs/generated/wiki/stage_lineage_wiki.md
docs/generated/wiki/narrative_wiki.md
```

Exit:

```text
generated docs are deterministic
generated docs cite source files/manifests
generated docs do not expose secrets or raw reveal contents
```

## Phase 5: Stage72.2 Release Gate

Goal: make the new capability enforceable.

Add:

```text
src/v1700/gates/stage72_2_release_gate.py
tools/run_stage72_2_release_gate.py
tests/stage_gates/test_stage72_2_release_gate.py
manifests/stage72_2_manifest.json
release/current/stage72_2_release_gate_report.json
```

Exit:

```text
GitNexus adapter pass or fallback pass
query/context/impact/detect_changes pass
route_map/tool_map/shape_check pass
skills/wiki generation pass
Node2 raw reveal access remains 0
provider default calls remain 0
pytest passes
```

## Phase 6: Developer Handoff

Goal: prepare the next handoff state.

Tasks:

```text
update README
update STAGE_INDEX
write release evidence
package only after tests pass
do not include .gitnexus in GitHub-ready source package
keep GitNexus index under gpt/gitnexus_index as generated local state
```

Exit:

```text
Stage72.2 is ready for implementation review or Stage72.3 planning
```
