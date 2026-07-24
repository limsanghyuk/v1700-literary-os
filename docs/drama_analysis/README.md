# 새 세션 한국 드라마 분석 V10 실행 인계서

Document ID: `DRAMA_ANALYSIS_NEW_SESSION_HANDOFF_V10`  
Effective date: `2026-07-24`  
Status: `ACTIVE_ENTRYPOINT`  
Authority: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10`

이 문서는 새 대화창이 과거 세션 전체를 다시 조사하지 않고도 한국 드라마 한 작품을 즉시 선정·독해·분석·검증·저장할 수 있게 하는 단일 진입점이다.

## 1. 시작할 때 읽을 문서 — 정확히 6개

다음 순서만 읽는다.

1. `README.md` — 지금 읽는 실행 인계서
2. `CURRENT_AUTHORITY_POINTER.json` — 현재 권위와 해시
3. `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10.md` — 유일한 의미·운영 규약
4. `authority/DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10/AUTHORITY_MANIFEST.json` — V10 구성·해시
5. `authority/DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10/schemas/EXACT_SCHEMA_REGISTRY.json` — exact keyset
6. `AUTHORED_WORK_INDEX_V22.json` — 79작품 최신 물리 인덱스

과거 V1–V9, GPT·Claude 개별 매뉴얼, 세션 handoff, 구형 DB 상태 문서는 읽지 않는다. 충돌 시 V10과 현재 포인터가 우선한다.

대상 작품을 정한 뒤에만 실행 상태를 추가로 읽는다.

- 신규 작품: V10 `work_state.template.json`로 새 `work_state.json` 생성
- 기존 작품 재개: 대상 작품의 `work_state.json`과 마지막 `CHECKPOINT_LOCKED`
- 기존 작품 재저작: 기존 lineage·SourceLock·현재 DB 파일을 읽되, 의미문을 먼저 모방하지 않는다

## 2. 현재 데이터베이스 상태

- 작품: 79
- 회차: 1,465
- SceneCard: 92,090
- 최신 작품 인덱스: `AUTHORED_WORK_INDEX_V22.json`
- 활성 권위: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10`
- 《질투의 화신》: 물리 편입 완료, 현재 의미 보강 및 V10 Stage04 재감사 대기
- 사용자 승인 전 전체 상태: `NOT_CANONICAL_USER_APPROVAL_REQUIRED`

작품 선정 시 `AUTHORED_WORK_INDEX_V22.json`과 후보 작품명을 대조하여 기존 작품을 신규 작품으로 중복 편입하지 않는다.

## 3. 절대 원칙

> 원본을 직접 읽고 이해한 뒤 고유하게 저작한다. 도구는 의미를 만들지 않고 판단을 보존·검증·운반한다.

필수:

- 한 회차 원본 전체를 처음부터 끝까지 순차 독해
- 실제 행동·전략·정보 변화·선택·구조 기능을 구분
- SceneCard exact 9키
- 저작 run과 독립 감사 run 분리
- 회차별 원자적 저장과 checksum
- 최대 8회차 블록 강검사
- 전 시즌 Stage01–03 잠금 후 Stage04
- 후보 100% 처분
- ZIP fresh extraction
- 사용자 승인 전 `CANONICAL` 금지

금지:

- Python으로 의미 필드 생성
- 대사·지문·기존 의미문 복사
- 고유명만 바꾼 반복 문형
- 장면 수 균등분할 Sequence
- 회차 요약을 모든 Arc에 복제
- 부분 원본으로 Stage04·전 시즌 PASS 생성
- 저작자가 같은 run에서 독립 감사 PASS 생성
- 구조 PASS를 의미 PASS로 확대

## 4. 신규 작품 선정과 SourceLock

1. 후보 목록과 79작품 인덱스를 대조한다.
2. 전 회차와 최종회 존재를 확인한다.
3. 최종회가 실제 종결본인지 읽어 확인한다.
4. 중복 판본·수정 조각·추가 장면 조각을 분리한다.
5. 원본 파일 SHA-256과 추출 텍스트 SHA-256을 기록한다.
6. 첫 회차·중간 회차·최종회 표본을 원본과 추출본으로 대조한다.
7. 삭제·삽입·번호 없는 외경·몽타주·회상 전환을 감사한다.
8. canonical `scene_no=1..N`과 원문 `source_label`을 분리한다.
9. `SourceFormatAudit`, `SourceLock`, canonical scene map을 잠근다.

