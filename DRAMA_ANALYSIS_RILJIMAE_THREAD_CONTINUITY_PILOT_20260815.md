# 돌아온일지매 Thread Continuity Anchor Pilot — 2026-08-15

Status: **PILOT_PASS_ID_ONLY / NOT_CANONICAL**

Purpose: test Claude D-61/R1 retrospective thread continuity repair on one anchor work before any broad rollout.

## Safety rule

Only high-confidence `thread_id` aliases supported by direct source and/or explicit prior refs were retained. No semantic payload was rewritten.

Unchanged:
- `event`
- `cast.desire_or_function`
- `info_shift`
- `plant_payoff.statement`
- `scene_notes.functional_propositions`
- existing source/evidence coordinates

R5/R8 were regenerated after ID rebinding.

## Before

- thread IDs: 116
- multi-episode thread IDs: 78
- multi-episode %: **67.2%**
- plant/payoff entries: 419
- previous-episode existing_refs %: **43.7%**
- R5 coupling %: **23.7%**

## High-confidence rebind

- accepted alias IDs: **22**
- changed plant/payoff entries: **170**
- semantic payload invariance: **PASS — only thread_id changed**

Examples of source-supported identities include:
- `dali_first_contact -> dali_bond`
- `bae_chadol_record -> gii_iljimaejeon`
- `gujamyeong_baekmae_reunion/promise -> gujamyeong_baekmae`
- `baekmae_unknown_reunion / mother-son reunion -> baekmae_mother`
- `hongtaiji_debt -> hongtaiji_recognition`
- `nonlethal_ethic -> nonlethal_justice`

Broader aliases that were semantically related but not proven identical were discarded rather than retained merely to raise a score.

## After

- thread IDs: 94
- multi-episode thread IDs: 66
- multi-episode %: **70.2%**
- plant/payoff entries: 419
- previous-episode existing_refs %: **43.7%**
- R5 coupling %: **26.5%**

Delta:
- multi-episode: **+3.0 pp**
- R5 coupling: **+2.8 pp**

## Interpretation

The proposed 40% multi-episode and 30% R5-coupling values are diagnostic lines, not correctness gates. This pilot remains below 30% R5 coupling after high-confidence repair. We explicitly did **not** broaden semantic aliases to hit 30%.

R5 is future-blind by design. A correct R5 cannot inspect the target episode and choose only the unresolved threads that happen to reappear there; therefore same-episode coupling is partly a corpus/episode manifestation measure rather than a pure correctness measure.

## Decision

- adopt Thread Continuity R1 prospectively for new dramas;
- retain conservative ID-only retrospective method;
- do not scale automatic semantic similarity merging across the corpus;
- do not promote this pilot into current canonical authority in this change;
- keep `resolves_thread` experimental until explicit schema validation/promotion.
