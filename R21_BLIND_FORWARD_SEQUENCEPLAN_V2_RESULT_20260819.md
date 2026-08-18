# R21 Blind Forward SequencePlan V2 — 실행·평가 최종 보고서

**Date:** 2026-08-19 KST  
**Status:** `PASS_INTERNAL_BENCHMARK_WITH_LIMITATIONS`  
**Scientific class:** `INTERNAL_BLIND_FORWARD_ROBUSTNESS_BENCHMARK_NOT_INDEPENDENT_CAUSAL_CERTIFICATION`

## 연구 질문
현재 R21의 `N-1 state / PlanningContext / R5 / THICK / Boundary R1 / 38-work EpisodeSynopsisPlan case library`를 이용해 미래 target SOURCE 없이 다음 회차의 Sequence를 실제로 기획·구성·설계·창조할 수 있는가를 시험했다.

Arms:
- B_STATE_DIRECT: N-1 safe state에서 SequencePlan 직접 생성.
- C_HIERARCHICAL: 먼저 자율 EpisodeSynopsisPlanLite를 만든 뒤 SequencePlans 생성.
- D_RETRIEVAL_HIERARCHICAL: C + 서로 다른 작품 top-5 EpisodePlan retrieval을 기능적으로 추상화·재조합.

## 사전등록과 blind integrity
유효 target:
- 강남엄마따라잡기 EP09
- 굿캐스팅 EP09
- 녹두꽃 EP09

초기 뉴하트 EP09는 다른 target retrieval에서 target 정보가 노출된 cross-target contamination을 발견해 **생성 전에 폐기**하고 굿캐스팅으로 교체했다. 이후 모든 target episode를 retrieval corpus에서 전역 차단했다.

raw R5에 target 의미가 아니라 target artifact 경로/해시 문자열이 남아 최초 Blind Guard가 FAIL했으나, holdout 미공개 상태에서 `target_refs/source_hashes`를 제거한 blind-safe R5로 재봉인한 후 세 target 모두 PASS했다.

총 9개 generation output을 holdout 공개 전에 SHA256으로 freeze했다. 최종 fresh validation에서 generation freeze hash mismatch 0, schema missing 0, retrieval high-specificity story/event/dialogue copy 0이었다.

## 사전등록 rubric
100점:
- cutoff causal continuity 20
- target episode functional compatibility 25
- character/relationship congruence 15
- thread/debt selection 15
- Sequence structure/Boundary plausibility 15
- originality/leak integrity 10

의미 채점은 동일 GPT 세션이 holdout 공개 후 수행했으므로 independent blind causal proof가 아니라 internal robustness benchmark다.

## 결과

| Target | B direct | C hierarchical | D retrieval+hierarchical | D−B |
|---|---:|---:|---:|---:|
| 강남엄마따라잡기 EP09 | 71 | 76 | 77 | +6 |
| 굿캐스팅 EP09 | 77 | 82 | 82 | +5 |
| 녹두꽃 EP09 | 64 | 69 | 68 | +4 |

Aggregate:
- B median **71**, mean 70.67
- C median **76**, mean 75.67
- D median **77**, mean 75.67

Deltas:
- C−B median **+5**
- D−B median **+6**
- D−C median **+1**
- D >= B: **3/3 targets**

Preregistered pilot rule: `hard gates PASS + D median>=B+5 + D>=C + D not worse than B on >=2/3` → **PASS**.

## 결정론 진단
Mean absolute Sequence-count error:
- B **1.00**
- C **0.33**
- D **0.33**

Canonical thread exact F1:
- B **0.427**
- C **0.442**
- D **0.394**

Text-function proximity diagnostic, char 3-gram cosine:
- B **0.8054**
- C **0.8131**
- D **0.8118**

해석: EpisodePlan-first hierarchy가 Sequence 개수 감각과 전체 구조를 가장 명확하게 개선했다. 반면 retrieval의 순수 증분은 D−C +1에 그쳤고 exact thread F1은 오히려 하락하여, 현재 retrieval은 정확한 active-thread 선택까지는 충분히 정밀하지 않다.

## 작품별 핵심 발견
### 강남엄마따라잡기 EP09
수진의 동거 발각, 학교 압력, 민주-상원 동맹은 잘 이어갔고 D는 canonical k=8을 맞췄다. 하지만 정본 핵심인 `특강비/월세 압박 → 민주의 노래방 도우미 노동 → 상원의 비밀 고통 감지`라는 **고비용 행동 선택**을 세 arm 모두 생성하지 못했다.

### 굿캐스팅 EP09
가장 잘 맞았다. 6103 내부선, 장부, 서국환 방해, 석호 과거, 예은 가족압박을 안정적으로 이어갔고 C/D의 `증거 수렴 → 권한 반격 → 비공식 팀`이 실제 팀해체·장부 탈취 작전 기능과 상당히 호환됐다. 그러나 피철웅 살해/화이트칼라 표식과 예은의 강제 작전유출은 놓쳤다.

### 녹두꽃 EP09
가장 어려웠다. R21은 EP08 전주성 함락 뒤 `승리 후 통치 비용`을 선택했지만 정본은 `홍계훈 포격 → 이현 야간 저격 → 이강 미끼작전 → 이현 총상/형제 조우`로 즉시 물리 escalation을 선택했다. 현재 시스템은 **다음 escalation level 선택**이 병목이다.

## 이전 2026-08-11 Blind Forward와의 관계
이전 결과는 공주 A65/B84/C88, 결혼못하는남자 SequencePlan 86, leakage 0, scene 77→86, holdout 73, `PASS_WITH_LIMITATIONS`였다.

이번 86↔77을 직접 비교하면 안 된다. 작품·schema·rubric·격리 조건이 다르다. 이번에 새로 확인된 것은:
1. B→C +5 median — EpisodeSynopsisPlan-first hierarchy 양의 신호.
2. B→D +6 median — 전체 고도화 stack pilot PASS.
3. C→D +1 median — retrieval 자체 추가효과는 약함.
4. k error 1.00→0.33 — 구조 설계 개선.
5. high-specificity retrieval copy 0 — 표면 모방 없이 추상화 가능.

따라서 `반복할수록 무조건 점수가 상승했다`가 아니라 **어떤 계층이 개선을 만들고 어디가 병목인지 더 구체적으로 분해되었다**가 정확하다.

## 최종 판정
- SequencePlan V2 capability: `SUPPORTED_FOR_FURTHER_EXPERIMENT`
- EpisodeSynopsisPlan→SequencePlan hierarchical control: `POSITIVE_INTERNAL_SIGNAL`
- Retrieval-Augmented Sequence planning: `EXPERIMENTAL_WEAK_POSITIVE_NOT_YET_PROVEN`
- Retrieval scaling: `NOT_TESTED`
- Autonomous multi-episode rollout: `NOT_TESTED`
- Formal independent certification: `NOT_GRANTED`

## 다음 연구
1. Retrieval representation을 state/debt/function/escalation/relationship-transition 중심으로 개선.
2. 0/5/10/20/38 works retrieval scaling.
3. 같은 debt를 서로 다른 비용·비가역성으로 해결하는 High-cost choice candidate generator.
4. reflective/governance/social confrontation/physical peril 등의 escalation-level predictor.
5. 독립 blind scorer로 formal 재검증.
6. 성공 후 3-episode rollout.

**Research integrity:** holdout 공개 후 생성물을 수정하거나 재렌더하여 PASS를 추구하지 않았다. 유효 9개 생성물은 holdout 공개 전 freeze SHA와 최종 package에서 동일하다.
