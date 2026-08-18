# Literary OS — Narrative Retrieval & Hierarchical Planning Roadmap R1

**Date:** 2026-08-19  
**Status:** `RESEARCH_DIRECTION_CURRENT / EXPERIMENTS_NOT_YET_PREREGISTERED`  
**Purpose:** 분석 DB를 실제 자율 창작 성능으로 전환하는 다음 연구·제품화 경로를 고정한다.

---

## 1. 핵심 가설

현재 38작 분석 DB의 진짜 가치는 “38개의 이야기를 저장했다”가 아니다.

> **수천 개의 회차·시퀀스 설계 의사결정 사례를 보유한다.**

현재 canonical corpus:
- 38 works
- 714 EpisodeSynopsisPlans
- 6,357 Sequences / THICK records
- 6,357 EpisodePlan sequence allocations

우리가 증명해야 할 질문은 다음이다.

1. DB를 검색하면 새로운 EpisodeSynopsisPlan과 SequencePlan의 품질이 실제로 좋아지는가?
2. DB 규모가 커질수록 좋아지는가?
3. 작품 수보다 분석 깊이가 더 중요한가?
4. 검색된 사례를 표절하지 않고 설계 문법으로 추상화할 수 있는가?
5. 모델이 N-1 상태만으로 EpisodeSynopsisPlan을 자율 생성할 수 있는가?
6. 생성 EpisodePlan에서 일관된 SequencePlans를 자율 생성할 수 있는가?
7. 생성 회차의 결과 상태를 다음 회차에 넘겨 여러 회차를 지속 설계할 수 있는가?
8. 이 계층을 Scene→Beat→Storyboard→영상 제작 자산으로 컴파일할 수 있는가?

---

## 2. Narrative Design Grammar

분석 DB에서 배우려는 것은 원작의 줄거리나 대사가 아니다.

### EpisodeSynopsisPlan grammar
조건:
- entry state
- active character/relationship trajectories
- active threads and debts
- information policy
- series position
- required / forbidden moves

설계 선택:
- episode axes
- why now
- defer policy
- debt paid/escalated/carried/retired
- terminal regime
- exit state
- Sequence function allocation

결과:
- state delta
- thread/debt delta
- relationship trajectory movement
- next-episode handoff quality

### SequencePlan grammar
조건:
- Sequence entrance state
- episode-axis responsibility
- active characters / goals
- thread and information state

설계 선택:
- goal
- obstacle
- tactic / pressure
- information movement
- relationship movement
- value shift
- turn
- plant/payoff role
- terminal/reset
- scene budget / scene functions

결과:
- Sequence exit state
- next-Sequence handoff
- contribution to EpisodeSynopsisPlan target

설계 문법은 단순 빈도 규칙이 아니라 **`조건 → 선택 → 상태변화 → 결과`**의 조건부 관계여야 한다.

---

## 3. Retrieval-Augmented Narrative Planning

### 잘못된 검색
- “도깨비와 비슷한 이야기 찾아줘”
- “배신 장면이 있는 작품 가져와”
- 특정 원작 한 편의 사건·대사·장면 순서를 template로 사용

### 목표 검색
현재 창작 문제를 기능적 상태로 표현한다.

예:
```text
relationship_state: trust weakening
information_policy: partial reveal
must_defer: betrayer identity
required_exit: distrust rises / truth unresolved
active_debt: identity question carried
terminal_need: forward pressure
```

이를 기반으로 여러 작품에서 서로 다른 기능 사례를 검색한다.

예:
- A: partial reveal 구조
- B: relationship pressure 구조
- C: debt carry timing
- D: terminal design
- E: subplot counterpoint

그 뒤:
`Retrieve → Abstract → Detach story surface → Recombine → Generate → Similarity/Leakage Audit`

검색된 사례의 인물명·고유 사건·대사·장소·고유 설정을 그대로 새 작품에 이전하지 않는다.

---

## 4. Anti-Plagiarism / Originality Protocol

### Before generation
1. single-reference 금지: 가능하면 multi-reference retrieval.
2. story-surface stripping: 이름·장소·고유 사건·고유 대사 제거.
3. function-only abstraction: state transition / pressure / information / relationship / timing만 유지.
4. current-work Canon을 먼저 고정하고 retrieved case를 그 Canon 아래에서만 사용.

### After generation
- phrase overlap
- event-order similarity
- character-role mapping similarity
- distinctive setup similarity
- Sequence-function sequence similarity
- one-source dominance
을 측정한다.

원작 similarity는 quality score가 아니라 **leakage diagnostic**이다.

---

## 5. Retrieval Scaling Experiment