전 회차·결말이 완전하지 않으면 `FULL_SERIES_SOURCE_LOCKED`를 선언하지 않는다.

## 5. 한 회차 실행 순서

```text
SourceBoundaryReview
→ 원본 전체 순차 독해
→ Stage01 SceneCard
→ EpisodeMeta
→ Stage02 SequenceBlueprint
→ EpisodeArc
→ CharacterArc·RelationshipArc
→ LocalEdge·PayoffCandidate
→ 회차 경량검사
→ 독립 원문 감사
→ 원자적 저장
→ EPISODE_CHECKPOINT_LOCKED
→ 다음 회차
```

Q1–Q4는 긴 회차를 순서대로 읽기 위한 보조 단위일 뿐, 별도 극적 4막이나 정본 산출물이 아니다.

앞 회차가 `EPISODE_CHECKPOINT_LOCKED`가 아니면 다음 회차를 잠그지 않는다.

## 6. Stage01

SceneCard exact 9키:

```text
work_id, scene_no, heading, title, intent_gist,
core, core2, skin, by
```

각 장면에서 확인한다.

1. 누가 실제로 무엇을 하는가
2. 목표·전략·은폐·회피는 무엇인가
3. 새로 생기거나 변한 정보·관계·권력은 무엇인가
4. 어떤 선택·거부·유예가 발생하는가
5. 회차 구조에서 어떤 기능을 하는가
6. 다음 장면을 미는 잔여 압력은 무엇인가

`title`, `intent_gist`, `skin`은 서로 다른 정보를 담고, 다른 장면에도 붙을 수 있는 추상문을 쓰지 않는다.

EpisodeMeta exact 5키:

```text
work_id, scene_count, core_dist, episode_function, by
```

`scene_count`와 `core_dist`는 저장된 SceneCard에서 결정론적으로 재계산한다.

## 7. Stage02

SequenceBlueprint exact 18키는 `EXACT_SCHEMA_REGISTRY.json`을 따른다.

Sequence 경계는 다음 중 하나 이상이 실제로 변하는 지점에 둔다.

- 지배 목표
- 장애·압력
- POV
- 장소·시간
- 행동 계획
- 가치 방향
- 극적 질문

불변식:

- 모든 장면이 정확히 한 Sequence에 포함
- 누락·중복 0
- `member_scene_nos` 연속·오름차순
- `scene_span`, `scene_budget` 일치
- `runtime_share` 합 1.0
- 실제 SceneCard에 존재하는 `core_mix`
- 균등 장면 수 분할 금지

## 8. Stage03

EpisodeArc는 회차의 `entry → turning point → exit` 변화를 기록한다.

CharacterArc:

- 실제 상태 변화가 있는 인물만 기록
- `state_label`은 현재 상태
- `state_delta`는 이번 회차 변화량
- trigger 장면과 evidence는 원문 행동·대사에 근거

RelationshipArc:

- 두 당사자가 실제 접촉·통화·교신한 변화만 기록
- `(A,B)`와 `(B,A)` 중복 금지
- 단일 인물·집단·추상 세력을 관계쌍으로 만들지 않음

LocalEdge:

- 같은 회차의 구체적 반사실 인과만 허용
- 단순 인접·주제 유사·Sequence 순서는 인과가 아님

PayoffCandidate:

- 장거리 회수 가능성이 있는 구체 plant만 기록
- 고정 수량 없음
- 후속 원문 확인 전 CrossEpisodeEdge로 확정하지 않음

## 9. 회차·블록·전 시즌 검사

### 회차 경량검사

- JSON/JSONL parse
- exact keyset·type·enum
- ID 중복
- SceneCard ordinal coverage
- Sequence partition·span·budget·runtime
- Arc·Edge 참조
- trigger 참여자
- LocalEdge 회차·target core
- placeholder·정확 중복·반복 문형

### 최대 8회차 블록 강검사

- 16부작: EP01–08 / EP09–16
- 20부작: EP01–08 / EP09–16 / EP17–20
- 24부작: EP01–08 / EP09–16 / EP17–24

검사 항목:

