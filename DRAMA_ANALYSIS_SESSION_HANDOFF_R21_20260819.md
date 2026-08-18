# Drama Analysis / Literary OS — Full Session Handoff R21

**Date:** 2026-08-19 KST  
**Status:** `CURRENT_SESSION_CLOSED_FOR_HANDOFF`  
**Primary repository:** `limsanghyuk/v1700-literary-os`  
**Engine/research bridge:** `limsanghyuk/literary-os`

이 문서는 2026-08-18~19 GPT 세션에서 수행한 분석 DB 보강, Sequence Boundary, EpisodeSynopsisPlan, CT-13 R3, 4작 Deep Semantic R2 편입, 새 세션 학습 번들 정리, 그리고 이후 Literary OS의 연구·상업 방향에 대한 논의를 한 문서에 통합한 자립형 인계서다.

---

## 1. 프로젝트의 현재 북극성

드라마 분석 자체가 최종 목적이 아니다. 현재 프로젝트의 목적은 실제 드라마에서 **서사 설계 사례를 축적하고**, 그 사례로부터 좋은 회차와 좋은 시퀀스의 **조건부 설계 문법**을 배우며, 필요한 사례를 검색·추상화·재조합하여 새로운 작품을 자율 설계하는 것이다.

최종 상업 파이프라인은 다음을 목표로 한다.

`Idea / Brief → Canon / Character / Relationship State → EpisodeSynopsisPlan → SequencePlan → ScenePlan → Beat → Screenplay → Storyboard → Shot / Production Assets → Video Production`

핵심 차별화 자산은 특정 영상 생성 모델이 아니라 **Narrative Intelligence**다. 기초 LLM과 영상 모델은 교체 가능한 renderer가 될 수 있지만, Narrative Case Library, 설계 문법, Retrieval, Thread/Debt/Continuity, candidate ranking, narrative weighting은 프로젝트의 독자 자산으로 남아야 한다.

---

## 2. 현재 DB 정본 상태

### Stage01–04
- 총 작품: **98**
- `V10_1_EQUIVALENT_CANONICAL`: **97**
- `SOURCE_HOLD_FAIL_CLOSED`: **1 — 최강칠우**
- Stage01–04 의미 권위: **V10.1**
- DB numeric release family: **V9**

### CANONICAL THICK / Boundary / EpisodePlan cohort
- 작품: **38**
- Stage02 Sequence: **6,357**
- THICK Sequence: **6,357**
- Stage02↔THICK membership parity: **exact**
- EpisodePlanningContext: **714**
- EpisodeSynopsisPlan: **714**
- Sequence allocations: **6,357**
- EpisodePlan schema: **`EpisodeSynopsisPlan.v0.3-r1`**
- PlannerInput R5: **714**
- Runtime R8: **714**
- Runtime scenes: **46,078**

### 38 CANONICAL THICK works
101번째프로포즈, 가을동화, 강남엄마따라잡기, 개와늑대의시간, 건빵선생과별사탕, 검사프린세스, 결혼못하는남자, 경성스캔들, 공주가돌아왔다, 구해줘, 국희, 굿캐스팅, 궁, 그저바라보다가, 난폭한로맨스, 내여자친구는구미호, 내이름은김삼순, 너의목소리가들려, 녹두꽃, 뉴하트, 닥터챔프, 대물, 대장금, 더킹투하츠, 도깨비, 돌아온일지매, 드림, 라이벌, 로망스, 마왕, 마지막전쟁, 모래시계, 밀회, 비밀, 개인의취향, 수호천사, 미안하다사랑한다, 미생.

주의: `미생`의 이번 Deep Semantic R2 보강 패키지에서 강화된 통합 범위는 **EP01–EP11**이다. 이를 EP20 전체 R2 강화로 과장하지 않는다.

---

## 3. Sequence Boundary R1 — 이번 세션의 핵심 기반

Sequence 정의:

> **하나의 지배적 dramatic transaction이 진행되는 최소 연속 Scene 묶음.**

Boundary 판정의 핵심은:
- `LEFT TERMINAL`
- `RIGHT RESET`
- `±1 minimality`

