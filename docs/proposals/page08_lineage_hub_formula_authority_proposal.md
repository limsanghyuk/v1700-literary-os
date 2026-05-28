# V1700 Page08 Proposal — Lineage / Hub / Formula Authority

Status: detailed proposal draft
Created: 2026-05-28
Roadmap: V1700 Page08~Page17 Commercial Absorption & Writer Studio Evolution Roadmap
Stage range: Stage186~Stage190
Next implementation branch: stage186-page08-branchpoint-map

## 0. Purpose

Page08 is the first mandatory page of the new Page08~Page17 evolution. It must run before commercial absorption, Codex-style Narrative Agent work, Story Patch Engine, Narrative IDE integration, or MultiWork expansion.

The goal is simple:

```text
Do not let the future roadmap quietly sever the past system.
```

V1700 has reached a point where adding new features is less dangerous than adding them without lineage control. Page08 therefore creates the authority layer that tells future stages what they must inherit, what they may extend, what they must not override, and what they may deprecate only with successor trace.

## 1. Current context

The known authority context is:

```text
Hub official line: Stage184 Page07 Release Seal
Known local next line: Stage185 NarrativeStateTensor 8D Advisory Absorption
New roadmap: Page08~Page17 Commercial Absorption & Writer Studio Evolution Roadmap
Uploaded proposal absorption: Codex-style Narrative Agent + Cursor-style Narrative IDE addendum
```

Stage185 already established that NarrativeStateTensor 8D values are advisory, while evidence integrity is gated. The uploaded proposal correctly extends that idea toward EAT8D Feature Schema, Scene-to-8D Extractor, Story Patch, Narrative Gate Runner v2, Narrative PR, and Writer Review. However, those concepts must not start at Stage186 because Stage186 must first audit inheritance.

## 2. Page08 mission

Page08 must produce four authority layers:

```text
1. Branchpoint Map
2. Inheritance Contract
3. Hub Authority Reconciliation
4. Formula / Logic Ledger v2
```

The page ends with:

```text
Stage190 — Page08 Release Seal
```

Page08 is successful only if every future Page09~Page17 stage can answer:

```text
What do I inherit?
What may I extend?
What must I not override?
What may I deprecate only with successor trace?
Which formulas, gates, manifests, and release evidence define my authority?
```

## 3. Expert review roles

This proposal uses three internal expert viewpoints:

```text
1. Chief Principal Architect
2. Chief Principal Compiler Engineer
3. Chief System Principal Engineer
```

The architect focuses on system shape and future page continuity. The compiler engineer focuses on machine-readable contracts, ledgers, runners, and validation. The system principal engineer manages risk, release authority, and next evolution constraints.

## 4. Chief Principal Architect review

### 4.1 Architect position

The architect argues that Page08 must be treated as the foundation of the entire second roadmap. The Page08~Page17 plan now contains many powerful future concepts:

```text
Story Repository
Narrative IDE
EAT8D Feature Extraction
Narrative Gate Runner v2
Story Patch
Narrative PR
Human Review
MultiWork
Plugin System
Learning Audit
Multi-Agent Creative Studio
```

Without Page08, each concept may be implemented as a strong isolated subsystem while weakening older V1700 principles.

### 4.2 Architect concern

The biggest architectural risk is not technical failure. It is architectural drift:

```text
A future Page12 may treat 8D as hard literary judgment.
A future Page13 may merge StoryPatch without writer approval.
A future Page14 may mix project memory before isolation.
A future Page17 may enable learning before audit and rollback.
```

Such changes would appear as progress while breaking the lineage.

### 4.3 Architect requirement

The architect requires a branchpoint map that is readable by both humans and tools. Each branchpoint must be classified as one of:

```text
CORE
GATED
ADVISORY
LEGACY
DEPRECATED
REPLACED_WITH_TRACE
```

### 4.4 Architect design amendment

The architect proposes that Page08 should define an inheritance declaration template used by every future page:

```text
must_inherit:
  - inherited invariant
may_extend:
  - permitted extension
must_not_override:
  - forbidden regression
may_deprecate_only_with_successor_trace:
  - old logic and successor mapping
```

This template becomes mandatory in Page09~Page17 proposals and blueprints.

