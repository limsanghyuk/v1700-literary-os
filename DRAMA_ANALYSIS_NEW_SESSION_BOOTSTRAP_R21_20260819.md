# Drama Analysis — New Session Bootstrap R21

**Current date:** 2026-08-19  
**Use:** 새 GPT/Claude 세션이 이전 대화 없이 현재 정본에서 즉시 재개하기 위한 부팅 문서.

## Mandatory reading order

1. `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`
2. `CURRENT_AUTHORITY_POINTER.json`
3. `DRAMA_ANALYSIS_SESSION_HANDOFF_R21_20260819.md`
4. `DRAMA_ANALYSIS_METHOD_CURRENT_R21_20260818.md`
5. `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1_HUB_MIRROR.md`
6. `DRAMA_ANALYSIS_EXACT_SCHEMA_REGISTRY_V10_1.json`
7. `DRAMA_ANALYSIS_EPISODE_PLAN_HANDOFF_MANUAL_R5_20260818.md`
8. `CT13_R3_FINAL_RESEARCH_CLOSURE_R1_20260818.md`
9. `LITERARY_OS_NARRATIVE_RETRIEVAL_HIERARCHICAL_PLANNING_ROADMAP_R1_20260819.md`
10. 대상 작품을 선택한 뒤에만 작품별 SOURCE / SourceLock / work_state / checkpoint를 연다.

## Current state

- Stage01–04: **98 works**
- V10.1-equivalent: **97**
- SOURCE_HOLD: **1 — 최강칠우**
- CANONICAL THICK / Boundary / EpisodePlan: **38 works**
- Stage02 = THICK: **6,357 = 6,357**
- EpisodeSynopsisPlan: **714**
- EpisodePlanningContext: **714**
- EpisodePlan schema: **EpisodeSynopsisPlan.v0.3-r1**
- R5/R8: **714 / 714**
- Runtime scenes: **46,078**
- CT-13 R3 formal verdict: **UNDECLARED**
- reverse-engineered EpisodePlan corpus: **CANONICAL**
- autonomous forward EpisodePlan control: **EXPERIMENTAL_HOLD**

## Current 4-work R2 reinforcement

- 개인의취향
- 수호천사
- 미안하다사랑한다
- 미생

Stage01–04와 Sequence membership은 보존되었고, THICK semantic prose와 일부 EpisodePlan semantic/debt가 보강되었으며 R5/R8을 재생성했다.

`미안하다사랑한다 EP16`에서 inherited debt 누락 1건을 발견해 `MISA_MUHYEOK_MINJU_REVENGE_SEDUCTION → PAID`로 수리했고, EpisodePlan self-check는 **714 / HARD 0**이다.

`미생`의 이번 강화 범위는 **EP01–EP11**로 해석한다.

## New drama execution chain

`SOURCE/SourceLock → Q1~Q4 direct reading → Stage01 → Stage02+Boundary → Stage03 → Stage04 → post-boundary semantic re-audit when needed → THICK → EpisodePlanningContext(N-1 freeze) → EpisodeSynopsisPlan → R5 → R8 → Exact/Provenance → Semantic V3 → Owner/Grounding → Depth → Thread R2 → Subplot → Deep Semantic → Artifact Hash → Whole-work Gate → Package → Fresh Extraction → DB Integration → Bundle Update`

## Non-negotiable rules

- Python semantic generation 금지.
- SOURCE 결손 추정 보완 금지.
- LocalEdge는 동일 회차 / causal / gap=0.
- 회차간 연결은 Stage04 CrossEpisodeEdge.
- Sequence 고정 개수 quota 금지.
- location=boundary 금지.
- corpus 평균을 hard rule로 쓰지 않음.
- canonical similarity를 품질 목표로 쓰지 않음.
- N-1 planning input에 future SOURCE 정보 금지.
- Boundary가 바뀌면 Stage03/04 의미 귀속을 SOURCE로 재감사.
- THICK/Plan이 바뀌면 affected R5/R8 재생성.
- CANONICAL 편입 전 non-target invariance + fresh extraction 필수.

## Next research priority

현재 정본을 다시 만드는 것이 다음 연구가 아니다.

다음 핵심은:

> **N-1 state + 38-work retrieval만으로 EpisodeSynopsisPlan을 자율 생성하고, 그 Plan에서 SequencePlans를 자율 생성하여 실제 회차 설계를 끝까지 수행할 수 있는가?**

병행 연구:
- Retrieval Scaling: no retrieval / 5 / 10 / 20 / 38 works
- Representation Depth Scaling: thin / THICK / THICK+Boundary / THICK+Boundary+EpisodePlan
- originality / leakage guard
- EpisodePlan→SequencePlan cross-level congruence
- multi-episode rollout
- Scene/Beat→Storyboard/Production compiler

CT-13을 유리한 결론이 나올 때까지 반복하지 않는다. formal verdict `UNDECLARED`를 보존한다.
