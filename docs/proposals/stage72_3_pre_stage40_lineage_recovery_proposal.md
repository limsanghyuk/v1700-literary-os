# Stage72.3 Proposal: Pre-Stage40 Lineage Recovery and Organic Impact Governance

## 1. Proposal Summary

Stage72.3 should restore the disconnected Stage01-39 inheritance layer and convert the development process itself into a GitNexus-style impact-governed workflow.

The goal is not to copy every old file into the active runtime. The goal is to identify which early-stage concepts are still essential, where they currently survive, where they were lost, and what must be implemented next.

This stage exists because the project has repeatedly experienced a known development failure mode:

```text
new patch solves the immediate problem
  -> older logic is accidentally bypassed
  -> later stage must return and reconnect the missing concept
```

Stage72.3 prevents that pattern by requiring every future addition or modification to pass a lineage and impact review before promotion.

## 2. Background

Stage72.2 successfully absorbed GitNexus capabilities into GraphNexus:

```text
query
context
impact
detect_changes
route_map
tool_map
shape_check
generated skills
deterministic wiki
```

However, the current formal lineage manifest starts at Stage40:

```text
manifests/stage_lineage_manifest.json
```

This means Stage40-72.2 is visible to GraphNexus, but Stage01-39 is still mostly stored as historical evidence in:

```text
C:\AI_Codex\codex-work\gpt\knowledge_base\v1650_stage35_critic_comparison_gate
```

That knowledge base contains important early-stage logic, including:

```text
multi-provider creative comparison
provider execution tracing
authoring scenario runner
memory conflict resolver
Node2 literary quality engine
literary depth calibration
long horizon memory drift stress
authoring review workflow
human/agent review console
episode draft export harness
series arc control
Node2 style evolution memory
boundary registry
release candidate gates
stage26-28 regression stream
stage33 concept validation workbench
stage39 temporal continuity
stage39 longform scene-sequence planner
stage39 branch commit/rollback
stage39 emotional pressure valve
stage39 Node2 candidate rendering
```

These are not obsolete. They are the early conceptual DNA of the literary generator.

## 3. Problem Statement

The current repository has two truths:

```text
Active runtime:
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator

Historical knowledge base:
C:\AI_Codex\codex-work\gpt\knowledge_base\v1650_stage35_critic_comparison_gate
```

The active runtime is clean, testable, and packageable. The historical knowledge base is rich but too large, old, and structurally noisy to be imported wholesale.

The risk is that future development may continue in the clean active repo while forgetting high-value early logic from Stage01-39.

The specific missing governance problem is:

```text
Before changing code, the system does not yet require:
1. Which old concepts are related?
2. Which current modules would be affected?
3. Which tests/gates prove the old concept still survives?
4. Which old concepts are only documented but not executable?
5. Which future implementation should restore the gap?
```

## 4. Design Principle

Stage72.3 should use the GitNexus principle, but apply it to the project lineage itself.

GitNexus principle:

```text
before changing a symbol, inspect context, impact, callers, routes, and tests
```

V1700 lineage principle:

```text
before changing a creative engine concept, inspect old stage origin, current runtime anchor, affected nodes, affected gates, and missing survival proof
```

This makes the project organic instead of patch-stacked.

## 5. Proposed Stage Name

```text
Stage72.3 - Pre-Stage40 Lineage Recovery and Organic Impact Governance
```

Alternative short name:

```text
Stage72.3 - Foundation Lineage Graph
```

## 6. Proposed Outputs

Stage72.3 should produce the following artifacts.

### 6.1 Foundation Lineage Manifest

```text
manifests/pre_stage40_lineage_manifest.json
```

Purpose:

```text
machine-readable index of Stage01-39 concepts, source files, current anchors, and survival status
```

Suggested schema:

