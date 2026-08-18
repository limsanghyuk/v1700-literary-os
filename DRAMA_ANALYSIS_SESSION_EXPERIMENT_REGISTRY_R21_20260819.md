# Drama Analysis / Literary OS — Session Experiment Registry R21

**Date:** 2026-08-19 KST  
**Status:** `CURRENT_SESSION_EXPERIMENT_REGISTRY_COMPLETE`  
**Scope:** 2026-08-18~19 GPT drama-analysis session plus prior experiments explicitly re-opened and used to set the next research direction.

이 문서는 세션 인계서의 요약보다 한 단계 더 엄격한 **실험·검증 전용 원장**이다. 새 세션은 무엇이 실제 과학 실험이고, 무엇이 품질 엔지니어링 검증이며, 무엇이 과거 실험의 재해석인지 혼동하지 않아야 한다.

## 0. 분류 원칙

- `SCIENTIFIC_EXPERIMENT`: 사전등록/대조군/종점/판정이 있는 실험.
- `ROBUSTNESS_DIAGNOSTIC`: 과학적 효용 신호를 보지만 독립성 등 formal gate를 충족하지 않아 공식 PASS를 인증하지 않는 진단.
- `ENGINEERING_VALIDATION`: 데이터·스키마·provenance·semantic quality·fresh extraction 검증. 인과 효과를 주장하지 않는다.
- `HISTORICAL_EVIDENCE_REOPENED`: 이번 세션에서 새로 실행한 것이 아니라 기존 허브 결과를 다시 읽고 다음 연구 설계에 사용한 증거.

---

## 1. CT-13 R3 — EpisodeSynopsisPlan incremental utility

### 분류
`SCIENTIFIC_EXPERIMENT + ROBUSTNESS_DIAGNOSTIC`

### 연구 질문
좋은 work-specific `EpisodeSynopsisPlan`을 renderer에 제공하면 B(회차 분석층) 또는 N(불일치 계획)보다 유예 정책, debt 처리, 목표 상태 설계가 좋아지는가?

### 설계
- 12 anchor episodes.
- Arms: A / B / C / N.
- 48 renderer inputs / 48 sealed outputs.
- 외부 Claude renderer: 6 isolated sessions × 8 inputs.
- renderer는 target SOURCE 및 reverse-engineered target plan에 접근하지 않음.
- N arm은 mismatched plan을 control로 사용.
- renderer output freeze manifest SHA256: `b9a7c420dde4c58d2c7469272aa230fb220f0cc4784e1859a83b272b804774e0`.

### Renderer 단계 결과
- 48/48 outputs.
- schema violation 0.
- sealed manifest PASS.
- 주의: N arm renderer가 일부 경우 불일치 계획의 구조를 현재 작품에 이식해 C vs N 대비를 보수적으로 만들 가능성이 있음.
- renderer는 모두 Claude 계열이므로 scorer 계열/세션 독립성이 중요함.

### 이번 GPT 세션에서 실행한 3-rubric robustness diagnostic
동일 GPT 세션 안에서 strict / semantic-lenient / conservative 세 가지 rubric pass로 재판정했다. 이것은 **독립 3인 scorer가 아니다**.

C vs B:
- P1: 8 positive / 0 negative / 4 ties, two-sided p = `0.0078125`
- P2: 11 / 0 / 1, p = `0.0009765625`
- P3: 12 / 0 / 0, p = `0.00048828125`
- three-pass direction agreement = `0.9722222222`

C vs N:
- P1: 10 / 0 / 2, p = `0.001953125`
- P2: 10 / 0 / 2, p = `0.001953125`
- P3: 12 / 0 / 0, p = `0.00048828125`
- direction agreement = `1.0`

P4 diagnostic:
- explicit high-specificity post-N leakage signals = `0`.

### Formal 판정
- numeric PASS-like conditions: 충족 패턴.
- formal preregistered verdict: **`UNDECLARED`**.
- 이유: preregistration §7의 genuinely separated three blind scorers 조건을 현재 단일 GPT session이 충족하지 못함.
- reverse-engineered 38-work EpisodeSynopsisPlan corpus: `CANONICAL 유지`.
- autonomous forward-generation control: `EXPERIMENTAL_HOLD`.

### 무엇을 증명하지 않았는가
CT-13 R3는 **좋은 Plan이 주어졌을 때 renderer utility**를 시험한다. N-1 상태만 보고 planner가 같은 품질의 EpisodeSynopsisPlan을 스스로 생성할 수 있는지는 시험하지 않았다.

### 권위 문서
- `CT13_R3_FINAL_RESEARCH_CLOSURE_R1_20260818.md`
- `CT13_R3_FINAL_RESEARCH_CLOSURE_R1_20260818.json`
- engine repo: `docs/tracks/confirmatory/CT13_R3_RENDERER_STAGE_REPORT_20260818.md`
- engine repo의 CT-13 R3 preregistration / execution kit / sealed renderer artifacts가 원 실험 계보의 권위다.

