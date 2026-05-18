# STAGE72.2: GitNexus Capability Absorption and GraphNexus Operationalization

Status: implemented.

## Goal

Stage72.2 turns GitNexus from an installed external sidecar into a controlled V1700 development capability.

The objective is not to copy GitNexus. The objective is to absorb its useful behaviors into GraphNexus so V1700 can prevent historical logic loss, map change impact, protect Node2 authority boundaries, and generate durable developer context.

## Baseline

Stage72.1 restored GraphNexus as:

```text
CodeGraph
NarrativeGraph
StageLineageGraph
GitNexus optional sidecar probe
Python fallback graph analysis
GraphNexus release gate
```

Current machine state:

```text
GitNexus installed: true
GitNexus alias: v1700_stage72_2_ascii
GitNexus index root: C:\AI_Codex\codex-work\gpt\gitnexus_index
GraphNexus release gate: pass
pytest: 15 passed
```

## Scope

Stage72.2 adds operational tools:

```text
query
context
impact
detect_changes
route_map
tool_map
shape_check
skill_generator
wiki_generator
```

Implemented outputs:

```text
src/v1700/sidecars/gitnexus/cli_adapter.py
src/v1700/sidecars/gitnexus/index_status.py
src/v1700/sidecars/gitnexus/stale_index_detector.py
src/v1700/sidecars/gitnexus/result_normalizer.py
src/v1700/graph_nexus/tools/
src/v1700/gates/stage72_2_release_gate.py
tools/run_stage72_2_release_gate.py
tools/run_graph_nexus_query.py
tools/run_graph_nexus_context.py
manifests/stage72_2_manifest.json
```

## Required Design Posture

```text
GitNexus = optional external sidecar
GraphNexus = V1700 core structure memory
Python fallback = mandatory safety path
Node2 = surface-only consumer
Node3 = critic/risk gate
```

## Non-Goals

Stage72.2 must not:

```text
vendor GitNexus source
make GitNexus a hard runtime dependency
allow Node2 raw graph or raw reveal access
enable automatic rename/migration without approval
enable embeddings by default
run provider calls during release gates
```

## Deliverables

```text
GraphNexus query/context/impact/detect_changes wrappers
GitNexus CLI adapter and result normalizer
stale index detector
runtime route map generator
tool/test/release map generator
IR shape checker
StageSkill / NodeSkill / SceneSkill generator
Architecture Wiki / StageLineage Wiki / Narrative Wiki generator
Stage72.2 release gate
Stage72.2 tests and fixtures
```

## Exit Gate

Stage72.2 is complete when:

```text
python tools/run_graph_nexus_query.py --q "Graph Intelligence"
python tools/run_graph_nexus_context.py --target Node2ProseCompiler
python tools/run_graph_nexus_impact.py --target Node2ProseCompiler
python tools/run_graph_nexus_detect_changes.py
python tools/run_graph_nexus_route_map.py
python tools/run_graph_nexus_tool_map.py
python tools/run_graph_nexus_shape_check.py
python tools/run_graph_nexus_generate_skills.py
python tools/run_graph_nexus_generate_wiki.py
python tools/run_stage72_2_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```

all pass without provider calls or Node2 raw reveal access.
