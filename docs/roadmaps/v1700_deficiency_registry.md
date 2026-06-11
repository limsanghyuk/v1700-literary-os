# V1700 Deficiency Registry

Status: ACTIVE_ROADMAP_REGISTRY
Created: 2026-06-10
Scope: long-term deficiency classification and remediation registry

## 1. Purpose

Track long-term missing capabilities in V1700 as structured remediation tracks.

## 2. Deficiency classes

| Class | Area | Current gap | Priority |
|---|---|---|---:|
| D-UX-001 | Writer IDE | no production UI surface | P0 |
| D-UX-002 | Story Bible/Codex | no full author-facing codex workspace | P0 |
| D-UX-003 | Agent Board | agent actions not visible in UX | P1 |
| D-MEAS-001 | Formula Measurement | no human rating calibration loop | P0 |
| D-MEAS-002 | EAT8D Calibration | advisory tensor not empirically fitted | P1 |
| D-DB-001 | Canonical Store | canonical record store not implemented | P0 |
| D-RAG-001 | Safe RAG | retrieval split between safe/protected context missing | P0 |
| D-GRAPH-001 | Graph Store | causal and relation graph backend missing | P1 |
| D-AGENT-001 | Agent Capability | permission contract incomplete in product UX | P0 |
| D-LEARN-001 | Self-learning | active weight update intentionally disabled | P1 |
| D-LEARN-002 | Frozen Dataset | no approved training corpus for coefficient update | P0 |
| D-MW-001 | MultiWork | cross-work isolation not complete | P0 |
| D-RIGHTS-001 | License Boundary | AuthorLicense / IP boundary not implemented | P0 |
| D-GOV-001 | Formula Registry | machine-readable formula registry incomplete | P0 |
| D-GOV-002 | GitNexus Bridge | early page bridge evidence incomplete | P1 |
| D-CI-001 | Product CI/CD | production pipeline and release automation incomplete | P1 |

## 3. Remediation tracks

```text
Track A: Writer IDE / UI productization
Track B: Formula Measurement and Calibration
Track C: Canonical DB / RAG / Graph
Track D: Agent Board and approval workflow
Track E: Bounded self-learning
Track F: Claude MultiWork conceptual absorption
Track G: Release and product proof automation
```

## 4. Promotion rule

A deficiency can be marked resolved only if:

```text
contract exists
fixture exists
validator exists
result artifact exists
boundary invariants are preserved
human or release governor decision is recorded
```

## 5. Current next action

```text
Implement Writer IDE advisory panel renderer after manual static review artifact.
```