---

## 2. 34→38 EpisodeSynopsisPlan corpus construction / source audit

### 분류
`ENGINEERING_VALIDATION`, **causal experiment 아님**.

### 방법
- 기존 34 CANONICAL works에서 EpisodePlanningContext + reverse-engineered EpisodeSynopsisPlan을 저작.
- 이미 방영된 Episode N을 읽기 전에 N-1 planning context를 freeze하는 정보 절단 규칙 사용.
- mass authoring 후보에서 formulaic WHY, truncation, final-episode false-next-episode, schema drift를 수리.
- 34작 당시 656 plans에 대해 102 episodes = 34 works × FIRST/MID/FINAL raw-SOURCE stratified audit.

### 결과
- raw-SOURCE audit: 102/102 PASS.
- SOURCE anchors: 583.
- rewrite_required: 0.
- 이후 외부 4작을 기존 work identity로 강화/승격하여 38작 / 714 EpisodeSynopsisPlan / 6,357 allocations.

### 정직성 제한
656 plan 단계에서 656 raw scripts를 모두 처음부터 다시 읽은 것이 아니라 SOURCE-grounded Stage02/THICK/R5/EpisodeArc semantics에서 reverse-engineer하고 102 episode raw-SOURCE 표본감사를 수행했다.

---

## 3. External 4-work equal-quality / Deep Semantic R2 integration

### 분류
`ENGINEERING_VALIDATION`.

### 대상
- 개인의취향
- 수호천사
- 미안하다사랑한다
- 미생

이 4작은 Stage01–04 98작에 이미 존재했으므로 total works는 98→102가 아니다. CANONICAL THICK/EpisodePlan cohort가 34→38로 승격됐다.

### 방법
- 외부 package를 staging에서 현재 38작 정본과 SHA/structure/semantic contract 비교.
- Stage01–04 identity / Sequence membership 보존 확인.
- THICK semantic prose 강화.
- selected EpisodePlan prose/debt parity 강화.
- affected R5/R8 rebuild.
- same blocking validators를 기존 34작과 동일하게 적용.
- non-target 34-work invariance audit.

### 실제 발견 결손
`미안하다사랑한다 EP16`의 inherited debt `MISA_MUHYEOK_MINJU_REVENGE_SEDUCTION`이 paid/escalated/carried/retired 어느 ledger에도 없어서 EP6 HARD violation을 일으킴. SOURCE-grounded terminal state와 final THICK를 대조해 `PAID`로 결산.

### 결과
- Stage02↔THICK 6,357=6,357 exact membership.
- Exact/Provenance: 6,357 records / 147,633 SOURCE refs / 31,785 hash checks / errors 0.
- Semantic V3: 38/38 PASS.
- Owner/Grounding blocking 0.
- Depth blocking 0.
- Thread R2 38/38 PASS.
- Subplot distinct-event duplicate 0.
- Deep Semantic 38/38 PASS.
- EpisodePlan 714 / HARD 0.
- R5/R8 714/714.
- artifact hash 2,142/2,142 PASS.
- non-target 34-work semantic artifact mismatch 0.

### Validator false positive
Deep Semantic에서 blocking 1이 한 번 발생했으나 데이터 결함이 아니라 과거 29-work manual SOURCE registry를 기본값으로 읽은 stale-default 문제였다. current 38-work registry를 명시하여 38/38 PASS 재현. 이후 실행 계약은 current registry 명시를 요구한다.

---

## 4. Sequence Boundary R1 qualification

### 분류
`ENGINEERING / MEASUREMENT REPAIR`.

### 배경
CT-11/11B/11C의 Sequence boundary prediction 실패를 곧바로 모델 능력 부족으로 해석할 수 없게 만든 CT-12A의 endpoint contamination 경보를 반영했다.

### Sequence 정의
`하나의 지배적 dramatic transaction이 진행되는 최소 연속 Scene 묶음.`

### 판정법
- LEFT TERMINAL
- RIGHT RESET
- ±1 minimality
- B1~B7 reason code

### 대표 수리
- 경성스캔들: Stage02 150 / THICK 138 → 145 / 145.
- 개와늑대의시간: 143 / 132 → 132 / 132, SOURCE 직접판정.
- 결혼못하는남자 EP04: 기계적 12 equal-like sequences → 13.
- 그저바라보다가: `_SEQxx` vs `_Sxx` 16건은 membership exact인 alias-only diagnostic.

### 결과
38/38 CANONICAL cohort Boundary-qualified, Stage02=THICK 6,357=6,357.

---

## 5. R21 packaging / fresh extraction / authority cleanup

### 분류
`ENGINEERING_VALIDATION`.

### 목적
실험 효과를 측정하는 것이 아니라 현재 38작 정본과 새 세션 학습 번들이 실제로 재현 가능하고 과거 26/34-work current pointer에 의해 오염되지 않도록 봉인하는 것.

