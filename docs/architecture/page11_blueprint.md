# Page11 Blueprint

Status: draft
Created: 2026-05-29
Page: Page11
Stage range: Stage201~Stage206

## Name

Writer Surface / Narrative IDE Contract / Draft Candidate Sandbox

## Mission

Page11 defines the writer-facing surface and the draft candidate sandbox.

It consumes Page10 repository packets and creates manuscript units, scene units, comments, snapshots, and candidate records.

## Stage plan

- Stage201: Manuscript Document Contract
- Stage202: Chapter, Scene, and Beat Node Model
- Stage203: Revision Snapshot and Comment Layer
- Stage204: Draft Candidate Sandbox
- Stage205: Candidate Evidence Report
- Stage206: Page11 Release Seal

## Core records

- ManuscriptDocument
- ChapterNode
- SceneNode
- BeatNode
- RevisionSnapshot
- CommentThread
- DraftCandidate
- CandidateEvidenceReport
- NarrativeIDEPanelContract

## Required rule

DraftCandidate is not committed story state.

Every candidate must reference its source packet and evidence summary.

Every comment must anchor to a manuscript, scene, beat, or candidate unit.

## Handoff

Page12 receives candidate and scene evidence for evaluation.

Page13 receives future review and approval preconditions, but Page11 does not perform merge actions.

## Exit criteria

- Writer surface contracts exist.
- Candidate sandbox contract exists.
- Candidate evidence report exists.
- Page10 dependency is explicit.
- Page12 and Page13 handoffs are defined.