Boundary reason codes:
- B1 GOAL_SETTLEMENT
- B2 KNOWLEDGE_PREMISE_SHIFT
- B3 RELATIONSHIP_OR_COMMITMENT_SHIFT
- B4 POWER_OR_CONSTRAINT_SHIFT
- B5 WORLD_REGIME_SHIFT
- B6 PLOT_LINE_HANDOFF
- B7 COMPOUND_TERMINAL

Verdict:
- VALID
- NEARBY_VALID
- MERGE_CANDIDATE
- SPLIT_CANDIDATE
- REVIEW_REQUIRED

금지:
- 장소가 같다는 이유로 묶기/나누기
- 동일 Scene 수 등분
- 작품 평균 Sequence 수 맞추기
- 고정 3-Sequence 규칙
- THICK에서 Stage02 membership을 조용히 재분할

이번 세션에서 기존 34 CANONICAL 작품을 Boundary R1로 닫은 뒤 외부 4작을 동일 규칙으로 편입하여 현재 38작에서 `Stage02=THICK 6,357=6,357`을 유지했다.

대표 수리:
- `경성스캔들`: 과거 Stage02 150 / THICK 138 → 최종 145 / 145.
- `개와늑대의시간`: 과거 143 / 132 → 최종 132 / 132. SOURCE 직접 판정 후 Stage02 의미까지 재저작.
- `결혼못하는남자 EP04`: 기계적으로 균등했던 12 Sequence → 13 Sequence.
- `그저바라보다가`: `_SEQxx` vs `_Sxx` 16건은 membership 동일한 historical alias 진단이며 blocking 결손이 아니다.

Boundary를 변경하면 Stage03/04를 단순 ID 참조 기준으로 끝내지 않고 CharacterArc, RelationshipArc, LocalEdge, PayoffCandidate, CrossEpisodeEdge, EpisodeArc 의미 귀속을 SOURCE로 다시 감사한다.

---

## 4. EpisodeSynopsisPlan — 현재 정의와 역할

실무상 `EpisodePlan`은 현재 `EpisodeSynopsisPlan`의 약칭으로 사용한다. 단 `EpisodeArc`나 `PlannerInput R5`와는 다르다.

- `EpisodeArc`: 완성된 회차를 후향적으로 설명하는 구조 분석.
- `EpisodeSynopsisPlan`: 회차를 **왜 지금 이렇게 설계하는가**를 명시하는 planning layer.
- `PlannerInput R5`: Episode N을 만들 때 사용 가능한 **N-1까지의 상태 경계/input**.

EpisodeSynopsisPlan의 핵심 책임:
- episode axes
- `why_this_episode`
- deferred decisions
- debt ledger (`paid / escalated / carried / retired`)
- terminal design
- exit-state target
- Sequence allocation / ownership

이미 방영된 작품에서는 N을 읽기 전에 `EpisodePlanningContext.R1`을 N-1 정보로 freeze한 뒤, N SOURCE 분석을 완료하고 `REVERSE_ENGINEERED_CASE` EpisodeSynopsisPlan을 저작한다. N-1 planning context에 N 또는 이후의 정보를 역주입하면 안 된다.

현재 38작 / 714회 / 6,357 allocations가 `EpisodeSynopsisPlan.v0.3-r1`로 canonical이다.

### 34작 mass authoring에서 배운 품질 교훈
초기 mass candidate는 곧바로 승격하지 않았다. 발견된 문제:
- formulaic WHY 문장
- `…` truncation
- final episode에서 허구의 “다음 회차” 전제
- v0.2와 current schema authority 불일치

수리 후:
- why_this_episode 1,897/1,897 unique (당시 34작)
- deferred reasons 1,272/1,272 unique
- 102 episode stratified raw-SOURCE audit: 102/102 PASS, 583 SOURCE anchors, rewrite_required 0

중요한 정직성: 656개 Plan을 만들 때 656개 raw script를 전부 새로 처음부터 다시 읽은 것이 아니라, SOURCE-grounded current Stage02/THICK/R5/EpisodeArc semantics에서 reverse-engineer했고 102회차를 raw-SOURCE stratified audit했다.

---

## 5. 외부 4작 편입과 Deep Semantic R2

외부/다른 GPT 세션에서 온 4작:
- 개인의취향
- 수호천사
- 미안하다사랑한다
- 미생

