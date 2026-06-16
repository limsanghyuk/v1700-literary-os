# Script Corpus To V1700 Data Pipeline

## Goal

Build a V1700-ready corpus layer that supports retrieval and learning without pushing raw copyrighted script text into the repository.

## Pipeline

```text
local script corpus
-> source inventory
-> scene/chunk structural scan
-> feature aggregation
-> canonical work registry
-> rag index registry
-> learning signal registry
-> formula signal / evaluation / writer IDE integration
```

## Storage Layers

### 1. Raw Source Layer

- local-only
- includes txt, hwp, pdf, doc, jsonl scene bodies, raw vectors

### 2. Canonical Metadata Layer

- repository-safe
- work counts, parse methods, QC flags, feature means, index readiness

### 3. Retrieval Layer

- ChromaDB or equivalent
- advisory only
- connected through `rag_index_registry`

### 4. Learning Layer

- derived from feature aggregates
- connected through `learning_signal_registry`
- can later feed EAT8D, Formula Signal, Narrative State Tensor, and critic loops

## Safety Boundary

- repo outputs must remain metadata-only
- raw scenes and dialogues must never be materialized into committed JSON artifacts
- canonical answers must be grounded in safe metadata, not vector hits alone
