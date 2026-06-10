# V1700 Page10 Proposal — Story Repository / Story Bible / Codex / Context Preview

Status: detailed proposal draft
Created: 2026-05-29
Stage range: Stage195~Stage200
Previous dependency: Page09 PASS_WITH_APPROVED_WARNINGS

## 1. Mission

Page10 builds the structured story substrate required before writer surface, draft candidate, EAT8D extraction, Story Patch, Narrative PR, or Narrative IDE work begins.

Page10 is not a prose generation page and not a patch page. It turns project source material into typed, traceable, boundary-aware repository packets.

## 2. Required inheritance

Page10 inherits:

- Page08 branchpoint map and GitNexus evidence
- Stage187 inheritance contract
- Stage189 Formula / Logic Ledger v2
- Page09 feature taxonomy and feature-to-contract mapping
- Page09 approved warnings

Page10 must preserve:

- Stage185 remains local-known
- 8D remains advisory
- story source must be provenance-traced
- context preview must be safe projection
- unmapped features remain unavailable

## 3. Chief Principal Architect review

The architect defines Page10 as the substrate page. The system must not build Story Patch or Narrative PR on unstable notes. Story Bible, Codex, entity registry, relation graph, and context packets must become the common source layer for later pages.

Risks:

- Story Bible stays as loose notes
- entity aliases diverge
- relation graph lacks evidence
- context preview exposes hidden reveal material
- Page11 or Page12 invents a different source shape

Architect amendment:

- Page10 must create a single repository contract for all future story-state readers.

## 4. Chief Principal Compiler Engineer review

The compiler engineer requires Page10 to be machine-readable. Repository data must compile into records and packets.

Required contracts:

- ProjectManifest
- StoryBiblePacket
- StoryRepositoryIndex
- EntityCard
- AliasIndex
- MentionTimelineRecord
- RelationEdge
- ContextPacket
- PromptPreviewPacket
- RedactionRule
- RevealBoundaryRule

Compiler amendment:

- Every context packet must declare source ids, redaction status, and intended consumer.

## 5. Chief System Principal Engineer review

The system principal engineer focuses on handoff. Page10 must give Page11 a safe writing surface input and Page12 a stable analysis input.

Operational concerns:

- Page10 must not become an archive only.
- Page10 must define output paths and acceptance criteria.
- Page10 must carry Page09 warnings forward.
- Page10 must not close Stage185 hub authority.

System amendment:

- Page10 release seal must block Page11 if repository packets are missing provenance or reveal-boundary state.

## 6. Expert consensus

The three experts agree:

- Page10 builds the Story Repository substrate.
- Page10 compiles story material into typed packets.
- Page10 does not write manuscript state.
- Page10 does not generate final prose.
- Page10 hands safe repository packets to Page11 and Page12.

## 7. Stage plan

Stage195 — Project Manifest & Story Bible Contract
Stage196 — Entity Registry / Character / Location / Lore Cards
Stage197 — Mention Timeline / Alias Index / Relation Graph
Stage198 — Context Packet Builder
Stage199 — Prompt Preview / Redaction Gate
Stage200 — Page10 Release Seal

## 8. Acceptance criteria

Page10 is accepted only if:

1. ProjectManifest and StoryBiblePacket are defined.
2. Entity registry records source references.
3. Alias and relation records are represented.
4. Context packets include provenance and intended consumer.
5. Prompt preview includes redaction state.
6. Reveal boundary is not bypassed.
7. Page09 mapping is inherited.
8. Page11 handoff is defined.
9. Page12 feature extraction input is anticipated.
10. StoryPatch, Narrative PR, and final manuscript generation remain outside Page10.

## 9. Next evolution direction

After Page10, Page11 should implement Writer Surface / Narrative IDE Contract / Draft Candidate Sandbox using Page10 repository packets.
