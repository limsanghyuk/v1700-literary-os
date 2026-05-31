# Page10 Design Outline

Status: draft
Created: 2026-05-29
Page: Page10
Stage range: Stage195~Stage200

## Name

Story Repository / Story Bible / Codex / Context Preview

## Mission

Page10 creates the story repository substrate for later pages.

It prepares story source records, entity records, relation records, context packets, and preview packets.

## Stage plan

- Stage195: Project Manifest and Story Bible Contract
- Stage196: Entity Registry and Lore Cards
- Stage197: Mention Timeline, Alias Index, Relation Graph
- Stage198: Context Packet Builder
- Stage199: Prompt Preview and Redaction Gate
- Stage200: Page10 Release Seal

## Core records

- ProjectManifest
- StoryBiblePacket
- StoryRepositoryIndex
- EntityCard
- AliasIndex
- MentionTimelineRecord
- RelationEdge
- ContextPacket
- PromptPreviewPacket

## Required rule

Every derived record keeps a source reference.

Every context packet states its consumer and projection status.

Every preview packet states its redaction status.

## Handoff

Page11 receives repository packets for writer surface and candidate work.

Page12 receives repository packets for feature extraction and advisory evaluation.

## Exit criteria

- Repository contracts exist.
- Entity and relation records exist.
- Context packet contract exists.
- Prompt preview contract exists.
- Page11 and Page12 handoffs are defined.