- 블록 전 파일 구조·참조
- 원문 표본 재대조
- 의미 중복·마스킹 문형
- 균등 Sequence 경계
- Arc trigger와 evidence
- Edge 과밀·인접 편향
- 감사 run 분리와 체크포인트

### 전 시즌

- 모든 회차 Stage01–03 잠금
- 블록 잠금 전부 존재
- 전 작품 의미 회귀검사
- Stage04 독립 원문 재개방
- CandidateDisposition 100%
- FullSeriesArc count 일치
- 작품 패키지·DB 편입·Fresh Extraction

## 10. Stage04

Stage04는 전 회차 Stage01–03 잠금 뒤 수행한다.

1. 모든 PayoffCandidate를 원 발생 장면에서 다시 읽는다.
2. 후보별 실제 회수 장면을 원문에서 다시 읽는다.
3. 후보를 100% 처분한다.
4. 실제 장거리 plant/payoff만 CrossEpisodeEdge로 승격한다.
5. 자동 회차 bridge, 최종회 집결, 결혼식 참석, 주제 유사만으로 승격하지 않는다.
6. FullSeriesArc를 전 시즌 전환에 따라 작성한다.
7. 저작 run과 다른 audit run이 독립 검사한다.

독립 원문 재개방 증거가 없으면 Stage04는 완료가 아니다.

## 11. 저장·중단 복구

시간 계약:

- 20분: 체크포인트 준비
- 25분: 산출물·상태·checksum 저장
- 30분: 체크포인트 없는 의미 작업 하드스톱

저장:

```text
<file>.tmp
→ parse
→ flush/fsync
→ 기존 파일 lineage 보존
→ atomic rename
→ SHA-256
→ manifest·work_state·RunJournal 동기화
```

중단 시 사용자 보고가 아니라 실제 파일·SHA·journal을 기준으로 마지막 `CHECKPOINT_LOCKED`까지 복구한다.

## 12. DB 편입

신규 작품:

- `ADD_NEW_WORK`
- 기존 79작품 의미 파일 변경 0
- 신규 work_id 중복 0

기존 작품 재저작:

- `REPLACE_EXISTING_WORK`
- 작품 lineage·source hash·scene ordinal 호환 확인
- 서로 다른 판본의 Stage 혼합 금지
- 작품 계층 전체 교체 또는 명시된 선택 재저작 ledger

편입 후:

- 최신 작품 인덱스·포인터·work_state 갱신
- 전체 JSON/JSONL parse
- 작품 수·회차 수·SceneCard 수 재집계
- ZIP CRC·SHA ledger·fresh extraction
- semantic FAIL 작품을 `CANONICAL`로 표시하지 않음

## 13. 새 세션에 줄 첫 명령

```text
README.md부터 지정된 6개 문서를 순서대로 읽어 V10 권위와 해시를 확인하라.
AUTHORED_WORK_INDEX_V22.json과 후보 원본 목록을 대조해 기존 DB에 없는 완전한 한 작품을 선정하라.
전 회차와 최종회·판본·SourceLock을 먼저 잠근 뒤 EP01 원본 전체를 순차 독해하고,
Stage01→02→03→회차 경량검사→독립 원문 감사→EPISODE_CHECKPOINT_LOCKED 순으로 진행하라.
최대 8회차 블록마다 강검사하고, 전 회차 Stage01–03 잠금 뒤에만 Stage04를 수행하라.
Python으로 의미를 생성하거나 과거 작품 문형을 복사하지 말고, 사용자 승인 전 CANONICAL을 선언하지 마라.
```

## 14. 충돌과 중단 조건

다음이면 분석을 시작하거나 계속하지 않는다.

- 포인터의 V10 master·manifest·schema·index 해시 불일치
- 허브와 DB의 V10 authority hash 불일치
- 전 회차·최종회 불완전
- source label과 canonical ordinal 재현 불가
- 기존 작품명·work_id 중복
- 마지막 checkpoint보다 work_state가 앞서거나 뒤섞임
- 같은 run이 저작과 독립 감사를 동시에 주장
- 구조 PASS만 있고 원문 의미 감사 없음

이 경우 상태를 `AUTHORITY_CONTRACT_DRIFT`, `SOURCE_HOLD`, `RECOVERY_REQUIRED`, `SEMANTIC_AUDIT_REQUIRED` 중 하나로 기록하고 사용자에게 보고한다.
