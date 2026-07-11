# 새 대화창 드라마 분석 부트스트랩 체크리스트

Updated: 2026-07-12  
Purpose: 과거 대화를 보지 못하는 새 세션이 즉시 다음 작품 분석을 시작하기 위한 최소 실행 순서

## A. 문서 로드

반드시 이 순서로 읽는다.

```text
1. docs/drama_analysis/README.md
2. DRAMA_ANALYSIS_OPERATING_MANUAL_V2.md
3. SCHEMA_CONTRACTS_V2.md
4. VALIDATION_RELEASE_PROTOCOL_V2.md
5. GPT_CLAUDE_ALIGNMENT_AND_INGESTION_V1.md
6. WORK_CATALOG_2026-07-12.md
7. 최신 docs/sessions/*_drama_analysis_handoff/README.md
```

읽은 뒤 다음 내용을 스스로 확인한다.

- 완료 작품 5편
- Stage01~04 계층
- quarter/episode/half-season/full-series 단위
- Python 의미 생성 금지
- LocalEdge와 CrossEpisodeEdge 차이
- 사용자 승인 전 CANONICAL 금지

## B. 현재 상태 확인

`WORK_STATUS_2026-07-12.json`을 읽고 완료 작품을 제외한다.

제외:

```text
101번째프로포즈
결혼못하는남자
공주가돌아왔다
시티헌터
내여자친구는구미호
```

현재 next:

```text
한국드라마04에서 다음 미분석 작품 1편 선정
```

## C. 원본 archive 조사

1. 한국드라마04 ZIP 존재 확인
2. 내부 작품 ZIP 목록 추출
3. 완료 작품 제외
4. 후보별 회차 파일 수 확인
5. 파일 인코딩 복원 시험
6. 장면 경계 탐지 시험
7. 총 장면 수·전후반 균형 계산
8. 장르·Claude 동일 작품 여부 확인

작품 선정 점수 예:

```text
source completeness      0~5
scene boundary stability 0~5
half balance             0~3
genre diversification    0~3
same-title benchmark     0~2
```

최고점 작품을 선정하되, 자동 점수보다 실제 원본 가독성을 우선한다.

## D. SourceLock 생성

Stage01 전에 다음을 잠근다.

```text
work_id
episodes_total
source archive SHA256
episode file SHA256
encoding
scene boundary policy
canonical scene count per episode
source marker anomaly
quarter ranges
first half / second half scene totals
direct_reading_required true
python_semantic_generation false
raw_script_exported false
status SOURCE_LOCKED_READY_FOR_EP01_Q1
next EP01_Q1
```

### 장면 번호 주의

원본 marker가 중복·결번·역순이면:

```text
scene_no = 등장 순서 ordinal
source_marker_no = 원본 값 보존
```

원본 marker가 없으면 재현 가능한 블록 경계 규칙을 사용한다.

## E. 사용자 초기 보고

선정 직후 한 번만 간단히 보고한다.

```text
선정 작품
회차 수
총 장면 수
전반부/후반부 장면 수
경계 정책
선정 이유
다음 = EP01 Q1
```

이후 내부 회차 PASS마다 완료 보고하지 않는다.

## F. 전반부 실행

각 회차:

```text
Q1 직접독해 → Stage01 → QuarterGate
Q2 직접독해 → Stage01 → QuarterGate
Q3 직접독해 → Stage01 → QuarterGate
Q4 직접독해 → Stage01 → QuarterGate
→ Stage02 회차 재분절
→ EpisodeArc/CharacterArc/RelationshipArc/LocalEdge/PayoffCandidate
→ EpisodeGate
```

모든 전반부 회차 후:

```text
HalfSeasonGate
→ fresh extraction
→ ZIP CRC
→ SHA256SUMS
→ validator rerun
→ PASS_CANDIDATE_FIRST_HALF
```

## G. 후반부 실행

전반부와 같은 방식으로 후반부를 완료한다.

```text
PASS_CANDIDATE_SECOND_HALF
```

후반부 분석 중 전반부 후보의 회수 가능성을 메모하되 CrossEpisodeEdge를 조기 확정하지 않는다.

## H. Stage04 실행

전 시즌 Stage01~03 완료 후:

```text
PayoffCandidate 전수 목록
→ 실제 후속 장면 대조
→ disposition 100%
→ CrossEpisodeEdge 승격
→ FullSeriesArc
→ FullSeriesGate
```

미처리 candidate 1건이라도 있으면 완료가 아니다.

## I. 최종 패키지

필수:

```text
README
SourceLock
Stage01~04 data
QuarterAudit
CandidateDisposition ledger
real validator
validation result
functional holdout
provenance/lineage
FINAL_MANIFEST
SHA256SUMS
reports
```

최종 판정:

```text
PASS_CANDIDATE_FULL_SERIES_STAGE01_04
canonical_allowed false
```

## J. 세션 중단 시 handoff

세션 한도·오류로 중단될 경우 다음을 허브에 남긴다.

```text
last_locked_episode
last_locked_quarter
current package paths
source lock path
validation state
known defects
next exact action
superseded files
```

“작업 중” 같은 모호한 표현을 금지한다.

좋은 예:

```text
EP06 Q4 LOCKED_PASS
EP06 EpisodeGate PASS
EP07 Q1 not started
next = read EP07 scenes 1~18
```

## K. 새 세션에 그대로 전달할 명령문

```text
개발자 허브의 docs/drama_analysis/README.md를 시작점으로 v2 문서를 전부 읽고 적용하라.
WORK_STATUS에서 완료 작품 5편을 제외하라.
한국드라마04의 남은 작품을 조사해 원본 안정성이 가장 높은 1편을 선정하라.
SourceLock v2와 전·후반 계획을 만들고 EP01 Q1부터 직접독해하라.
Python은 추출·직렬화·검증·패키징에만 사용하라.
내부 회차 체크포인트에서 사용자 완료 보고를 하지 말고 전반부 전체까지 순차 진행하라.
```

## L. 최종 자체 확인

작업 시작 전 다음 질문에 전부 “예”여야 한다.

```text
[ ] 이미 완료한 작품을 제외했는가
[ ] SourceLock이 있는가
[ ] 장면 경계 정책이 재현 가능한가
[ ] quarter 범위가 정해졌는가
[ ] Python 의미 생성이 금지됐는가
[ ] LocalEdge는 동일 회차만 허용하는가
[ ] Stage04는 전 시즌 뒤인가
[ ] 사용자 제출 단위를 기억하는가
[ ] 실제 validator가 준비됐는가
[ ] 상태를 PASS_CANDIDATE로 제한하는가
```
