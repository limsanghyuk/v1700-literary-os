# Canonical Record Store and RAG Blueprint

Status: PROPOSED_SCAFFOLD
Created: 2026-06-10
Scope: database and retrieval planning for V1700 Writer IDE and MultiWork expansion

## 1. Purpose

Define the long-term database and retrieval architecture for V1700 without opening live provider RAG or write-enabled memory.

## 2. Data layer

```text
RawVault
CanonicalRecordStore
GraphStore
RetrievalIndex
FormulaSignalStore
AgentAuditStore
ReviewApprovalStore
ReleaseEvidenceStore
```

## 3. Canonical record families

```text
WorkRecord
CharacterRecord
WorldRuleRecord
RelationGraphRecord
TimelineEventRecord
SceneBlueprintRecord
CausalityMatrixRecord
PayoffDebtRecord
DialogueFunctionRecord
FormulaSignalRecord
AgentActionRecord
HumanApprovalRecord
ReleaseEvidenceRecord
```

## 4. RAG modes

```text
SafeSurfaceRAG: approved summaries and non-spoiler context only
ProtectedAuthorRAG: author-only notes and reveal-bearing records, local only
```

## 5. Initial retrieval score

```text
RetrievalScore =
  0.35 * BM25
+ 0.25 * GraphProximity
+ 0.20 * RecencyWithinProject
+ 0.10 * CharacterOverlap
+ 0.10 * ScenePhaseMatch
- LeakagePenalty
- LicensePenalty
```

## 6. Boundary invariants

```text
raw manuscript is not provider input
raw reveal access is logged
cross-work retrieval requires license edge
memory write is disabled by default
vector index is optional and never source of authority
canonical record store remains source of truth
```

## 7. Build order

```text
1. record contracts
2. JSON fixtures
3. local read-only store
4. deterministic query/ranking
5. leakage and license boundary checks
6. graph neighborhood retrieval
7. optional vector index
8. optional live RAG only after separate gate
```

## 8. Next implementation candidate

```text
docs/contracts/canonical_record_store_contract.md
docs/contracts/rag_retrieval_packet_contract.md
fixtures/canonical_record_store/minimum_records.json
fixtures/rag/minimum_retrieval_cases.json
tools/canonical_record_store_validator.py
```
