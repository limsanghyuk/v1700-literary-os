# 26작 작품별 구조·의미 무결성 정밀 감사 — 2026-08-15

## 최종 판정

**구조 무결성: 26/26 PASS. 의미 독립성·exact/provenance·R5/R8도 26/26 기계 검증 PASS. 그러나 직접 SOURCE 표본과 필드 소유권을 포함한 심층 의미 검사에서는 9작 선택 보강 필요, 1작 추가 검토 필요가 확인됐다.**

- PASS_STRONG: 6작
- PASS_WITH_CAUTION: 10작
- REVIEW_REQUIRED: 1작
- REPAIR_REQUIRED: 9작

전체 상태는 `STRUCTURAL_INTEGRITY_PASS__DEEP_SEMANTIC_INTEGRITY_REPAIR_REQUIRED`이다. 기존 V9의 구조·해시·계보 정합성은 유지되지만, 26작 전체 의미 무결성이 완결됐다고 보기는 어렵다.

## 검사 범위

- 작품별 Stage01~04 exact schema / 회차·장면 / Sequence coverage / Edge / disposition / FullSeriesArc 구조 검사
- THICK Semantic Independence V3 strict-all
- THICK exact schema + SOURCE/provenance hash
- PlannerInput R5 / Runtime R8 parity
- Q25 4지표, Stage01 반복, cast 중복, Stage02 밀도, cast body 반복, SOURCE ref coverage
- 26작 각각 첫·중간·최종 THICK Sequence의 원문 직접 표본 대조(총 78표본) + 고위험 레코드 추가 점검

## 작품별 판정

| 작품 | 구조 | 의미 판정 |
|---|---|---|
| 101번째프로포즈 | PASS | REPAIR_REQUIRED |
| 가을동화 | PASS | PASS_STRONG |
| 강남엄마따라잡기 | PASS | REPAIR_REQUIRED |
| 개와늑대의시간 | PASS | REPAIR_REQUIRED |
| 건빵선생과별사탕 | PASS | PASS_STRONG |
| 검사프린세스 | PASS | PASS_WITH_CAUTION |
| 결혼못하는남자 | PASS | REPAIR_REQUIRED |
| 경성스캔들 | PASS | PASS_WITH_CAUTION |
| 공주가돌아왔다 | PASS | REVIEW_REQUIRED |
| 구해줘 | PASS | PASS_STRONG |
| 국희 | PASS | PASS_STRONG |
| 굿캐스팅 | PASS | PASS_WITH_CAUTION |
| 궁 | PASS | PASS_WITH_CAUTION |
| 그저바라보다가 | PASS | PASS_STRONG |
| 난폭한로맨스 | PASS | REPAIR_REQUIRED |
| 내여자친구는구미호 | PASS | PASS_WITH_CAUTION |
| 내이름은김삼순 | PASS | PASS_WITH_CAUTION |
| 너의목소리가들려 | PASS | REPAIR_REQUIRED |
| 녹두꽃 | PASS | REPAIR_REQUIRED |
| 뉴하트 | PASS | REPAIR_REQUIRED |
| 닥터챔프 | PASS | PASS_STRONG |
| 대물 | PASS | PASS_WITH_CAUTION |
| 더킹투하츠 | PASS | PASS_WITH_CAUTION |
| 도깨비 | PASS | REPAIR_REQUIRED |
| 돌아온일지매 | PASS | PASS_WITH_CAUTION |
| 드림 | PASS | PASS_WITH_CAUTION |

## REPAIR_REQUIRED 9작 — 대표 확인 결손

- `101번째프로포즈`: THICK cast에 원문 대사·지문 조각이 desire_or_function으로 남아 있음. info_shift 184건, plant/payoff 65건은 직접 SOURCE ref가 없음.
- `강남엄마따라잡기`: cast owner mismatch. EP09 S03의 윤수미 기능문이 실제 지영 행동을 설명. EP01 중복 주어도 잔존.
- `개와늑대의시간`: EP01 R01의 민기 기능문 등에서 원문 대사 조각이 cast 기능문으로 남고 EP08에도 지문·대사 복사형이 다수 존재.
- `결혼못하는남자`: EP01 S06 현규 기능문이 실제 유진의 병원 행동과 책임감을 설명.
- `난폭한로맨스`: EP09 q07의 박무열·유은재·강종희 기능문이 같은 시퀀스 요약을 공유한 뒤 suffix만 달라짐.
- `너의목소리가들려`: EP01 S01의 `청소년축/증언축/주변축` 같은 generic axis가 desire/function을 대신함. global cast body repeat 38.48%.
- `녹두꽃`: 일부 cast/info가 `관련 장면축/현장 비용/판단기준` 템플릿으로 남아 인물 고유 기능과 정보 변화가 희석됨.
- `뉴하트`: EP23 S08 info_shift에 `혜석:혜석 ... 이후 판단` 같은 결합 오류 및 후반 cast 장면요약형 잔존.
- `도깨비`: EP16 S05 cast가 여러 장면과 participation label을 합친 aggregate payload이며 info_shift도 `출발/도착/판단 축` 템플릿.

## REVIEW_REQUIRED

- `공주가돌아왔다`: 사건선은 대체로 맞지만 cast가 장면 요약형으로 작성된 비율이 높고 info_shift 48건이 직접 SOURCE ref 없이 구조 근거에 의존한다.

## 구조·계보 검사 합계

- 구조 검사: 26/26 PASS
- Semantic Independence V3 strict: 26/26 PASS
- exact/provenance: 26/26 PASS
- 전체: 3,883 THICK / 68,677 SOURCE refs / 19,415 hash checks / errors 0
- R5/R8: 26/26 PASS
- 직접독해 attestation 확인: 14작 / 과거 attestation 미복구 12작

## 핵심 교훈

**구조 PASS와 의미 무결성 PASS는 동일하지 않다.** 기존 validator는 스키마·참조·해시·exact reuse·동일 문자열 중복은 잘 잡지만, 인물 소유권 오귀속, 긴 템플릿 문장, 원문 대사 조각의 cast 기능문 혼입을 놓칠 수 있다.

향후 정본 게이트에 최소 다음을 추가해야 한다.

1. cast owner-congruence 검사
2. cast raw-dialogue/script-fragment 검사
3. first/middle/final direct-source sample gate
4. generic-axis / aggregate-payload 탐지
5. info_shift / plant_payoff direct-source grounding 진단

## 다음 조치

전면 재분석은 불필요하다. `REPAIR_REQUIRED 9작 → REVIEW_REQUIRED 1작` 순으로 문제 Sequence/필드만 원문 직접독해하여 선택 보강하고, 영향 THICK/R5/R8 및 hash를 재생성한 뒤 26작 전체 deep-semantic gate를 다시 닫는다.
