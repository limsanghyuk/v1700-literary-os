# Narrative Corpus Source Policy

Status: policy draft
Created: 2026-06-07
Scope: narrative corpus planning and source classification
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This policy defines how V1700 may classify, store, and use narrative corpus sources.

It is designed for metadata and structured analysis records, not uncontrolled copyrighted full-text ingestion.

## 2. Source classes

### 2.1 USER_PROVIDED_STRUCTURED_ANALYSIS_DB

Definition:

Structured analysis records provided by the user, such as K-Drama Master DB and Cinematic Sovereign DB row dumps.

Allowed use:

- schema design
- metadata analysis
- formula-to-corpus mapping
- value proof fixture planning
- LearnableCritic calibration planning

Restrictions:

- do not assume underlying raw source rights
- preserve provenance and user-provided status
- do not redistribute as raw commercial dataset without separate decision

### 2.2 USER_OWNED_SOURCE

Definition:

Works or analysis records owned by the user or explicitly licensed to the project.

Allowed use:

- full analysis
- controlled experiments
- training or calibration if explicitly approved

Required:

- ownership or license note
- permission scope
- removal policy

### 2.3 PUBLIC_DOMAIN_SOURCE

Definition:

Works confirmed to be public domain in the relevant jurisdiction.

Allowed use:

- analysis
- metadata extraction
- controlled corpus fixture

Required:

- jurisdiction note
- public-domain basis

### 2.4 LICENSED_SOURCE

Definition:

Works available under a license permitting the intended use.

Required:

- license identifier
- permitted use scope
- attribution requirement
- redistribution restriction

### 2.5 METADATA_ONLY_ANALYSIS_RECORD

Definition:

Records that describe narrative structure without storing full copyrighted expression.

Examples:

- title
- genre
- theme tags
- scene function
- conflict axis
- character arc summary
- emotional transition
- audience signal summary

Allowed use:

- corpus database
- search
- critic calibration planning
- value proof metadata

### 2.6 RESTRICTED_COPYRIGHTED_FULL_TEXT

Definition:

Full scripts, novels, episodes, subtitles, or copyrighted text without explicit permission.

Default decision:

```text
NOT_ALLOWED_FOR_INGESTION
```

Allowed only if:

- explicit license or ownership exists
- usage scope is documented
- storage and access boundaries are approved

### 2.7 UNKNOWN_OR_UNRESOLVED_SOURCE

Definition:

Source rights or provenance is unclear.

Default decision:

```text
QUARANTINE
```

Allowed use:

- none except source review

## 3. Required source fields

Every corpus record must include:

```text
source_class
source_name
provenance_ref
rights_status
allowed_use_scope
restriction_notes
created_by_or_provided_by
review_status
```

## 4. Permitted storage model

Allowed:

- structured metadata
- user-provided analysis records
- schema fields
- summaries where permitted
- tags and numeric signals
- provenance references

Not allowed by default:

- uncontrolled full-text scraping
- unlicensed script ingestion
- unlicensed subtitle ingestion
- bulk copying of copyrighted works
- hidden training data without source class

## 5. Uploaded database handling

The uploaded Master DB files are classified as:

```text
USER_PROVIDED_STRUCTURED_ANALYSIS_DB
```

They may be used as schema seeds for:

- DramaEntryRecord
- CorePhilosophyRecord
- CharacterRecord
- CausalityMatrixRecord
- SceneBlueprintRecord
- CriticThresholdRecord

But the underlying works referenced by those records must still be treated according to their source rights.

## 6. Integration with Value Proof

Value Proof experiments may use corpus records only if:

- source class is allowed
- prompt material does not include restricted full text
- provenance is recorded
- experiment preregistration references the source policy

## 7. Integration with LearnableCritic

LearnableCritic calibration may use corpus-derived signals only if:

- source class is allowed
- coefficient changes record source signal
- rollback is possible
- no hidden preference update occurs

## 8. Review statuses

Every source should be marked:

- DRAFT
- REVIEWED_ALLOWED
- REVIEWED_RESTRICTED
- QUARANTINED
- REMOVED

## 9. Blocking failures

- source_class missing
- rights_status missing
- full text stored under metadata-only label
- unknown source used in value proof
- restricted source used for calibration without approval
- provenance removed

## 10. Final policy

V1700 must build a rights-aware narrative corpus.

The project may use structured analysis records and metadata, but must not silently ingest copyrighted full text.