### 결과
Final DB:
- SHA256 `7c0cf924a5acd78d338df4f36a7626d14c290fbd6c9eadcf09bdc6ad1b8a1b49`
- fresh extraction PASS.

Current-only new-session bundle:
- SHA256 `b932a186c195844b0c07537d4470c81df65eb12fcd621e78abf60b2a027f44e7`
- fresh extraction PASS.
- historical current pointers in learning path: 0.
- DB pairing SHA match: true.

---

# 6. 이번 세션에서 다시 읽고 다음 연구에 사용한 기존 실험

아래는 **이번 세션에서 새로 실행한 것이 아니라**, 엔진 허브의 기존 결과를 재대조하여 현재 로드맵의 근거로 사용한 것이다.

## 6.1 2026-08-11 Blind Forward SequencePlan

공주가돌아왔다 EP01–08→EP09:
- A high-level 65
- B + Stage01–04 84
- C + THICK + PlannerInput 88
- C−A +23 / C−B +4

결혼못하는남자 EP01–08→EP09:
- candidates 8 → selected 6 / deferred 2
- SequencePlan quality 86
- future leakage 0
- scene draft 77 → critic/revision 86
- holdout compatibility 73, gate 70
- overall PASS / scientific interpretation `PASS_WITH_LIMITATIONS`

한계: 2 works, model-pretraining knowledge 완전 배제 불가, multi-genre/generalization/rollout 미증명.

## 6.2 CT-07 / CT-07R / CT-08 family — representation depth

- CT-07: THICK representation에서 `r_L2G=0.807`, depth effect +0.74 dominant signal.
- CT-07R: r_T=0.817, 당시 PASS이나 이후 계측기 검증 이슈 때문에 판정 강도 주의.
- CT-08A: Δ_true +1.479이었으나 scorer agreement gate 미달로 INVALID.
- CT-08A-R / CT-08B: Δ_true는 반복 양수였지만 scorer agreement/measurement bottleneck 때문에 formal 선언 보류.

현재 해석: **분석 깊이가 생성 조향에 기여한다는 방향 신호는 반복됐지만, 일부 확증 판정은 계측기 독립성 문제로 제한된다.**

## 6.3 CT-11 / 11B / 11C — cross-work retrieval and boundary

CT-11:
- overall boundary reproduction: NOT ESTABLISHED.
- U F1±1 0.465 / C 0.471.
- main endpoint max(B,C)−U = +0.007 < +0.10.
- 그러나 `C−B = +0.070`, preregistered +0.05 auxiliary threshold 충족.
- C의 |Δk| 1.67 vs A/B/N 3.22 → cross-work examples가 Sequence count 감각을 크게 교정하는 신호.

CT-11B:
- k estimation → boundary two-stage도 overall gate 미달.

CT-11C:
- deterministic k prior가 강함; regular layer에서 generated boundary가 해롭고 irregular layer에서만 우세 신호.

## 6.4 CT-12A — boundary endpoint reliability alarm
- independent annotator R1 F1±1 = 0.737.
- annotator vs canonical R2 = 0.426.
- uniform split vs canonical = 0.704.
- 결론: canonical boundary endpoint contamination 위험. CT-11 계열을 단순 '모델 능력 부족'으로 해석하지 않음.

---

# 7. 이 실험군에서 도출된 현재 연구 프로그램

다음 우선순위는 CT-13 반복이 아니다.

1. `Retrieval Scaling`: no retrieval / 5 / 10 / 20 / 38 works.
2. `Representation Depth Scaling`: thin / THICK / THICK+Boundary / THICK+Boundary+EpisodePlan.
3. `Blind Forward EpisodeSynopsisPlan`: N-1만 보고 target Plan 자율 생성.
4. `Hierarchical Planning`: generated EpisodeSynopsisPlan → SequencePlans → ScenePlans → Beats.
5. `Multi-Episode Rollout`: generated N state를 N+1 planning state로 사용.
6. `Originality/Leakage`: retrieved 사례의 고유 사건/대사/설정 복제를 방지하고 기능적 문법만 재조합하는지 평가.
7. `Narrative Weight Learning`: hard constraints / learned priors / retrieval weights / dynamic narrative attention을 실험으로 측정.

최종 상업적 연결:
`Idea → EpisodeSynopsisPlan → SequencePlan → Scene → Beat → Screenplay → Storyboard → Shot/Production Assets → Video`.

---

# 8. 증거 보존 규칙

- raw sealed renderer outputs를 새로 고쳐 favorable result를 만들지 않는다.
- 과학적 실험 결과와 engineering validation을 혼동하지 않는다.
- same-session repeated scoring은 independent scorers로 재명명하지 않는다.
- historical experiments는 original `literary-os/docs/tracks/confirmatory/` 문서를 권위로 한다.
- v1700은 current drama corpus/method/release authority, literary-os는 CT preregistration/engine experiment authority다.