### Question A — corpus size
동일 planning task에서:
- A0: no retrieval
- C5: 5 works
- C10: 10 works
- C20: 20 works
- C38: 38 works
- N: unrelated / mismatched retrieval

### Question B — representation depth
동일 작품 pool에서:
- D1: Stage02 thin only
- D2: THICK
- D3: THICK + Boundary
- D4: THICK + Boundary + EpisodeSynopsisPlan

### Factorial principle
DB size와 representation depth를 가능한 한 orthogonal하게 분리한다.

예:
`5/10/20/38 works × thin/THICK/full-planning representation`

목표는 단순한 “38 > 20” 증명이 아니다.

가능한 결과:
- quality saturates at 20 works → retrieval precision/representation depth가 더 중요
- 38 works keeps improving → DB expansion 가치 강함
- high-quality 10 works > thin 38 works → depth가 size보다 중요
- unrelated N arm도 좋아짐 → retrieval effect가 아니라 context-volume effect일 가능성

---

## 6. 기존 실험이 주는 근거

### Blind Forward 2026-08-11
공주가돌아왔다 EP01–08→EP09:
- A high-level 65
- B + Stage01–04 84
- C + THICK + PlannerInput 88

결혼못하는남자 EP09 full loop:
- SequencePlan 86
- future leakage 0
- scene draft 77 → critic/revision 86
- holdout compatibility 73
- scientific interpretation `PASS_WITH_LIMITATIONS`

해석: 깊은 planning representation이 forward generation에 도움을 주는 방향 신호.

### CT-11 2026-08-17
전체 boundary reproduction 주판정은 균등분할 baseline을 이기지 못해 불성립.
그러나:
- episode design B−A: +0.028
- **cross-work retrieval C−B: +0.070** (사전 임계 +0.05 통과)
- Sequence-count error A/B/N 3.22 → C 1.67

해석: cross-work retrieval은 유용할 수 있으나 당시 canonical boundary ceiling 문제 때문에 최종 causal proof는 아님.

### CT-13 R3
좋은 EpisodeSynopsisPlan을 공급한 C arm은 B/N보다 매우 강한 PASS-like numeric pattern을 보였다.
하지만 independent 3-scorer gate가 성립하지 않아 formal verdict `UNDECLARED`.

해석: **좋은 EpisodePlan의 renderer utility는 강하게 지지되지만, EpisodePlan을 N-1에서 자율 생성하는 능력은 아직 미검증.**

---

## 7. 제안 CT-14 — Retrieval Scaling

**아직 preregistration 전.**

목표:
- corpus size effect
- representation depth effect
- retrieval relevance effect
을 분리한다.

출력:
- autonomous EpisodeSynopsisPlan candidate
- autonomous SequencePlan candidates

평가:
- planning coherence
- why-now quality
- defer policy
- debt consistency
- character/relationship congruence
- terminal quality
- Sequence allocation quality
- Sequence goal/obstacle/turn/value shift
- Boundary validity
- originality/leakage

---

## 8. 제안 CT-15 — Blind Forward EpisodeSynopsisPlan

Target episode N의 SOURCE를 물리적으로 holdout한다.

입력:
- N-1 Canonical state only
- allowed retrieval corpus
- current design grammar

모델이 직접 생성:
- EpisodeSynopsisPlan N

생성 결과를 seal한 뒤에만 actual N SOURCE를 연다.

실제 방송분과의 유사도는 유일한 정답 지표가 아니다. 실제 회차는 high-quality reference solution 중 하나다.

평가 중심:
- state consistency
- character/relationship plausibility
- thread/debt policy
- novelty
- future leakage
- feasible Sequence allocation

---

## 9. 제안 CT-16 — Hierarchical Forward Planning

입력:
- generated EpisodeSynopsisPlan

생성:
- SequencePlan 01..K

핵심 metric:
**EpisodePlan→SequencePlan cross-level congruence**

각 Sequence는 적어도 하나의 episode-axis / debt / terminal function을 소유해야 하며, 불필요한 기능 중복과 누락을 측정한다.

추가 평가:
- Sequence count plausibility
- Boundary transaction validity
- handoff continuity
- subplot allocation
- repetitive pattern rate

---

## 10. 제안 CT-17 — Multi-Episode Rollout

EP09만 잘 만드는 것으로 장기 시리즈 창작 능력을 증명할 수 없다.

실험:
`generated EP09 → derive new Canon state → plan EP10 → derive state → EP11 → EP12`

관측:
- character drift
- relationship drift
- thread orphaning
- debt explosion
- payoff starvation
- repeated terminal pattern
- retrieval overfitting
- state contradiction