```json
{
  "stage_id": "STAGE22",
  "title": "Node1 Series Arc Control",
  "introduced_concepts": ["series arc", "episode progression", "longform control"],
  "source_evidence": ["knowledge_base/.../stage22_node1_series_arc_control_manifest.json"],
  "current_runtime_anchor": ["src/v1700/ir/scene_intent.py"],
  "survival_status": "PARTIAL",
  "missing_runtime_work": ["season planner", "episode planner", "sequence planner"],
  "required_tests": ["pre_stage40_survival_gate", "longform_planner_gate"]
}
```

### 6.2 Foundation Stage Document

```text
docs/stages/stage_001_039_foundation.md
```

Purpose:

```text
human-readable map of early concepts and whether they are live, partial, deferred, or rejected
```

### 6.3 Concept Survival Matrix

```text
docs/generated/wiki/foundation_lineage_wiki.md
docs/generated/skills/foundation_lineage_skill.md
```

Purpose:

```text
developer-facing and agent-facing summaries of early-stage inheritance
```

### 6.4 Pre-Stage40 Survival Gate

```text
src/v1700/gates/pre_stage40_survival_gate.py
tools/run_pre_stage40_survival_gate.py
tests/test_stage72_3_pre_stage40_survival_gate.py
```

Purpose:

```text
block future releases if essential early-stage concepts disappear from lineage tracking
```

### 6.5 Organic Impact Review Protocol

```text
docs/runbooks/organic_impact_review_protocol.md
manifests/change_impact_review_template.json
```

Purpose:

```text
force every future change to state what it touches, what it inherits, and what it risks breaking
```

Required fields:

```text
change_intent
related_stage_origins
affected_runtime_modules
affected_graph_nodes
affected_tests
node_authority_risks
reveal_leakage_risks
provider_cost_risks
rollback_plan
promotion_decision
```

## 7. Proposed GraphNexus Extensions

Stage72.3 should extend GraphNexus with lineage-aware tools.

```text
src/v1700/graph_nexus/tools/foundation_lineage.py
src/v1700/graph_nexus/tools/concept_impact.py
src/v1700/graph_nexus/tools/survival_matrix.py
src/v1700/graph_nexus/tools/change_review.py
```

### 7.1 Foundation Lineage

Reads Stage01-39 evidence from the knowledge base and emits normalized concept cards.

### 7.2 Concept Impact

Answers:

```text
If we change Node2, which old style/literary quality concepts are affected?
If we implement scene-sequence planning, which Stage22/39 concepts must be preserved?
If we alter provider routing, which Stage10/40/45-60 constraints are touched?
```

### 7.3 Survival Matrix

Classifies each concept:

```text
LIVE_RUNTIME
LIVE_GATE_ONLY
DOCUMENTED_ONLY
PARTIAL
DEFERRED
REJECTED_WITH_REASON
UNKNOWN_NEEDS_REVIEW
```

### 7.4 Change Review

Creates a required review packet before major changes.

This is the project-level version of GitNexus `impact`.

## 8. Initial Concept Groups to Recover

Stage72.3 should not try to restore all Stage01-39 files at once. It should recover by concept group.

Priority 1: Longform generation foundations

```text
Stage21 episode draft export
Stage22 series arc control
Stage39 longform scene-sequence planner
Stage39 temporal continuity
Stage39 emotional pressure valve
```

Reason:

```text
These directly support the user's core goal: a generator that can organically calculate episodes, sequences, and scenes.
```

Priority 2: Literary quality and style foundations

```text
Stage14 Node2 literary quality engine
Stage15 literary depth calibration
Stage23 Node2 style evolution memory
Stage56-57 literary quality/refinement evaluation
Stage71 reader-facing prose renderer
```

Reason:

```text
The user-facing quality of the model is felt through prose, rhythm, emotional indirectness, dialogue taste, and anti-LLM surface control.
```

Priority 3: Governance and boundary foundations