## 5. Chief Principal Compiler Engineer review

### 5.1 Compiler position

The compiler engineer argues that Page08 must not be a prose-only historical document. It must compile the lineage into machine-readable authority.

The key compiler model is:

```text
Historical stage evidence
-> BranchpointRecord
-> InheritanceContract
-> FormulaLogicLedgerEntry
-> PageSealPrecondition
-> ReleaseGateInput
```

### 5.2 Compiler concern

The main problem is ambiguity. If Page08 only says “preserve legacy,” later code cannot enforce it. The compiler engineer therefore rejects vague inheritance and requires explicit data structures.

### 5.3 Compiler required data structures

```text
BranchpointRecord
CoreInvariant
ForbiddenRegressionRule
SuccessorRequirement
SuccessorTrace
StageAuthorityRecord
HubAuthorityRecord
FormulaLogicLedgerEntry
InheritanceContract
PageSealPrecondition
Page08GateReport
```

### 5.4 Compiler validation model

The compiler engineer proposes five executable validators:

```text
run_stage186_branchpoint_map_builder.py
run_stage187_inheritance_contract_gate.py
run_stage188_hub_authority_reconciliation.py
run_stage189_formula_logic_ledger_v2.py
run_stage190_page08_release_seal.py
```

Each validator must produce a release/current report.

### 5.5 Compiler non-negotiable rule

The Formula / Logic Ledger must not record formulas only. It must also track logic status:

```text
formula
contract
gate
runner
fixture
manifest
release report
authority status
successor trace
```

## 6. Chief System Principal Engineer review

### 6.1 Principal position

The system principal engineer agrees with the architect and compiler but adds operational discipline. Page08 must not become a large philosophical archive. It must answer release questions:

```text
Can the next stage safely begin?
What must it inherit?
What would make it unsafe?
Which hub evidence defines the active authority?
Which local evidence is known but not hub-closed?
```

### 6.2 Principal risk register

| Risk | Impact | Required mitigation |
|---|---|---|
| Stage185 local line mistaken as hub-closed | authority confusion | HubAuthorityRecord distinguishes hub official and local known evidence |
| Uploaded proposal Stage186~195 numbers used directly | stage collision | Page08 keeps Stage186~190 for lineage authority |
| Branchpoints listed without invariants | unenforceable history | each BranchpointRecord requires core_invariants |
| New pages omit inheritance declarations | roadmap drift | inheritance gate blocks future page seal |
| 8D becomes hard literary gate | creative rigidity | 8D advisory invariant recorded as CORE/ADVISORY hybrid |
| GIG blocks intended mystery | false negative | exemption classifier required before hard promotion |
| StoryPatch mutates main story before approval | author control failure | Page13 must inherit approval-before-merge invariant |
| MultiWork shares project state too early | project contamination | Page14 must inherit isolation-before-sharing invariant |
| learning changes runtime behavior without audit | non-reproducible release | Page17 must inherit audit-first learning invariant |

### 6.3 Principal additional requirement

Page08 must produce a local-Codex execution guide. The reason is practical: a new ChatGPT session or another local environment must know exactly which documents to read before implementation.

### 6.4 Principal release policy

Page08 may be documentation-heavy, but it should still follow V1700 release discipline:

```text
proposal
blueprint
manifest
runner plan
release gate plan
evidence report plan
next-chat handoff
hub PR closure
```

## 7. Three-expert debate

### 7.1 Architect vs Compiler

The architect wants Page08 to preserve the grand lineage. The compiler warns that broad lineage without schemas cannot be enforced. The compromise is:

```text
human-readable branchpoint map
+ machine-readable branchpoint manifest
+ executable inheritance gate
```

### 7.2 Compiler vs Principal

The compiler wants detailed validation for every formula and stage. The principal warns that Page08 cannot rebuild the entire repository. The compromise is:

```text
Page08 records authority and required successor traces.
It does not re-implement all previous stages.
It verifies references, classifications, and invariants.
```

### 7.3 Architect vs Principal

The architect wants Page08 to include all major history. The principal warns that too many legacy items may freeze future evolution. The compromise is the status taxonomy:

