# Literary Generation Next Roadmap Priority Proposal

Status: planning proposal loaded
Created: 2026-06-17
Branch: corpus-absorption-formula-bridge-handoff
Baseline: stage242
Scope: candidate Page18 to Page24 planning only

## Purpose

This proposal upgrades the next roadmap from a generic LLM application stack into a domain-native literary generation operating system.

The design does not open Page18, does not create Stage243, and does not start generation experiments. It records the priority order and entry gates required before later pages can be implemented.

## External Stack Reference

LangChain provides an agent harness around model, tools, prompt, and middleware.
LangGraph provides low-level orchestration for long-running, stateful agents.
LangSmith provides tracing, evaluation, monitoring, prompt management, and deployment support.

V1700 should not copy this stack directly. V1700 should absorb the useful responsibilities into a literary authority system:

```text
LangChain role -> Literary Generation Harness
LangGraph role -> Narrative State and Authority Graph
LangSmith role -> Evidence Ledger and Value Proof Observatory
```

## Current V1700 Position

The current branch already contains:

```text
metadata-only corpus absorption
formula signal bridge
formula signal store
learnable critic audit fixture
writer IDE advisory consumer
Value Proof guidance scaffold
Value Proof preregistration scaffold
Value Proof blind evaluator scaffold
Page18 readiness precheck blocked state
```

The current blocker is not writing or pushing. The blocker is missing generated Value Proof reports.

## Priority Model

Prioritization uses four weights:

```text
P1 = unlocks blocked roadmap gate
P2 = directly improves literary generation quality
P3 = reduces safety, copyright, or authority risk
P4 = creates reusable runtime infrastructure
```

## Ranked Priorities

### Priority 0 — Evidence Completion

Purpose: finish the local proof chain already required by the current precheck.

Required outputs:

```text
value_proof_arm_b_guidance_surface_report.json
value_proof_arm_b_preregistration_packet_report.json
value_proof_blind_evaluator_packet_report.json
```

Exit gate:

```text
all three reports exist
focused tests pass
release gate passes
Page18 readiness precheck is rerun
```

### Priority 1 — Page18 Candidate: Controlled Literary Generation Boundary

Purpose: define the first safe generation boundary without turning it into production runtime.

Core objects:

```text
LiteraryGenerationRequest
GenerationContextPacket
NarrativeConstraintPacket
ProviderExecutionPolicy
OutputCaptureSchema
CanonicalMutationBlocker
```

Exit gate:

```text
provider policy chosen
output capture schema frozen
raw corpus text blocked
canonical mutation blocked
human approval boundary present
```

### Priority 2 — Page19 Candidate: Narrative State Graph Runtime

Purpose: replace generic agent state with a literary state graph.

Core objects:

```text
NarrativeStateGraph
SceneNode
CharacterArcNode
ConflictArcNode
ForeshadowingNode
EmotionalMomentumEdge
ContinuityConstraintEdge
```

Exit gate:

```text
graph state can be serialized
scene continuity checks pass
character arc continuity checks pass
no hidden memory writes
```

### Priority 3 — Page20 Candidate: Literary Evaluation and Value Proof Engine

Purpose: run controlled comparison without leaking arm labels or changing thresholds after outputs.

Core objects:

```text
EvaluatorRubric
BlindEvaluationAssignment
PairwisePreferenceRecord
ContinuityScoreRecord
StyleCoherenceScoreRecord
EffectSizeReport
ValueProofConclusionRecord
```

Exit gate:

```text
blind packets valid
rubric frozen
outputs captured once
results mapped only after evaluation
statistics report created
```

### Priority 4 — Page21 Candidate: Writer Studio Product Surface

Purpose: convert advisory records and evaluation results into usable writer workflow.

Core objects:

```text
WriterWorkbenchSession
SceneRevisionBoard
AdvisoryDiffCard
ApprovalDecisionRecord
ManuscriptPatchProposal
ExportBoundaryRecord
```

Exit gate:

```text
writer can inspect suggestions
approval is explicit
canonical manuscript is not mutated automatically
export boundary is recorded
```

### Priority 5 — Page22 Candidate: Safe Personalization and Memory

Purpose: add bounded personalization without hidden training or uncontrolled memory.

Core objects:

```text
WriterPreferenceProfile
StylePreferenceVector
MemoryConsentRecord
RollbackablePersonalizationSnapshot
PersonalizationAuditLog
```

Exit gate:

```text
consent exists
profile is inspectable
rollback works
hidden memory is blocked
runtime training remains disabled unless separately approved
```

### Priority 6 — Page23 Candidate: Plugin and Tool Capability Layer

Purpose: add external tools only through declared literary capabilities.

Core objects:

```text
PluginManifest
LiteraryCapabilityDeclaration
ToolSandboxPolicy
FixturePack
PluginReleaseGate
```

Exit gate:

```text
every tool has declared capability
fixture tests pass
no raw corpus exfiltration
no unsupervised write action
```

### Priority 7 — Page24 Candidate: Multi-Agent Literary Studio Runtime

Purpose: coordinate specialized literary agents under authority boundaries.

Core agents:

```text
PlannerAgent
SceneWriterAgent
ContinuityEditorAgent
CharacterArcCritic
StyleEditorAgent
ValueProofAuditor
```

Exit gate:

```text
all agents are capability-scoped
handoff records exist
no hidden scratchpad authority
no direct canonical mutation
human approval required for manuscript change
```

## Final Priority Decision

The next immediate work is not another blueprint. It is:

```text
1. run local Value Proof chain
2. commit the three generated reports
3. rerun Page18 readiness precheck
4. only then prepare Page18 candidate implementation plan
```

The roadmap above is loaded as planning priority, not as an opened implementation stage.
