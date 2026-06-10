# V1700 Page11 Proposal — Writer Surface / Narrative IDE Contract / Draft Candidate Sandbox

Status: detailed proposal draft
Created: 2026-05-29
Stage range: Stage201~Stage206
Previous dependency: Page10 design authority

## 1. Mission

Page11 defines the first writer-facing surface after Page10 repository substrate.

It introduces manuscript unit contracts, scene and beat nodes, revision snapshots, comments, draft candidates, and candidate evidence reports.

Page11 does not merge drafts into final story state. It prepares a safe candidate surface for later review and approval pages.

## 2. Required inheritance

Page11 inherits:

- Page08 lineage authority
- Page09 feature mapping
- Page10 repository packet contracts
- candidate output is not committed manuscript
- review is required before commit path

## 3. Chief Principal Architect review

The architect defines Page11 as the controlled writer surface. The user must be able to see drafts, comments, candidate evidence, and scene structure without losing the separation between proposal and committed story state.

Architectural risks:

- UI surface becomes story authority
- candidate text becomes committed state
- scene nodes diverge from repository packets
- IDE contract grows before core state is stable

Architectural amendment:

- Page11 must distinguish manuscript surface, candidate surface, and committed state.

## 4. Chief Principal Compiler Engineer review

The compiler engineer requires Page11 to define machine contracts for writer-facing units.

Required contracts:

- ManuscriptDocument
- ChapterNode
- SceneNode
- BeatNode
- RevisionSnapshot
- CommentThread
- DraftCandidate
- CandidateEvidenceReport
- NarrativeIDEPanelContract

Compiler risks:

- candidate missing source context
- revision missing snapshot
- comment not anchored to a unit
- ranking without evidence

Compiler amendment:

- Every candidate must include source packet id, generation context id, and evidence summary.

## 5. Chief System Principal Engineer review

The system principal engineer requires Page11 to remain operationally modest.

Page11 should not become the full Narrative IDE product. It should define the contract for later UI expansion and the safe draft candidate sandbox.

System risks:

- Page11 expands into Page13 approval system
- Page11 mutates canon before Page13 exists
- Page11 ignores Page10 repository packets

System amendment:

- Page11 must produce handoff records for Page12 and Page13 but not perform Page13 actions.

## 6. Expert consensus

The three experts agree:

- Page11 is the writer surface and draft candidate sandbox.
- It consumes Page10 repository packets.
- It creates visible manuscript and scene surfaces.
- It can create candidates, but candidates are not commits.
- It prepares future review and approval paths without executing them.

## 7. Stage plan

Stage201 — Manuscript Document Contract
Stage202 — Chapter / Scene / Beat Node Model
Stage203 — Revision Snapshot / Comment Layer
Stage204 — Provider Sandbox Draft Candidate
Stage205 — Candidate Ranking / Evidence Report
Stage206 — Page11 Release Seal

## 8. Acceptance criteria

Page11 is accepted only if:

1. ManuscriptDocument is defined.
2. Chapter, Scene, and Beat nodes are defined.
3. Revision snapshots are defined.
4. Comment threads are anchored.
5. DraftCandidate is separate from committed state.
6. Candidate evidence report exists.
7. Page10 repository packet dependency is explicit.
8. Page12 and Page13 handoffs are defined.
9. Page11 does not merge StoryPatch or Narrative PR.
10. Page11 does not claim final manuscript authority.

## 9. Next evolution direction

After Page11, Page12 should evaluate scene and candidate evidence through EAT8D feature extraction and graph advisory.
