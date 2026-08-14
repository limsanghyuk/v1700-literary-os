# Drama Analysis — THICK Mechanical Response Lease Protocol

This protocol mechanically enforces the response-boundary rules for long THICK authoring. It supplements `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md`.

## Problem addressed

Documentation-only limits were insufficient: late-finishing writer flows could continue after the assistant response boundary and create semantic specs/records/audits ahead of `work_state`. This produces false progress and race conditions even when the semantic records themselves look valid.

## Mechanical lease

Every assistant response that authors THICK must open exactly one response lease before the first new sequence.

A lease records:
- `lease_id`
- `start_locked_count`
- `start_seq_id`
- `max_new_sequences = 3`
- `committed_count`
- `accepted_seq_ids`
- `state = OPEN | CLOSED`

The commit path must refuse a fourth sequence under the same lease.

## Commit rule

For each sequence:

`SOURCE_READ -> SEMANTIC_AUTHORED -> spec atomic write -> exact/source checks -> THICK record atomic write -> independent audit PASS -> checkpoint atomic write -> lease counter increment`

No process may automatically advance to a next sequence after the lease reaches 3 commits.

## End-of-response filesystem freeze

After the third commit, or before the response ends if fewer than three were authored:

1. close the response lease;
2. fsync the current checkpoint;
3. release the writer lock;
4. mark active semantic write surfaces read-only or otherwise deny new atomic renames;
5. record `next_seq_id`;
6. stop all semantic advancement.

The next assistant response must run reconciliation, explicitly thaw the write surfaces, acquire a new writer lock, and open a new lease.

## Overrun handling

Any semantic spec, THICK record, audit, or episode assembly created beyond the current response lease is not progress. It must be preserved in quarantine rather than silently accepted or deleted.

Promotion from quarantine requires a later assistant response to re-read the relevant source range and re-run the normal semantic/audit path under a new response lease. Files may be reused only as comparison evidence, not as already-completed semantic authoring.

## Reconciliation invariant

Only the contiguous sequence prefix within closed valid response leases is checkpoint-locked progress. `work_state.next_seq_id` must be computed from that prefix, not from the furthest file present on disk.

## Phase separation

THICK semantic authoring, episode assembly, block audit, PlannerInput R5 generation, Runtime R8 generation, database promotion, packaging, and fresh-extraction validation remain separate phases. A timeout in a later phase must not invalidate earlier durable PASS phases.

## 2026-08-14 hardening after repeated interruption

The `국희` incident demonstrated that even correct documentation can be violated if a response attempts to satisfy a block-level milestone in one turn. Therefore the following are non-overridable:

- A user request to finish a block defines the milestone only. It does not permit exceeding the 3-sequence lease.
- Source reading without a `CHECKPOINT_LOCKED` THICK transaction is not progress and must not advance `locked_sequences` or `next_seq_id`.
- A response that performs THICK semantic authoring must end after closing its semantic lease. It must not begin whole-work validation, R5, R8, DB integration, checksum build, ZIP build, fresh extraction, or hub promotion in that same response.
- Later phases advance only from durable PASS evidence, never from chat prose.
- `tools/drama_analysis_phase_guard.py` is the mechanical guard for these rules. Long THICK work must use it or an equivalent guard that rejects a fourth commit and out-of-order phase transitions.
- If the guard state and chat text disagree, guard/durable disk state wins.

See `DRAMA_ANALYSIS_REPEAT_INTERRUPTION_INCIDENT_20260814.md` for the incident evidence and recovery point.
