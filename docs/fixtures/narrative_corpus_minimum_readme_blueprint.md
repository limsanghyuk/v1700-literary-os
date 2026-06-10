# Narrative Corpus Minimum README Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: README structure for future metadata-only narrative corpus fixture
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This document defines the README structure for the future minimum narrative corpus fixture.

The fixture is metadata-only. It must not include unlicensed full-text scripts, books, subtitles, or other protected expressive content.

## 2. Future fixture location

Proposed future path:

```text
fixtures/narrative_corpus_minimum/README.md
fixtures/narrative_corpus_minimum/fixture.json
fixtures/narrative_corpus_minimum/source_review.md
fixtures/narrative_corpus_minimum/schema_validation_report.md
```

## 3. README required sections

The future README must include:

```text
1. Fixture purpose
2. Source policy summary
3. Allowed source classes
4. Disallowed source classes
5. Record inventory
6. Schema coverage
7. Formula signal coverage
8. Value Proof compatibility
9. LearnableCritic compatibility
10. Writer IDE compatibility
11. Known limitations
12. Review status
```

## 4. Minimum record inventory

The README should declare counts for:

```text
WorkRecord
DramaEntryRecord
CorePhilosophyRecord
CharacterRecord
KeyObjectRecord
CausalityMatrixRecord
EpisodeOrChapterRecord
SceneBlueprintRecord
DialogueFunctionRecord
CriticThresholdRecord
RelationshipGraphRecord
FormulaSignalRecord
```

## 5. Source policy summary

The README must state:

```text
This fixture stores structured metadata and analysis records only.
It does not store unlicensed full-text narrative material.
Every record must include source_class, rights_status, and provenance_ref.
```

## 6. Schema coverage checklist

The README should include a checklist:

```text
[ ] all records include record_id
[ ] all records include record_type
[ ] all records include source_class
[ ] all records include rights_status
[ ] all records include provenance_ref
[ ] scene metadata includes emotional transition tags
[ ] causality metadata includes trigger / resolution / residue summaries
[ ] formula signals link to source record ids
```

## 7. Fixture readiness states

```text
DRAFT
SOURCE_REVIEW_READY
SCHEMA_VALIDATED
FORMULA_SIGNAL_VALIDATED
VALUE_PROOF_READY
LEARNABLE_CRITIC_READY
REJECTED
```

## 8. Blocking failures

- source_class missing
- rights_status missing
- provenance_ref missing
- restricted full text included
- formula signal without source record
- unknown source used outside quarantine
- schema validation report missing
- source review report missing

## 9. Final decision

The README must make the fixture auditable before any future Page18 Option B implementation uses it.
