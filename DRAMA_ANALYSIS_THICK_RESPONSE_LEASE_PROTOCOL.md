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