이들은 Stage01–04 98작에 이미 존재하던 작품이므로 작품 총수가 98→102가 된 것이 아니다. 현재 승격은 **CANONICAL THICK / Boundary / EpisodePlan 34→38작**이다.

초기 외부 Plan은 주로 v0.2였으며 의미를 보존해 v0.3-r1로 무손실 승격했다. 4작 58 Plan은 schema PASS 후 현재 714 Plan corpus에 편입했다.

Deep Semantic R2 보강에서는:
- Stage01–04와 Sequence membership: 유지
- THICK semantic prose: 강화
- 일부 EpisodePlan prose / debt parity: 강화
- R5/R8: final THICK에서 재생성

실제 편입 중 발견한 blocking 결손:
- `미안하다사랑한다 EP16`
- inherited debt `MISA_MUHYEOK_MINJU_REVENGE_SEDUCTION`이 ledger에서 누락
- SOURCE-grounded final state를 대조해 `PAID`로 결산
- 수리 후 EpisodePlan **714 / HARD 0**

비대상 34작 THICK/R5/R8/EpisodePlan은 SHA invariance를 확인하여 강화 4작 때문에 기존 정본이 흔들리지 않음을 검증했다.

---

## 6. 현재 전역 품질 closure

최종 38작 R21 기준:
- Stage01–04 V10.1 equalization: PASS
- Boundary R1: 38/38 PASS
- Stage02↔THICK: 6,357=6,357
- Exact/Provenance: PASS
- THICK records: 6,357
- SOURCE refs checked: 147,633
- provenance hash checks: 31,785
- Semantic Independence V3: 38/38 PASS
- Owner/Grounding: blocking 0
- Depth: blocking 0
- Thread R2: 38/38 PASS
- Subplot distinct-source-event duplicate: 0
- Deep Semantic: 38/38 PASS
- EpisodePlan: 714 / HARD 0
- R5/R8: 714/714
- Artifact hash: 2,142/2,142 PASS

Deep Semantic validator에서 한 번 blocking 1이 발생했으나 데이터 결함이 아니라 과거 29작 manual SOURCE registry를 기본으로 읽는 stale-default 문제였다. current 38작 registry를 명시하여 38/38 blocking 0으로 재현했다. 앞으로 validator 실행계약에서 current registry를 명시적으로 고정한다.

---

## 7. CT-13 R3 — EpisodeSynopsisPlan 효용 연구의 최종 상태

질문:
> 좋은 work-specific EpisodeSynopsisPlan을 renderer에 주면 planning quality가 실제로 좋아지는가?

외부 Claude renderer:
- 48/48 outputs
- 6 isolated sessions × 8 inputs
- manifest SEALED
- manifest SHA256: `b9a7c420dde4c58d2c7469272aa230fb220f0cc4784e1859a83b272b804774e0`

현재 세션 내부 3-rubric robustness diagnostic:
- C vs B P1: p=.0078125
- C vs B P2: p=.0009765625
- C vs B P3: p=.00048828125
- C vs B direction agreement: 0.9722
- C vs N P1/P2: p=.001953125
- C vs N P3: p=.00048828125
- C vs N direction agreement: 1.000
- explicit post-N leakage diagnostic: 0

숫자상 preregistered PASS-like pattern은 매우 강했다. 그러나 preregistration §7은 단일 assistant session이 3 independent blind scorers를 대신해 PASS를 인증할 수 없다고 고정했다.

따라서 최종 과학적 상태:
- formal preregistered verdict: **`UNDECLARED`**
- diagnostic effect: **strong PASS-like incremental utility support**
- reverse-engineered 38-work EpisodePlan corpus: **CANONICAL 유지**
- autonomous forward-generation control: **EXPERIMENTAL_HOLD**

CT-13이 직접 증명하지 않는 것:
> N-1 상태만 보고 planner가 같은 수준의 EpisodeSynopsisPlan 자체를 자율 생성할 수 있는가?

이것이 다음 blind forward-plan 연구 질문이다.

---

## 8. SequencePlan — 이미 확보한 전방생성 신호

이 세션에서는 이전 engine hub의 blind-forward 결과를 다시 대조했다.

### 2026-08-11 Blind Forward
`공주가돌아왔다 EP01–08 → EP09`
- A high-level: 65
- B + Stage01–04: 84
- C + THICK + PlannerInput: **88**
- C−A = +23
- C−B = +4

