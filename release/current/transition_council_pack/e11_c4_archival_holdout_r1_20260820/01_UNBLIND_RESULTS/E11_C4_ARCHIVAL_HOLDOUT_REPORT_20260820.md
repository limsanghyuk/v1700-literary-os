# E11-C4 Archival Holdout 검증 보고서

Date: 2026-08-20  
Status: COMPLETE_INTERNAL_ARCHIVAL_HOLDOUT  
Claim boundary: E10에서 이미 동결된 미사용 E11 작품군을 이용한 archival holdout; 새 prospective run이나 promotion evidence가 아님

## 1. 표본과 봉인

- 작품: 개인의취향, 난폭한로맨스, 도깨비, 라이벌, 로망스, 미안하다사랑한다
- 대상: EP15, 총 56 Sequence
- 기존 E11 여섯 작품과 중복: 0
- pre-unblind freeze 검증: **PASS**
- holdout EpisodePlan/Arc 수: 12 files
- provider 호출: 0

기존 E10 controller 결정은 target EpisodePlan 공개 전에 이미 동결돼 있었다. 이번 실험에서는 그 결정의 completion/phase 신호를 C2 scope로 변환하고, 앞서 봉인한 A1/A2를 적용한 뒤에만 EpisodePlan을 공개했다.

## 2. 범위 분류 결과

| 지표 | C2 | C4(A1) |
|---|---:|---:|
| 정확도 | 44/56 (78.57%) | 45/56 (80.36%) |
| Ordinal MAE | 0.2321 | 0.2143 |
| L3 recall | 66.67% | 0.00% |
| L3 precision | 40.00% | N/A |

A1은 3건을 고쳤지만 2건을 새로 틀렸다(McNemar p=1.0000). 정확도와 MAE는 소폭 개선됐지만 효과가 작고, 실제 L3를 하나도 유지하지 못했다. **A1은 H1만 통과하고 필수 안전조건 H2를 위반했으므로 채택 실패다.**

실패 원인은 의미 규칙이 아니라 표현 규칙에 묶였기 때문이다. E11 이유 문장에는 `회차/axis/carrier + 완료/전환/확정`이 있었지만 E10의 같은 의미는 `목표가 완결`, `downstream objective class가 바뀜`, `단계가 끝남`으로 기록됐다.

## 3. 개입 경제성 결과

| 지표 | C2 | C4(A2) |
|---|---:|---:|
| material interventions | 11 | 11 |
| evaluable interventions | 11 | 11 |
| known valid / invalid | 10 / 1 | 10 / 1 |
| known activation precision | 90.91% | 90.91% |
| final Sequence material rewrites | 0 | 0 |

E10 controller가 이미 마지막 Sequence에서 rewrite 대신 close/log만 수행했기 때문에 A2가 제거할 개입은 0건이었다. **A2는 안전하지만 incremental benefit은 이 표본에서 재차 비활성화됐다.**

## 4. 가설 판정

- H1 정확도 증가 및 MAE 감소: **PASS, 단 1행 순개선이며 p=1.0000**
- H2 L3 recall 저하 0.10 이내: **FAIL** (66.67% → 0.00%)
- H3 final zero-value rewrite = 0: **PASS**, 단 C2도 이미 0
- H4 C4 total interventions < C2: **FAIL / NOT ACTIVATED**
- H5 stale-carrier 비열등: **NOT EVALUABLE**, E10에는 같은 정의의 행 단위 stale-carrier ledger가 없음

## 5. 결론

이 holdout에서는 이전 재분석의 81.63%→91.84% 개선 폭이 재현되지 않았다. 정확도는 78.57%→80.36%로 1행만 순개선됐고, A1은 L3 recall을 66.67%에서 0%로 떨어뜨렸다. 따라서 기존 A1을 controller 규칙으로 채택하면 안 된다.

다음 버전은 특정 단어를 찾는 규칙이 아니라 구조 필드로 판정해야 한다. `current carrier question answered`, `remaining sequences require a different objective class`, `final hook only`를 각각 명시적인 boolean evidence로 기록한 뒤 L3를 결정해야 한다. 이 변경은 A1을 수정하는 것이므로 새 A1-R2 실험으로 다시 봉인해야 한다.
