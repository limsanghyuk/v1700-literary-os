# 한국 드라마 분석·저작·데이터화 End-to-End 실행 표준 R21 — CURRENT 2026-08-18

이 문서는 **새 GPT 세션이 기존 대화 내용을 몰라도** 새로운 한국 드라마 한 작품을 선정하고,
원본 대본을 직접 읽어 분석·저작·검증·데이터화·DB 편입까지 마무리하기 위한 현재 실행 기준이다.

## 0. 절대 권위와 충돌 처리

권위 우선순위:

`SOURCE + SourceLock > V10.1 exact schema authority > R21 current method > Boundary R1 > current THICK/Deep Semantic rules > EpisodePlan R5 > current validators > historical reports`

과거 pre-R21 cohort 문서, 중간 CT-13 상태 문구, R1~R19 pointer는 역사 증거일 뿐 current 규칙이 아니다.

현재 수치:
- Stage01–04: 98 works
- 97 V10.1-equivalent + 1 SOURCE_HOLD
- CANONICAL THICK/Boundary/EpisodePlan: 38 works
- Stage02=THICK: 6,357
- EpisodeSynopsisPlan: 714
- R5: 714
- R8: 714 / 46,078 runtime scenes
- DB numeric family: V9
- Stage01–04 schema authority name: V10.1
- connectivity/current documentation: R21

## 1. 새 작품 선정

1. `AUTHORED_WORK_INDEX_V24.json`에서 기존 작품 여부를 확인한다.
2. 이미 존재하는 작품이면 신규 분석이 아니라 replacement/reinforcement lineage 규칙을 적용한다.
3. 새 작품이면 원본 전체 회차의 존재·중복·결번·인코딩·부속파일을 먼저 조사한다.
4. SOURCE_HOLD가 있으면 fail-closed한다. 결손 원본을 추정으로 메우지 않는다.

## 2. SourceFormatAudit + SourceLock

분석 전에:
- 원본 파일명
- 원본/정규화 저장본 SHA256
- 인코딩
- 회차 대응
- canonical scene ordinal
- 비정본 제외 파일
- numbering anomaly
- alignment
을 고정한다.

SourceLock은 의미 데이터가 아니라 분석 원본의 신원을 고정하는 증거 계층이다.

## 3. 순차 직접독해

- 회차를 순서대로 읽는다.
- 한 회차는 Q1→Q2→Q3→Q4 순서로 직접독해한다.
- 최대 8개 연속 회차를 하나의 Block으로 운영한다.
- 고정 Sequence 개수 quota는 없다.
- 각 의미 단위는 원자적으로 저장하고 checkpoint를 남긴다.
- Python으로 의미 문장을 생성하지 않는다.

## 4. Stage01 — SceneCard

SOURCE를 직접 읽어 SceneCard exact 9키를 저작한다.
장면 경계, 사건, 행동, 감정/관계/정보 변화가 실제 원문에 근거해야 한다.
Python은 scene split 후보·해시·직렬화·검사까지만 허용한다.

## 5. Stage02 — SequenceBlueprint + Boundary R1

Sequence는 **하나의 지배적 dramatic transaction이 진행되는 최소 연속 Scene 묶음**이다.

경계 판정:
- LEFT TERMINAL
- RIGHT RESET
- ±1 minimality
- B1~B7 reason code

금지:
- 같은 장소라서 묶기/나누기
- 동일 Scene 수 등분
- 평균 Sequence 개수 맞추기
- 3 Sequence hard cap
- THICK에서 Stage02를 조용히 재분할

Stage02 exact 18키를 유지하고 BoundaryEvidence는 append-only 증거로 둔다.

## 6. Stage03 — episode semantic ledger

현재 exact 계약:
- EpisodeArc 13키
- CharacterArc 8키
- RelationshipArc 9키
- LocalEdge 12키
- PayoffCandidate 7키

LocalEdge는 반드시:
- 동일 회차
- causal
- `gap_episodes == 0`

회차를 넘는 인과/회수 연결은 Stage04 CrossEpisodeEdge로 보낸다.

## 7. Stage04 — whole-series fan-in

전 회차 분석 후:
- CandidateDisposition
- CrossEpisodeEdge
- FullSeriesArc 17키
를 직접 SOURCE 의미에 근거해 저작한다.

Stage04는 장거리 payoff/callback/continuity를 관리한다.

## 8. Boundary 변경 후 Stage03/04 재감사 — HARD

Stage02 membership을 바꿨다면 반드시:
1. CharacterArc 의미 귀속
2. RelationshipArc 변화
3. LocalEdge 원인→결과
4. PayoffCandidate plant/payoff
5. CrossEpisodeEdge
6. EpisodeArc turning/act span
을 SOURCE로 다시 의미감사한다.