`결혼못하는남자 EP01–08 → EP09`
- candidates 8 → selected 6 / deferred 2
- SequencePlan quality: **86**
- future leakage: **0**
- scene draft: 77 → critic/revision **86**
- holdout compatibility: **73** (gate 70)
- overall: `PASS`, scientific interpretation `PASS_WITH_LIMITATIONS`

제한:
- 표본 2작
- 동일 모델 계열의 pretraining knowledge 배제 불가
- multi-work / genre generalization 미증명
- multi-episode rollout 미증명

### CT-11 cross-work retrieval 신호
CT-11의 “회차를 Sequence로 분할하는 경계 재현” 자체는 균등분할 baseline을 못 이겨 **불성립**이었다. 그러나 부수 효과는 중요했다.
- B + episode design layer vs A: +0.028
- **C + cross-work examples vs B: +0.070** — 사전 임계 +0.05 충족
- Sequence count error가 A/B/N 3.22에서 C 1.67로 크게 교정

해석:
> cross-work retrieval이 Sequence 설계에 유용할 수 있다는 초기 양의 신호는 있었지만, 당시 canonical Sequence boundary 자체에 ceiling 문제가 있었으므로 최종 증명은 아니었다.

이후 Boundary R1 보강의 목적 중 하나가 바로 이 실험 기반을 다시 신뢰 가능하게 만드는 것이었다.

---

## 9. 현재 연구 방향 — Narrative Design Grammar

우리가 만드는 것은 드라마 내용을 복사하는 시스템이 아니라 다음의 **조건부 설계 문법**이다.

### EpisodeSynopsisPlan grammar
질문:
> 이번 회차에서 무엇을 움직이고, 무엇을 미루며, 어떤 상태로 끝낼 것인가?

주요 축:
- entry / exit state
- episode function / axes
- why now
- defer policy
- inherited debt / payoff timing
- terminal regime
- subplot allocation
- Sequence ownership

### SequencePlan grammar
질문:
> 이 하나의 dramatic transaction을 어떤 목표·장애·압력·전환으로 진행하고 어디에서 끝낼 것인가?

주요 축:
- goal
- obstacle
- tactic / pressure
- information movement
- relationship movement
- value shift
- turn
- thread / plant / payoff role
- entrance / exit state
- Boundary terminal/reset
- next-Sequence handoff

궁극 구조:
`EpisodeSynopsisPlan = 여러 Sequence를 조직하는 문법`
`SequencePlan = 여러 Scene을 조직하는 문법`

---

## 10. Retrieval-Augmented Narrative Planning

다음 진화의 핵심은 38작 DB를 단순 예시 저장소가 아니라 **Narrative Design Case Library**로 사용하는 것이다.

새 창작 문제를 작품명/줄거리 유사도로 검색하지 않는다. 기능적 상태로 검색한다.
예:
- trust down
- partial reveal
- identity deferred
- relationship pressure up
- debt carry
- unresolved terminal

검색은 multi-reference가 기본이다.
- 작품 A: information reveal pattern
- 작품 B: relationship pressure pattern
- 작품 C: terminal design
- 작품 D: subplot counterpoint
- 작품 E: debt timing

그 뒤 원작 고유의 인물명·장소·대사·사건을 제거하고 기능적 설계만 추상화해 새 작품 Canon에 재조합한다.

권장 흐름:
`Retrieve → Abstract → Detach story surface → Recombine → Generate → Similarity / Leakage Audit`

canonical similarity는 품질 목표가 아니다. 높은 유사도는 오히려 leakage / imitation diagnostic이 될 수 있다.

---

## 11. DB scaling과 분석 깊이 — 다음 핵심 실험

다음 연구 질문:
> DB 규모와 분석 깊이가 SequencePlan·EpisodeSynopsisPlan의 자율 설계 성능을 얼마나 높이는가?

두 축을 분리한다.

### Corpus-size scaling
`No retrieval → 5작 → 10작 → 20작 → 38작`

### Representation-depth scaling
`Stage02 thin → THICK → THICK+Boundary → THICK+Boundary+EpisodeSynopsisPlan`

가능한 결과는 단순한 “100작 > 38작”이 아닐 수 있다. 고품질 20작이 저품질 100작보다 더 유용할 수 있다. 따라서 작품 수와 의미 깊이의 상호작용을 측정해야 한다.

