# 드라마 분석 결정·정정 로그 — 2026-07-12

이 문서는 과거 평가와 최신 규칙이 충돌할 때 왜 v2를 우선해야 하는지 설명한다.

## D-001 — 스키마 모방만으로 분석 완료를 인정하지 않는다

결정:

```text
형식 PASS와 내용 PASS를 분리한다.
```

근거:

- 템플릿 변수 잔류
- 동일 골격 반복
- metadata-derived CharacterArc
- 실제 원문에 없는 장면
- report/validation 모순

적용:

- 반게이밍 gate를 구조 gate와 동급으로 강제
- actual data > validator > report

## D-002 — Python은 의미 저작자가 아니다

결정:

```text
Python = extraction / serialization / validation / packaging
```

금지:

- keywords/theme 기반 SceneCard
- 회차 요약 기반 CharacterArc 복제
- sequence successor 기반 Edge 자동 생성
- 이전 화 마지막 장면 기반 CrossEdge 자동 생성

## D-003 — 작업 확장은 제출 단위만 확장한다

초기 안전 단위는 1~2회차였으나, 사용자의 요구에 따라 반시즌 제출을 실험했다.

결정:

```text
quarter 의미 저작
episode 잠금
half-season 제출
```

내부 독해 단위를 확대하지 않는다.

## D-004 — 내부 회차 PASS는 사용자 완료가 아니다

시티헌터 EP01에서 내부 체크포인트를 최종 완료처럼 보고해 중단한 문제가 있었다.

결정:

- SourceLock에 사용자 제출 범위를 기록
- 약속 범위가 끝나기 전 최종 보고 금지
- 회차 PASS는 internal ledger

## D-005 — LocalEdge는 동일 회차만

초기 GPT 패키지 일부에 회차 간 `gap=1 causal` edge가 LocalEdge에 들어갔다.

결정:

```text
LocalEdge: same episode / gap0 / causal
CrossEpisodeEdge: later episode / verified fan-in
```

## D-006 — Claude 초기 오탐 정정

Claude 1차 감사의 다음 지적은 재검증으로 철회됐다.

- GPT가 다른 작품을 분석했다
- 대량 scene dangling이 있다
- 작품 내용이 전반적으로 환각이다

정정 후 결론:

- 작품·장면 내용 일치
- 보강 후 의미 품질 수용 가능
- 핵심 결함은 계층 배치·일부 규약 정규화

## D-007 — GPT와 Claude의 핵심 스키마는 동일

초기 “GPT SequenceBlueprint가 더 풍부하다”는 평가를 정정한다.

실측:

```text
SequenceBlueprint 18키 동일
EpisodeArc 13키 동일
Stage03/04 핵심 계층 동일
```

수용 대상은 신규 필드가 아니라 GPT의 검증·증빙 method다.

## D-008 — GPT 검증 장치 수용

채택:

- SourceLock
- QuarterAudit
- Lineage/Quarantine
- FunctionalHoldout
- portable real validator
- fresh-extraction release audit

## D-009 — 동일 작품 판본 혼합 금지

장면 수·ordinal이 다른 Claude/GPT 판본은 계층별로 섞지 않는다.

결정:

```text
전량 유지 / 전량 교체 / 원문 기반 새 통합판
```

중 하나만 허용.

## D-010 — Stage04는 disposition 100% 후 완료

모든 PayoffCandidate는 다음 중 하나로 판정한다.

- promoted
- local/adjacent reclassification
- resolved within episode
- duplicate
- insufficient evidence
- source mismatch

미처리 후보가 있으면 Stage04 미완료.

## D-011 — 실제 validator만 인정

미리 작성한 FINAL_VALIDATION_REPORT를 읽고 PASS를 출력하는 stub를 금지한다.

validator는 파일을 직접 열어 다음을 재계산한다.

- schema/type
- count/coverage
- reference/participant
- edge/core
- Stage04 disposition
- anti-gaming

## D-012 — 기능 holdout은 제한적 증거

같은 프로젝트가 작성한 task/answer의 12/12 PASS는 유용하지만 외부 인간 블라인드 평가가 아니다.

판정명:

```text
PASS_LIMITED_HOLDOUT_NONBLINDED
```

과장 금지.

## D-013 — 결혼못하는남자 현재 count

패키지 내부 과거 strong-gate에는 1,249장면이 기록돼 있으나 현재 authored 전수 집계와 validation_v2는 1,250장면이다.

결정:

```text
current = 1,250
1,249 report = historical/superseded
```

## D-014 — 사용자 승인 전 CANONICAL 금지

현재 5작품은 강한 게이트를 통과했지만 상태는 PASS_CANDIDATE다.

```text
canonical_allowed = false
```

사용자의 명시적 승격 지시가 필요하다.

## D-015 — 신규 계층은 앵커 ablation 후

추가 분석 계층은 즉시 37작품에 확대하지 않는다.

```text
anchor work
→ baseline
→ ablation
→ false-positive audit
→ functional gain
→ versioned adoption
```

## 최신 권위

이 로그와 `docs/drama_analysis/*_V2` 문서가 초기 `docs/external/...v1` 문서보다 우선한다.
