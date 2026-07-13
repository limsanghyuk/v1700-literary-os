# 드라마 분석 권위 인덱스

Document status: **AUTHORITATIVE ENTRYPOINT**  
Version: 2.2  
Updated: 2026-07-13 (Asia/Seoul)

이 디렉터리는 GPT가 한국 드라마 원본을 직접 읽고 Stage01~04 분석 산출물을 만드는 데 필요한 최신 권위 문서군이다. 새 대화창·새 세션·새 모델은 다른 과거 문서보다 이 파일을 먼저 읽어야 한다.

## 권위 우선순위

충돌이 있을 때 아래 순서가 우선한다.

1. `CURRENT_AUTHORITY_SNAPSHOT_2026-07-13.md`
2. `DRAMA_ANALYSIS_OPERATING_MANUAL_V2.md`
3. `SCHEMA_CONTRACTS_V2.md`
4. `VALIDATION_RELEASE_PROTOCOL_V2.md`
5. `GPT_CLAUDE_ALIGNMENT_AND_INGESTION_V1.md`
6. `WORK_CATALOG_2026-07-12.md`
7. `NEXT_SESSION_BOOTSTRAP_CHECKLIST.md`
8. `PROTOCOL_V2.json` 및 `WORK_STATUS_2026-07-12.json`
9. 최신 `docs/sessions/*drama*/README.md`

`docs/external/claude_drama_analysis_method_manual_stage01_04_v1.md`는 중요한 역사·원형 문서이지만, 초기 감사의 오탐과 이후 규격 정정이 포함되기 전 문서다. v1과 이 디렉터리의 최신 문서가 충돌하면 **이 디렉터리의 최신 문서**를 적용한다.

## 새 세션의 5분 시작 절차

```text
1. 이 README를 읽는다.
2. CURRENT_AUTHORITY_SNAPSHOT_2026-07-13.md를 읽는다.
3. OPERATING_MANUAL_V2의 작업 단위와 Python 경계를 읽는다.
4. SCHEMA_CONTRACTS_V2의 키셋·enum·ID 규칙을 로드한다.
5. VALIDATION_RELEASE_PROTOCOL_V2의 fail-closed 게이트를 로드한다.
6. WORK_STATUS에서 완료한 7작품을 제외한다.
7. 한국드라마04 원본 목록을 조사하여 다음 작품 1편을 선정한다.
8. SourceLock v2를 만들고 전체 회차·장면·반시즌 작업량을 잠근다.
9. EP01 Q1부터 직접독해를 시작한다.
```

## 최신 실행 단위

```text
의미 저작 최소 단위: quarter
잠금 단위: episode
기본 사용자 제출 단위: half-season
안전 축소 제출 단위: 2 episodes
최종 통합 단위: full series
```

반시즌 제출은 여러 회차를 한 번에 자동 생성한다는 뜻이 아니다. 내부에서는 반드시 다음 순서를 유지한다.

```text
EP01 Q1→Q2→Q3→Q4→회차 게이트
→ EP02 Q1→Q2→Q3→Q4→회차 게이트
→ ...
→ 전반부 통합 게이트
```

내부 회차 PASS는 사용자 작업 완료가 아니다. 약속한 전반부·후반부 범위가 끝날 때만 사용자에게 완료를 보고한다.

## 절대 금지

- Python 또는 템플릿 함수로 의미 필드 생성
- 키워드 조각을 분석문처럼 확장
- 회차 요약을 인물별 CharacterArc에 복사
- `LocalEdge`에 회차 간 연결 저장
- 전 회차 독해 전 Stage04 확정
- 실제 데이터를 검사하지 않는 stub validator
- 사람용 PASS 보고서로 데이터 FAIL을 덮기
- 사용자 승인 없이 `CANONICAL` 승격

## 현재 완료된 GPT 분석 작품

- 101번째프로포즈
- 결혼못하는남자
- 공주가돌아왔다
- 시티헌터
- 내여자친구는구미호
- 좋은사람
- 파라다이스목장

누적 상태:

```text
7작품 / 115회 / 7,518 SceneCard / 1,043 SequenceBlueprint
115 EpisodeArc / 787 CharacterArc / 757 RelationshipArc
1,634 LocalEdge / 580 PayoffCandidate / 301 CrossEpisodeEdge
460 QuarterAudit / 7 FullSeriesArc
```

모두 authoritative v3 권위 계약으로 fresh extraction·ZIP CRC·내부 SHA·휴대형 validator를 재검증했으며 현재 지위는 `PASS_CANDIDATE`다. 사용자 승인 전 `CANONICAL`로 승격하지 않는다. 상세 수량·패키지 SHA256·보강 이력은 `WORK_CATALOG_2026-07-12.md`와 `WORK_STATUS_2026-07-12.json`을 참조한다.

## 현재 최신 허브 기준

```text
latest authoritative drama commit:
555530412ddda6ab623102778e54c79db37156c9

latest complete handoff:
docs/sessions/2026-07-12_drama_7work_authoritative_v3/README.md

latest authority refresh:
docs/sessions/2026-07-13_drama_analysis_authority_refresh/README.md
```

대화 기록이 허브와 충돌하면, 검증된 허브 authoritative v3 상태를 우선한다. 특히 파라다이스목장은 허브 기준으로 EP09~EP16 직접독해와 Stage04까지 완료된 전 시즌 `PASS_CANDIDATE`다.

## 다음 정상 작업

한국드라마04에서 위 7작품과 겹치지 않는 다음 작품 1편을 선정한다. 원본 분리 상태, 장면 경계 안정성, 반시즌 균형, 장르 확장성, Claude 동일 작품 비교 가능성을 평가한 뒤 SourceLock을 만들고 전반부 분석을 시작한다.

정확한 next pointer:

```text
SELECT_NEXT_UNANALYZED_WORK_FROM_한국드라마04
→ SOURCE_ARCHIVE_INVENTORY
→ SourceLock v2
→ EP01 Q1 직접독해
```

## 보고 원칙

개발자 보고는 최소화한다.

```text
작품 / 범위 / 레코드 수 / 최종 gate / 오류·경고 / SHA256 / 다음 진입점
```

분석 과정의 상세 판단과 보강 이력은 패키지 내부 ledger·validation·provenance에 저장하고, 대화 보고에는 핵심만 제시한다.