CT-07/Blind Forward 계열은 얇은 분석보다 THICK 정보가 생성 조향에 더 유용하다는 방향 신호를 이미 제공했다. CT-11은 cross-work retrieval의 +0.070 신호를 보였다. 이제 Boundary/THICK/EpisodePlan이 보강된 38작에서 재시험한다.

---

## 12. 제안 연구 프로그램 — CT-14 이후

아래 번호는 **현재 세션의 제안 roadmap**이며 아직 preregistered authority가 아니다.

### CT-14 — Retrieval Scaling
- corpus size와 representation depth를 orthogonal하게 비교
- SequencePlan과 EpisodeSynopsisPlan 각각 측정
- unrelated retrieval negative control 포함

### CT-15 — Blind Forward EpisodeSynopsisPlan
- target N SOURCE를 물리적으로 holdout
- N-1 state만으로 EpisodeSynopsisPlan N 자율 생성
- 실제 N은 생성 봉인 후에만 개봉

### CT-16 — Hierarchical Planning
- generated EpisodeSynopsisPlan → generated SequencePlans
- cross-level congruence 측정
- 각 Sequence가 EpisodePlan axis/debt/terminal 목적을 실제 수행하는지 평가

### CT-17 — Multi-Episode Rollout
- 생성 EP09 결과 상태 → EP10 → EP11 → EP12
- Thread drift / relationship drift / debt explosion / repetitive terminal / retrieval overfitting 측정

### CT-18 — Scene / Beat Production
- SequencePlan → ScenePlan → Beat
- continuity와 dramatic transaction 유지 여부 측정

### CT-19 — Storyboard / Production Compilation
- Beat → Shot → Storyboard panel → image/video/audio prompts / production assets
- 상업 제품 파이프라인으로 연결

---

## 13. Narrative Weighting — 우리 시스템의 ‘가중치’ 개념

현재 Literary OS는 기초 LLM처럼 내부 수십억 neural weights를 직접 학습하는 시스템은 아니다. 그러나 이미 외부 planning weights에 해당하는 구조가 있고 앞으로 학습 가능하다.

### Level 1 — Hard Constraints
- SOURCE integrity
- future leakage
- Canon contradiction
- Boundary validity
- ID/parity
- debt accounting

위반 시 사실상 `−∞ penalty`.

### Level 2 — Narrative Priors
- thread timing
- debt timing
- information reveal
- relationship pressure
- terminal strategy
- Sequence rhythm

평균을 hard rule로 쓰지 않고 diagnostic prior로 유지한다.

### Level 3 — Retrieval / Candidate Ranking Weights
현재 state와 retrieved case의 적합도:
- dramatic function
- relationship state
- information policy
- debt state
- character goal
- episode position
- genre

### Level 4 — Dynamic Narrative Attention
작품/회차별로 중요한 Thread와 관계·정보 축의 가중치가 달라진다. 장기적으로는 work-specific / episode-specific dynamic weighting을 학습할 수 있다.

권장 진화:
`Explicit Rules → Measured Priors → Learned Weights → Dynamic Narrative Attention`

38작 6,357 Sequence와 714 EpisodePlan은 일반 LLM pretraining용 대규모 corpus가 아니라, retrieval scorer / ranker / critic / candidate selector 같은 작은 학습 시스템에 특히 유용한 외부 훈련 corpus가 될 수 있다.

---

## 14. 최종 상업 목적

일반 개인이 전문 작가실·프리프로덕션 팀의 일부 기능을 이용할 수 있도록 한다.

사용자 경험의 궁극 구조:
- Project / Story Bible
- Characters / Relationships / Threads
- Season / Series Architecture
- Episode 01..N
  - EpisodeSynopsisPlan
  - SequencePlan 01..K
  - ScenePlan
  - Beats
- Screenplay
- Storyboard
- Assets
- Production

제품 메시지의 핵심:
> **아이디어를 바로 영상으로 만드는 AI가 아니라, 아이디어를 이야기로 설계한 뒤 영상으로 만드는 AI.**

앞으로 연구와 제품화는 병렬로 진행한다. 분석 데이터 확대만 계속해 연구는 깊어지지만 제품이 나오지 않는 상태를 피한다.