수정할 필요가 없는 경우도 `NO_CHANGE_REQUIRED` 근거를 남긴다.
“seq_id를 직접 참조하지 않는다”는 이유만으로 영향 없음 판정을 하지 않는다.

## 9. THICK — 독립 의미 저작

THICK는 Stage02를 복사해 길게 만드는 계층이 아니다.
SOURCE를 다시 읽어 Sequence의 기능·정보·인물·관계·plant/payoff·thread를 독립 저작한다.

Blocking:
- Stage02 event exact copy
- cast 기능 복사
- generic cast
- 이름만 바꾼 stock function
- 의미 없는 template 반복

Thread는 실제 PLANT/HOOK에서 생성하고,
CONTINUE/ESCALATION/CALLBACK/REACTIVATION/REVERSAL/PAYOFF는 동일 durable `thread_id`를 재사용한다.

## 10. EpisodePlanningContext + EpisodeSynopsisPlan

이미 방영된 작품:
1. N을 읽기 전에 N-1 cutoff로 PlanningContext를 freeze한다.
2. N SOURCE 분석을 끝낸 후 reverse-engineered EpisodeSynopsisPlan을 저작한다.
3. `why now / deferred / debt / terminal / exit-state / Sequence ownership`을 직접 설명한다.

EpisodePlan은 EpisodeArc 요약이 아니다.
현재 schema는 `EpisodeSynopsisPlan.v0.3-r1`.

## 11. R5 PlannerInput

Episode N의 R5는 **N-1까지의 상태만 사용**한다.
미래정보, target 이후 payoff 사실을 금지한다.

## 12. R8 Runtime

R8은 current final THICK + same-episode R5를 deterministic projection한다.
THICK/Plan 의미가 변하면 affected R5/R8을 재생성한다.

## 13. 작품 전체 검증 순서

반드시 다음 순서로 닫는다.

1. Stage01–04 V10.1 equalization
2. Boundary partition/parity
3. THICK exact/provenance
4. Semantic Independence V3 strict
5. Owner/Grounding
6. Depth Integrity
7. Thread Continuity R2
8. Subplot event distinctness
9. EpisodePlan schema + self-check + allocation/debt/handoff
10. Planner/R8 parity
11. Deep Semantic DS1–DS4
12. artifact hash
13. whole-work gate
14. fresh extraction

DS-4에는 first/middle/final + 위험구간의 직접 SOURCE 의미감사가 필요하다.

## 14. 보강·외부 작품 편입

외부/다른 GPT 작품은 별도 staging에서:
- SourceLock
- exact schema
- Scene ordinal
- Stage02 membership
- Stage03/04 semantics
- THICK provenance
- EpisodePlan
- R5/R8
을 현재 DB와 비교한다.

동일 작품 판본을 계층별로 섞지 않는다.
replacement 또는 reinforcement lineage를 명시한다.
의미 무손실 schema migration과 의미 재저작을 ledger에서 분리한다.

## 15. 패키징과 fresh validation

검증과 패키징을 분리한다.

`VALIDATION_PASS → clean temp files → manifest/checksum → ZIP → separate fresh extraction → real validators → pre/post comparison → RELEASE_READY`

ZIP 내부:
- 단일 root
- UTF-8 filename
- SHA256SUMS
- current pointer
- validation evidence
- no credentials
- no nested obsolete release ZIP

## 16. DB 편입

CANONICAL 편입 전:
- current DB snapshot
- change ledger
- non-target invariance
- target old/new comparison
- all global gates
- fresh extraction
을 남긴다.

그 후에만 current authority pointer / manifest / work index를 갱신한다.

## 17. 현재 특별 주의

- `최강칠우`: SOURCE_HOLD precedent. 완결 작품으로 모방 금지.
- `그저바라보다가`: `_SEQxx` vs `_Sxx` alias 16건은 membership parity가 맞는 nonblocking historical alias diagnostic.
- `미생`: 현재 Deep Semantic R2 강화 패키지의 편입 범위는 EP01–EP11.
- `미안하다사랑한다 EP16`: 강화 integration에서 누락 debt를 `PAID`로 보완함.
- CT-13 R3 formal verdict는 `UNDECLARED`; reverse-engineered EpisodePlan corpus는 CANONICAL이지만 autonomous forward control은 EXPERIMENTAL_HOLD.

## 18. 새 세션 완료 조건

새 작품은 다음이 모두 존재해야 끝난다:
- SourceLock
- Stage01–04
- Boundary evidence
- THICK
- EpisodePlanningContext
- EpisodeSynopsisPlan
- R5
- R8
- all current validation reports
- whole-work closure
- individual package
- DB integration ledger
- final DB fresh validation
- updated new-session learning bundle

이 중 하나가 빠지면 “완료”라고 보고하지 않는다.
