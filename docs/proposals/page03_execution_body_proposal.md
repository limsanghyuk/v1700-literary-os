# Page03 Consensus Proposal — Execution Body

## 1. Hub verification summary

The developer hub was checked before drafting this proposal.

Findings:

- Page01 is documented as complete at Stage149. `docs/stages/stage149.md` states that Stage149 seals the full Page01 constitution chain built in Stage145 through Stage148 and makes Stage150 Memory Body the next active development target.
- Page02 is represented by Stage150 through Stage154 in the recent development flow: Memory Contract, Local Read-Only Memory Store, Deterministic Local Query / Ranking, Memory Health & Leakage Boundary, and Page02 Release Seal.
- Hub search found no concrete Page03 design document.
- Hub search also found no authoritative 7-page roadmap document. The 7-page structure is therefore treated as a remembered architecture hypothesis that should now be formalized.

## 2. Seven-page architecture proposal

The proposed seven-page evolution model is:

| Page | Name | Role | Stage range |
|---|---|---|---|
| Page01 | Body Constitution | Constitutional authority, identity, state, project manifest, node boundary | Stage145-149 |
| Page02 | Narrative Memory Body | Memory contract, read-only store, deterministic query, health/leakage boundary, seal | Stage150-154 |
| Page03 | Execution Body | Deterministic execution planning, packets, plan graph, conflict preflight, dry-run trace, seal | Stage155-160 |
| Page04 | Rendering Body | Controlled scene/prose rendering surface over sealed execution plans | TBD |
| Page05 | Evaluation Body | Quality gates, benchmark interpretation, regression diagnosis, editorial scoring | TBD |
| Page06 | Governance Body | Release governance, policy authority, cross-project/cross-lineage control | TBD |
| Page07 | Evolution Body | Future-safe extension, migration planning, absorption governance, long-horizon self-audit | TBD |

## 3. Three-principal expert review

### Chief Principal Architect

Page03 should become the Execution Body. Page01 defines the constitution. Page02 defines memory. Page03 must convert those sealed authorities into execution plans without performing generation, mutation, training, or provider calls.

Architecture judgment:

- The correct abstraction is not an agent runtime.
- The correct abstraction is a deterministic execution compiler.
- Page03 must produce typed execution artifacts that later pages can consume.
- Page03 must not expand authority beyond Page01 and Page02.

### Chief Principal Compiler

Page03 should compile narrative intent into deterministic execution packets and plan graphs.

Compiler judgment:

- Inputs must be typed Page01 and Page02 evidence.
- Outputs must be typed packets, dependency graphs, dry-run traces, and conflict reports.
- The compiler must be deterministic: same inputs, same outputs.
- No provider, vector DB, write path, or hidden reveal payload may participate.
- Node2 receives only surface-safe projected plans.

### Chief System Principal Engineer

The main risk is privilege expansion. Page03 could accidentally become a runtime executor, hidden reveal bridge, write-enabled planner, or provider orchestration layer. Therefore Page03 must be sealed as dry-run-only infrastructure.

Systems judgment:

- Every Stage155-160 gate must assert provider-zero and write-zero.
- Every plan artifact must carry source stage, checksum, boundary level, and visibility.
- Every Node2 output must be projection-safe.
- Runtime execution must remain disabled until a later page explicitly authorizes it.

## 4. Consensus decision

The three experts agree:

Page03 should be defined as **Execution Body**.

It is a deterministic compiler page that converts sealed Page01 constitution and sealed Page02 memory into safe execution planning artifacts.

It must not perform final prose generation, memory mutation, canon mutation, runtime training, live provider execution, vector search, or auto-repair.

## 5. Proposed Stage155-160 sequence

### Stage155 — Execution Contract

Purpose: define typed execution packet contracts.

Outputs:

- `ExecutionIntentContract`
- `ExecutionPacketBase`
- `SceneExecutionPacket`
- `RevealExecutionPacket`
- `ContinuityExecutionPacket`
- `PayoffExecutionPacket`
- `ExecutionBoundaryPolicy`
- `ExecutionWritePolicy`

Gate invariants:

- provider calls = 0
- execution runtime disabled
- memory write disabled
- canon mutation disabled
- Node2 hidden reveal access = 0

### Stage156 — Local Execution Packet Store

Purpose: provide local read-only storage for execution packets.

Outputs:

- JSONL packet fixture store
- checksum index
- read-only loader
- schema validation report

Gate invariants:

- store write enabled = false
- packet mutation count = 0
- provider calls = 0

### Stage157 — Deterministic Plan Graph Builder

Purpose: build deterministic execution dependency graphs.

Outputs:

- plan node catalog
- edge/dependency registry
- topological order report
- blocked-cycle report

Gate invariants:

- deterministic ordering
- no hidden reveal projection to Node2
- no runtime execution

### Stage158 — Dependency and Conflict Preflight

Purpose: detect contradictions, missing prerequisites, unsafe boundary requests, and plan conflicts before execution.

Outputs:

- conflict registry
- prerequisite matrix
- boundary conflict report
- execution blocker registry

Gate invariants:

- all conflicts are report-only
- no automatic repair apply
- no canon mutation

### Stage159 — Execution Dry-Run Trace

Purpose: simulate execution order without executing generation or writes.

Outputs:

- dry-run trace log
- packet execution order
- skipped/blocked step registry
- reproducibility checksum

Gate invariants:

- dry-run only
- provider-zero
- write-zero
- deterministic trace

### Stage160 — Page03 Release Seal

Purpose: seal Page03 as a safe deterministic execution compiler page.

Outputs:

- Page03 release seal
- Stage155-159 evidence index
- execution safety matrix
- Page04 readiness matrix

Gate invariants:

- Page01 sealed
- Page02 sealed
- Page03 sealed
- no execution runtime enabled
- no provider calls
- no writes

## 6. Problem review and solutions

| Risk | Impact | Solution |
|---|---|---|
| Page03 becomes an agent runtime too early | Provider/write leakage | Keep Page03 compiler-only and dry-run-only |
| Execution packets mutate memory or canon | Breaks Page01/Page02 authority | Write policy disabled; mutation count must be zero |
| Node2 receives hidden reveal details | Boundary violation | Projection registry and release gate checks |
| Plan graph becomes nondeterministic | Non-reproducible release | Stable sorting, checksums, deterministic graph build |
| Future Page04 consumes unsafe plans | Downstream leakage | Stage160 Page04 readiness matrix must only expose safe artifacts |

## 7. Final recommendation

Create Page03 docs in hub under:

- `docs/proposals/page03_execution_body_proposal.md`
- `docs/architecture/page03_execution_body_blueprint.md`
- `docs/development/page03_developer_handoff.md`
- `docs/roadmap/seven_page_architecture.md`

Then begin Stage155 only after Stage154 Page02 Release Seal is merged into main.