```text
Stage17 authoring review workflow
Stage18 human/agent review console
Stage24 boundary registry
Stage25 release candidate gate
Stage26 boundary-required validations
Stage33 concept validation workbench
```

Reason:

```text
These prevent future patch drift and make promotion decisions auditable.
```

Priority 4: Provider and adapter foundations

```text
Stage10 multi-provider comparison
Stage11 provider execution trace
Stage40 provider route
Stage54 multi-adapter provider routing
Stage58 runtime cost/provider safeguards
```

Reason:

```text
These preserve the local-first and provider-cost-control philosophy.
```

## 9. Governance Rule for Future Development

After Stage72.3, no major feature should be promoted unless it includes:

```text
1. GraphNexus query result
2. GraphNexus context packet
3. GraphNexus impact report
4. affected stage lineage list
5. affected tests/gates list
6. Node authority boundary check
7. provider-cost boundary check
8. rollback or quarantine plan
```

This does not mean development becomes slow. It means future development stops losing old logic.

## 10. Relationship to Stage72.2

Stage72.2 built the tools.

Stage72.3 should use those tools against the project's own historical lineage.

```text
Stage72.2:
GitNexus capability -> GraphNexus operational tools

Stage72.3:
GraphNexus operational tools -> lineage recovery and impact-governed development
```

## 11. Acceptance Criteria

Stage72.3 is complete when:

```text
pre_stage40_lineage_manifest.json exists
stage_001_039_foundation.md exists
at least 20 high-value Stage01-39 concepts are classified
each classified concept has source evidence
each LIVE or PARTIAL concept has a current runtime/test/doc anchor
pre_stage40_survival_gate passes
organic impact review protocol exists
Stage72.2 release gate remains pass
main release gate remains pass
pytest remains green
provider default calls remain 0
Node2 raw reveal access remains 0
```

## 12. Risks and Mitigations

Risk:

```text
Importing too much historical material makes the active repo noisy again.
```

Mitigation:

```text
Do not copy old modules wholesale. Convert them into concept cards, survival matrix entries, and implementation tickets.
```

Risk:

```text
Old concepts may conflict with current clean architecture.
```

Mitigation:

```text
Use concept_impact and shape_check before implementation. Conflicting concepts become deferred or rejected with reason.
```

Risk:

```text
Lineage recovery becomes documentation-only.
```

Mitigation:

```text
Add pre_stage40_survival_gate and require source evidence plus current anchors.
```

## 13. Recommended Decision

Proceed with Stage72.3 before building the next large creative engine feature.

Reason:

```text
The next major feature is likely the longform season/episode/sequence/scene execution engine.
That feature depends heavily on Stage21, Stage22, Stage23, Stage24, Stage26, Stage33, and Stage39 concepts.
If those are not recovered first, the project risks repeating the earlier pattern of solving the present problem while silently breaking inherited logic.
```

## 14. Proposed Roadmap

Phase 0: Baseline Lock

```text
Run Stage72.2 gate
Run release gate
Run pytest
Record GitNexus alias and index status
```

Phase 1: Historical Evidence Scan

```text
Scan knowledge_base/v1650_stage35_critic_comparison_gate
Extract Stage01-39 manifests, reports, tests, and design docs
Create raw evidence index
```

Phase 2: Concept Card Normalization

```text
Group old artifacts by concept
Create normalized concept cards
Assign source evidence and stage origin
```

Phase 3: Current Anchor Mapping

```text
Map each concept to current src/docs/tests/manifests
Classify LIVE, PARTIAL, DOCUMENTED_ONLY, DEFERRED, REJECTED, UNKNOWN
```

Phase 4: Impact Governance

```text
Implement change_impact_review_template
Implement organic impact review protocol
Implement pre_stage40_survival_gate
```

Phase 5: Developer Handoff

```text
Update STAGE_INDEX
Update generated wiki/skills
Write Stage72.3 developer handoff report
Package full integrated repository only after gates pass
```