```text
CORE: must survive
GATED: can activate only under conditions
ADVISORY: informs but does not block literary outcomes
LEGACY: preserved as design history
DEPRECATED: retired with reason
REPLACED_WITH_TRACE: replaced but mapped to successor
```

## 8. Final consensus

The three experts agree:

```text
Page08 is not optional.
Page08 must precede Page09 commercial absorption.
Page08 must create both human-readable and machine-readable lineage authority.
Page08 must distinguish hub-official authority from local-known evidence.
Page08 must preserve Stage185 8D as advisory and prevent accidental hard promotion.
Page08 must prevent future pages from silently weakening Provider-Zero, Node2 safety, non-mutating ASD, audit-first learning, project isolation, and license boundaries.
```

## 9. Final Page08 stage plan

```text
Stage186 — Branchpoint Map Builder
Stage187 — Inheritance Contract Gate
Stage188 — Hub Authority Reconciliation
Stage189 — Formula / Logic Ledger v2
Stage190 — Page08 Release Seal
```

### Stage186 — Branchpoint Map Builder

Goal:

```text
Convert V1700's major lineage branchpoints into a human-readable map and machine-readable manifest.
```

Outputs:

```text
docs/lineage/v1700_branchpoint_map.md
manifests/stage186_branchpoint_manifest.json
release/current/stage186_branchpoint_map_report.json
```

### Stage187 — Inheritance Contract Gate

Goal:

```text
Define and validate the inheritance declaration required for all future stages and pages.
```

Outputs:

```text
manifests/stage187_inheritance_contract.json
release/current/stage187_inheritance_contract_gate_report.json
```

### Stage188 — Hub Authority Reconciliation

Goal:

```text
Record which authority is hub official, which authority is local known evidence, and which work requires later closure.
```

Outputs:

```text
manifests/stage188_hub_authority_reconciliation.json
release/current/stage188_hub_authority_reconciliation_report.json
```

### Stage189 — Formula / Logic Ledger v2

Goal:

```text
Create a ledger for formulas, logic contracts, gates, runners, fixtures, manifests, and release authority states.
```

Outputs:

```text
manifests/stage189_formula_logic_ledger_v2.json
manifests/stage189_formula_status_matrix.json
release/current/stage189_formula_logic_ledger_report.json
```

### Stage190 — Page08 Release Seal

Goal:

```text
Seal Page08 as the authority base for Page09~Page17.
```

Outputs:

```text
docs/development/page08_next_chat_handoff.md
release/current/stage190_page08_release_seal_report.json
release/current/page08_release_gate_report.json
```

## 10. Page08 acceptance criteria

Page08 is accepted only if:

```text
1. Branchpoint map exists.
2. Branchpoint manifest exists.
3. Each CORE branchpoint has at least one invariant.
4. Each future page has an inheritance declaration requirement.
5. Hub authority and local-known evidence are separated.
6. Formula / Logic Ledger v2 includes formulas, contracts, gates, runners, fixtures, manifests, and release reports.
7. Stage185 8D advisory principle is preserved.
8. Uploaded Codex / Narrative IDE proposal is mapped without using its conflicting stage numbers.
9. Page09 is blocked until Page08 seal passes.
10. Local Codex execution guide exists.
```

## 11. Next evolution direction after Page08

The system principal engineer recommends this direction:

```text
Page09 should not merely classify commercial tools.
Page09 should encode Codex-first policy as an authority rule.
```

The reason is that the uploaded proposal showed a strong implementation path:

```text
Story Repository
-> EAT8D Feature Schema
-> Scene-to-8D Extractor
-> Story Patch
-> Narrative Gate Runner v2
-> Narrative PR
-> Narrative IDE
```

Page09 should formally declare that Page10~Page13 are the Codex-style Narrative Agent Core path, while Cursor-style Narrative IDE becomes a surface and integration layer built on top of that core.

## 12. Final conclusion

Page08 is the roadmap's constitutional lock. It does not build Story Patch, Narrative PR, or Narrative IDE yet. It creates the authority conditions under which those future systems can be built without breaking V1700's lineage.

The final expert consensus is:

```text
Build Page08 first.
Treat lineage as executable authority.
Then allow Page09~Page17 to evolve commercially and agentically without severing the past.
```
