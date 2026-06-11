# Agent Board Blueprint

Status: PROPOSED_SCAFFOLD
Created: 2026-06-10
Scope: AI agent UX and governance planning for V1700 Writer IDE

## 1. Purpose

Expose AI agent actions as inspectable, auditable, permission-bound workflow units.

Agents must not become invisible autonomous mutators.

## 2. Agent roles

```text
ArchitectAgent
CompilerAgent
CriticAgent
ContinuityAgent
MemoryCuratorAgent
RightsBoundaryAgent
UXAgent
ReleaseGovernorAgent
```

## 3. Agent permission levels

```text
L0 Observe
L1 Annotate
L2 Propose
L3 PatchDraft
L4 ApplyWithHumanApproval
L5 AutonomousApplyReserved
```

Initial V1700 Writer IDE should open only L0-L2 by default.

## 4. Agent action record

```text
agent_action_id
agent_id
agent_role
permission_level
input_refs
action_type
output_refs
confidence
requires_human_approval
mutation_performed
blocked_by_policy
created_at
```

## 5. Agent board UX

```text
Left: agent list and status
Center: selected proposal / annotation
Right: evidence refs and boundary flags
Bottom: human approval queue
```

## 6. Required checks

```text
agent cannot read restricted source without policy edge
agent cannot mutate canon without approval
agent cannot write memory by default
agent cannot update coefficients
agent cannot open Page18 runtime
agent disagreement is recorded, not hidden
```

## 7. Next implementation candidate

```text
docs/contracts/agent_action_record_contract.md
fixtures/agent_board/minimum_agent_actions.json
tools/agent_board_packet_builder.py
tests/test_agent_board_packet_builder.py
```