목표: **long-horizon writer stability**.

---

## 11. 제안 CT-18 / CT-19 — Production Descent

### CT-18
`SequencePlan → ScenePlan → Beat`

평가:
- dramatic transaction preservation
- scene necessity
- scene boundary
- beat causality
- dialogue/action feasibility
- continuity

### CT-19
`Beat → Shot → Storyboard → Production Assets`

생성 대상:
- shot purpose
- framing / camera
- character state
- wardrobe
- location
- props
- lighting
- dialogue / VO
- SFX / music cue
- image-generation prompt
- video-generation prompt

목표: Narrative OS를 실제 개인 영상 제작 workflow와 연결.

---

## 12. Narrative Weights / Learned Planning

현재 시스템의 “가중치”는 LLM 내부 neural parameter와 다르다.

### Hard constraints
위반 시 candidate 탈락:
- future leakage
- Canon contradiction
- SOURCE/SourceLock integrity
- Boundary/parity
- inherited debt accounting

### Narrative priors
soft diagnostics:
- thread timing
- debt timing
- terminal distribution
- relationship movement
- information release
- Sequence rhythm

### Retrieval weights
예시 feature:
- dramatic-function similarity
- relationship-state similarity
- debt-state similarity
- information-policy similarity
- character-goal similarity
- episode-position similarity
- genre similarity

### Candidate ranking weights
좋은 Episode/Sequence 후보를 고르는 score/ranker를 실험 결과로 학습할 수 있다.

### Dynamic Narrative Attention
작품/회차마다 중요도가 다르다.
예: romance-heavy episode와 conspiracy-payoff episode에서 active Thread weights는 달라야 한다.

장기 진화:
`Explicit Rules → Measured Priors → Learned Retrieval/Ranking Weights → Dynamic Narrative Attention`

---

## 13. DB 확장 원칙

새 작품을 분석할 이유는 “작품 수를 늘리기 위해서”가 아니다.

새 분석은 다음 중 하나를 개선해야 한다.
- retrieval coverage
- genre/state diversity
- rare planning pattern coverage
- Episode grammar estimation
- Sequence grammar estimation
- learned ranker performance
- long-horizon rollout robustness

따라서 향후 DB 확장 판단은 scaling curve와 coverage gap에 연결한다.

---

## 14. 제품화 방향

최종 사용자는 JSON schema를 직접 다루지 않는다.

예상 UX:
```text
PROJECT
 ├─ Story Bible
 ├─ Characters / Relationships
 ├─ Series / Season
 ├─ Episode 01
 │   ├─ Episode Synopsis Plan
 │   ├─ Sequence 01
 │   │   ├─ Scene 01
 │   │   └─ Scene 02
 │   └─ Sequence 02...
 ├─ Screenplay
 ├─ Storyboard
 ├─ Assets
 └─ Production
```

사용자가 “관계가 너무 빨리 가까워진다”라고 수정하면 EpisodePlan→SequencePlan→Scene의 영향을 추적해 다시 설계해야 한다.

상업 메시지:
> **Story Architecture → Script → Storyboard → Production**

---

## 15. 프로젝트 판단 기준

앞으로 새로운 분석층·필드·실험을 제안할 때 반드시 묻는다.

1. 현재 Stage01–04/THICK/Plan으로 표현 못 하는 정보인가?
2. retrieval 또는 planning quality를 실제로 높이는가?
3. blind holdout / ablation으로 검증 가능한가?
4. SOURCE provenance를 유지할 수 있는가?
5. originality/leakage를 악화시키지 않는가?
6. Scene/Beat/Storyboard로 내려갈 때 사용되는가?

이 질문에 답하지 못하는 데이터 증가는 연구 부채가 될 수 있다.

---

## 16. 현재 최우선 순서

1. R21/38작 corpus를 연구 baseline으로 고정.
2. Retrieval Scaling preregistration 작성.
3. blind forward EpisodeSynopsisPlan generation protocol 작성.
4. SequencePlan hierarchical congruence metric 정의.
5. unrelated retrieval / story-surface leakage negative controls 정의.
6. 독립 scorer/custodian 구조를 실험 시작 전에 확보.
7. CT-14/15에서 양의 결과가 나오면 multi-episode rollout.
8. 그와 병렬로 Scene/Beat/Storyboard compiler의 최소 제품 vertical slice를 시작.

이 로드맵의 핵심은 **분석 DB를 ‘좋은 분석 자료’에서 ‘실제로 창작 성능을 증가시키는 Narrative Design Memory’로 전환하는 것**이다.