---

## 15. 현재 최종 전달 artifacts

### Full DB — R21 FINAL SEALED
Filename:
`DB98_98WORK_STAGE04_38THICK_BOUNDARY_R1_38QUAL_EPPLAN_38WORK_CANONICAL_V03_R1_4WORK_DEEP_SEMANTIC_R2_CURRENT_AUTHORITY_CLEAN_R21_V9_20260818_FINAL_SEALED.zip`

SHA256:
`7c0cf924a5acd78d338df4f36a7626d14c290fbd6c9eadcf09bdc6ad1b8a1b49`

Fresh validation:
- status PASS
- files 25,914
- checksum errors 0
- CRC errors 0
- parse errors 0
- credential hits 0
- plans 714 / contexts 714 / profiles 38 / THICK 6,357 / R5 714 / R8 714

### New-session CURRENT-ONLY learning bundle
Filename:
`DRAMA_ANALYSIS_NEW_SESSION_CURRENT_ONLY_R21_38THICK_38EPPLAN_4WORK_DEEP_SEMANTIC_R2_20260818_FINAL_SEALED.zip`

SHA256:
`b932a186c195844b0c07537d4470c81df65eb12fcd621e78abf60b2a027f44e7`

Fresh validation:
- status PASS
- files 4,415
- checksum errors 0
- CRC errors 0
- parse errors 0
- required_missing 0
- historical current pointer files in learning path 0
- pairing DB SHA match true

이 learning bundle은 `00_READ_FIRST/README_FIRST.md`를 단일 시작점으로 사용한다.

---

## 16. 새 세션 부팅 순서

1. root `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`
2. `CURRENT_AUTHORITY_POINTER.json`
3. `DRAMA_ANALYSIS_SESSION_HANDOFF_R21_20260819.md`
4. `DRAMA_ANALYSIS_METHOD_CURRENT_R21_20260818.md`
5. V10.1 exact schema authority/registry
6. Sequence Boundary R1 rules
7. `DRAMA_ANALYSIS_EPISODE_PLAN_HANDOFF_MANUAL_R5_20260818.md`
8. current Deep Semantic / Thread / validators
9. 대상 작품을 고른 뒤에만 work_state / checkpoint / SOURCE를 연다.

새 작품 실행 체인:
`SOURCE/SourceLock → Q1~Q4 direct reading → Stage01 → Stage02+Boundary → Stage03 → Stage04 → post-boundary semantic re-audit if needed → THICK → EpisodePlanningContext → EpisodeSynopsisPlan → R5 → R8 → all current gates → individual package → DB integration → fresh extraction → update new-session bundle`.

Python은 의미를 생성하지 않는다.

---

## 17. 다음 세션의 최우선 작업

1. **현재 R21 상태를 다시 분석하는 데 시간을 쓰지 않는다.** 이 문서와 pointer를 current truth로 읽는다.
2. CT-13을 유리한 결과가 나올 때까지 반복하지 않는다. formal state는 UNDECLARED로 보존한다.
3. 다음 핵심 연구는 `N-1 only + retrieval → autonomous EpisodeSynopsisPlan → autonomous SequencePlans` blind forward test다.
4. 동시에 Retrieval Scaling의 preregistration을 작성한다.
5. 실험에서 DB size와 analysis depth를 분리한다.
6. generation quality뿐 아니라 originality/leakage와 cross-level congruence를 반드시 측정한다.
7. 성공 후 multi-episode rollout으로 넘어간다.

---

## 18. 반드시 보존할 과학적/감사 구분

- reverse-engineered EpisodePlan corpus canonicality ≠ autonomous causal-control proof.
- SequencePlan Blind Forward PASS_WITH_LIMITATIONS ≠ genre-general autonomous writer proof.
- CT-11 overall boundary reproduction failure ≠ cross-work retrieval effect가 0이라는 뜻이 아님.
- corpus averages / priors ≠ hard dramatic rules.
- retrieval similarity ≠ quality target.
- DB expansion 자체 ≠ 자동 성능 향상. scaling experiment로 검증해야 함.

이 구분을 잃으면 Literary OS가 연구 결과를 과장하거나, 데이터 평균을 기계적 창작 규칙으로 잘못 고정하게 된다.
