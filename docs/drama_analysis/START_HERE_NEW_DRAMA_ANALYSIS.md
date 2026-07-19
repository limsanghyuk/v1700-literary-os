# 새 대화창 드라마 분석 START HERE

- 상태: `AUTHORITATIVE / CURRENT`
- 갱신일: `2026-07-19`
- 적용 대상: GPT·Claude 공동 드라마 분석
- exact schema: `SCHEMA_CONTRACTS_V2.md`
- EXT6: `DISABLED_BY_DEFAULT`
- DB 릴리즈: **사용자 명시 승인 전 동결**

이 문서는 새 프로젝트·새 대화창·새 모델이 과거 대화 전체를 다시 조사하지 않고도 새 드라마를 바로 분석하기 위한 단일 실행 진입점이다.

---

## 1. 절대 원칙

### 1.1 직접독해와 의미 저작이 본 작업이다

```text
원본 대본 직접독해
→ 장면의 행동·전략·정보·관계·선택·구조 기능 해석
→ Stage01~03 직접 저작
→ 전 시즌 완료 후 Stage04 직접 저작
```

검증은 직접독해를 대신하지 않는다. Python·템플릿·규칙 함수는 원본 추출, 인코딩 정규화, 해시, 직렬화, 구조 검사, 패키징에만 사용한다. 의미 필드는 모델이 원문을 직접 읽고 저작한다.

### 1.2 회차를 순서대로 수직 처리한다

```text
EP01 Q1→Q4 직접독해
→ EP01 Stage01~03 저작
→ 정본 파일 저장
→ 최소 구조검사
→ 단일 checkpoint 갱신
→ EP02
```

여러 회차를 한 번에 의미 생성하지 않는다. 계층별로 전 시즌을 일괄 생성하지 않는다.

### 1.3 GPT와 Claude는 공동 Provider다

- 최종 Stage01~04 스키마와 DB 계약은 동일하다.
- 내부 프롬프트·메모·세션 분할 방식은 Provider별로 달라도 된다.
- `authored_provider`, `normalized_by`, `semantic_reauthoring` 등 provenance를 보존한다.
- 어느 Provider도 자동 상위 권위를 갖지 않는다.
- 사용자 승인 후 공동 `CANONICAL`로 승격한다.

### 1.4 검증은 최소화하되 구조와 의미를 분리한다

다음은 일반 작품의 기본 의무에서 제거한다.

- Q마다 QuarterAudit JSON
- 회차별 다수 증빙 JSON
- 여러 checkpoint 형식
- 반복 checksum
- 약 8회차마다 의무 강경검사
- 회차·블록·전 시즌 중복 validator
- 회차별 ZIP·Fresh Extraction
- 중복 validation registry
- 작품마다 전체 DB 새 릴리즈

이 도구는 삭제하지 않고 **원본 불일치·직접독해 누락 의심·템플릿 반복·Edge 과밀·Provider 충돌·SourceLock 불일치·정본 교체·사용자 요청** 때만 포렌식으로 사용한다.

구조검사 PASS는 스키마·키·참조·coverage만 입증한다. 원문 충실도, 고유 의미, 시퀀스 전진, Arc 변화, LocalEdge 반사실 인과를 입증하지 않는다. 일반 작품은 과도한 회차별 증빙 대신 전체의 약 50% 지점에서 의미 캘리브레이션 1회, Stage04 직전에 전 시즌 의미 품질검사 1회를 수행한다. 상세 기준은 `DRAMA_ANALYSIS_SEMANTIC_QUALITY_LESSONS_2026-07-19.md`를 따른다.

---

## 2. 새 대화창 최소 로드

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. `DRAMA_ANALYSIS_SEMANTIC_QUALITY_LESSONS_2026-07-19.md`
4. 최신 DB **전체 작품 인덱스** 1개
5. 중단 재개 시 작품별 `checkpoint.json` 1개

집계 수치만 있는 DB 상태 파일은 작품 선정용 차집합에 사용할 수 없다. 현재 작품 ID 전체가 있는 인덱스를 사용한다.

과거 대화 전체, 모든 세션 README, 모든 방법론 문서는 시작 전에 전수 조사하지 않는다. 충돌이나 사고가 있을 때만 관련 문서를 부분 조회한다.

---

## 3. 작품 선정

```text
제공 원본 inventory
→ 최신 DB 작품 인덱스와 차집합
→ 회차 완전성
→ 중복·수정본·재수록·누락
→ 인코딩·장면 표식
→ 원본 안정성이 가장 높은 신규 작품 1편
```

다음은 `SOURCE_HOLD`다.

- 회차 누락
- 충돌 판본 판별 불가
- 회차 번호와 실제 내용 불일치
- 인코딩 복구 불가
- 장면 경계 잠금 실패

---

## 4. SourceLock Core

작품당 한 파일만 기본 유지한다.

```text
source_lock/<work>.source_lock.json
```

최소 필드:

```text
schema
work_id
series_title
episodes_total
source_archive
source_archive_sha256
source_encoding
numbering_policy
scene_boundary_policy
direct_reading_required: true
python_semantic_generation: false
provider
model
run_id
status
episodes
completed_episodes
next
```

각 episode:

```text
episode_no
source_filename
original_bytes_sha256
canonical_scene_count
Q1_Q4_ranges
source_marker_anomaly
```

장면별 해시·Quarter별 해시·원문 offset·판본 정렬표는 기본 필수가 아니다. 사고가 있는 작품에서만 Extended SourceLock으로 추가한다.

---

## 5. 장면 경계와 Q1~Q4

Q1~Q4는 극적 4막이 아니라 직접독해의 작업 분할 단위다.

1. 원본 장면 표식과 장소·시간·행동 전환을 조사한다.
2. canonical `scene_no=1..N`을 연속 부여한다.
3. 장면을 자르지 않는 범위에서 약 4분할한다.
4. Q1부터 Q4까지 원문 순서대로 읽는다.
5. Q별 별도 감사 파일은 만들지 않는다.
6. 회차 전체가 끝난 뒤 Stage01~03 완료를 선언한다.

각 장면에서 내부적으로 답한다.

1. 실제 행동은 무엇인가.
2. 누가 어떤 목표·전략을 쓰며 무엇을 숨기거나 피하는가.
3. 정보·오해·관계·권력·의존 조건 중 무엇이 바뀌는가.
4. 누가 무엇을 선택·거부·유예하는가.
5. 회차 구조에서 어떤 기능을 하는가.
6. 어떤 잔여 압력이 다음 장면·시퀀스를 미는가.

이 답은 임의 키를 추가하지 않고 SceneCard 필드에 역할을 나누어 압축한다.

---

## 6. 회차 실행 순서

```text
Q1 직접독해
→ Q2 직접독해
→ Q3 직접독해
→ Q4 직접독해
→ SceneCard
→ EpisodeMeta
→ SequenceBlueprint
→ EpisodeArc
→ CharacterArc
→ RelationshipArc
→ LocalEdge
→ PayoffCandidate
→ 정본 파일 저장
→ 최소 구조검사
→ checkpoint next 갱신
→ 다음 회차
→ 전체의 약 50%에서 의미 캘리브레이션 1회
→ 교정 규칙을 후반부에 적용
→ 전 회차 Stage01~03 완료
→ 전 시즌 의미 품질검사 1회
→ Stage04
```

회차 완료는 채팅 보고가 아니라 위 파일의 실제 존재와 checkpoint 상태로 판단한다.

---

## 7. Stage01

### SceneCard 정확히 9키

```text
work_id
scene_no
heading
title
intent_gist
core
core2
skin
by
```

CORE 16:

```text
ESTABLISH ORACLE INTRO BOND CONFLICT REVERSAL LOSS PUNISH
REVELATION REUNION RELIEF ROMANCE PERIL RESCUE DESIRE HOOK
```

필드 역할:

- `heading`: 원본 장소·시간 provenance
- `title`: 장면의 고유한 극적 행동 또는 전환
- `intent_gist`: 주체·목표·전략·장애·변화
- `core/core2`: 극적 기능
- `skin`: 표면 사건과 구체 상황
- `by`: 저작 Provider

금지:

- 원문 문장 단순 복사
- 동일 문장 골격 반복
- 인물명·장소명만 교체한 템플릿
- 존재하지 않는 감정·인과·사건
- 필드 간 동일 요약 복사
- 전 회차 공통 종결문
- 장면 변화가 없는데 감정·인과를 장문화해 추가

중간·완료 의미검사에서는 title·intent의 원문 대응, exact 반복, 인물명을 마스킹한 동일 골격, 장면 경계와 누락을 표본 대조한다.

### EpisodeMeta 정확히 5키

```text
work_id
scene_count
core_dist
episode_function
by
```

---

## 8. Stage02 SequenceBlueprint

정확히 18키:

```text
seq_id
work_id
episode_no
seq_index
member_scene_nos
scene_span
scene_budget
sequence_intent
goal
obstacle
value_shift
turn_type
turn_class
core_mix
pov_char
place_cluster
runtime_share
by
```

시퀀스 경계는 목표 주체, 목표, 장애 성격, 정보·관계·권력 가치, 행동 계획, POV, 장소 클러스터, 극적 방향이 바뀌는 지점에 둔다. 장면 수 균등분할이 아니다.

불변식:

- 모든 장면 정확히 한 시퀀스
- 누락·중복 0
- span·budget 일치
- runtime 합 1.0
- core_mix는 실제 member SceneCard 근거
- seq_index 1부터 연속
- 각 sequence의 goal·obstacle은 sequence_intent와 직접 대응
- 시작 상태→행동 계획→종료 상태가 실제로 전진
- 같은 goal·obstacle의 exact·masked 반복 금지

turn_type 11종:

```text
RISE BOND PUNISH FALL LOSS REVEAL ORACLE REVERSAL STALL HOOK CONFLICT
```

turn_class:

```text
RISE FALL REVEAL STALL
```

---

## 9. EpisodeArc

정확히 13키:

```text
work_id
episode_no
scene_count
sequence_count
dramatic_question
act_structure
entry_state
exit_state
turning_point
central_conflict_axis
episode_function
core_dist
by
```

실제 entry→turning point→exit 변화를 기록한다. `turning_point`는 실제 `seq_index`와 설명을 사용한다. 모든 시퀀스는 act_structure에서 한 번씩 덮는다. 같은 4막 문장을 반복하지 않는다.

---

## 10. Stage03

### CharacterArc 정확히 8키

```text
work_id
character
episode_no
state_label
state_delta
trigger_scene_no
by
evidence
```

권장 구조:

```text
이전 상태 → trigger → 선택·거부 → 새 상태 → 후속 영향
```

실제 변화가 있는 인물만 기록한다. 주인공 외 가족·조직·팀·경쟁 진영도 실제 변화가 있으면 포함한다. `DESIRE`, `CONFLICT`, `series_start` 같은 범용 표지를 state 변화의 대용물로 반복하지 않는다.

### RelationshipArc 정확히 9키

```text
work_id
char_a
char_b
episode_no
relation_state
relation_delta
trigger_scene_no
evidence
by
```

신뢰·권력·정보 비대칭·의존·적대·거래·은폐·공모·보호·통제·위계의 실제 변화를 기록한다. trigger 장면에 양쪽 인물이 등장·통화·교신해야 한다. `(A,B)`와 `(B,A)` 중복을 금지한다. 같은 회차의 동일 unordered pair는 하나의 복합 전진으로 통합한다.

### LocalEdge 정확히 12키

```text
edge_id
work_id
edge_type
src_episode_no
src_scene_no
tgt_episode_no
tgt_scene_no
gap_episodes
label
confidence
note
by
```

필수:

```text
edge_type = causal
src_episode_no = tgt_episode_no
src_scene_no < tgt_scene_no
gap_episodes = 0
label = target SceneCard.core
```

반사실 질문을 통과한 경우만 생성한다.

```text
source가 없었다면 target이 발생하지 않거나 실질적으로 달라지는가?
```

인접 장면, 같은 시퀀스, 유사 감정은 인과 근거가 아니다.

### PayoffCandidate 정확히 7키

```text
candidate_id
work_id
episode_no
scene_no
edge_type_guess
description
by
```

구체적인 물건·정보·약속·위협·선택처럼 장거리 회수 가능성이 있는 것만 기록한다. 고정 수량은 없다.

---

## 11. 회차 최소 구조검사

회차마다 단 한 번 실행한다. 의미를 재채점하지 않는다. 이 검사의 PASS만으로 회차·작품의 의미 품질 PASS를 선언하지 않는다.

1. JSON/JSONL parse
2. exact keyset·자료형
3. ID 중복
4. SceneCard `1..N` coverage
5. Sequence 누락·중복·span·budget
6. runtime 합
7. Arc trigger·turning point·Edge 참조
8. LocalEdge 같은 회차·gap 0
9. 필수 파일 존재

검사 결과는 별도 다중 JSON이 아니라 단일 checkpoint에 기록한다.

```json
{
  "episode_no": 8,
  "direct_reading_completed": true,
  "stage01_03_saved": true,
  "structure_check": "PASS",
  "next": "EP09_Q1"
}
```

실패하면 해당 회차만 수정한다. 이전 전 회차를 자동 재검증하지 않는다.

---

## 12. 단일 checkpoint

작품당 하나만 유지한다.

```json
{
  "schema": "DRAMA_WORK_CHECKPOINT_CURRENT",
  "work_id": "작품명",
  "provider": "gpt-or-claude",
  "source_lock": "source_lock/작품명.source_lock.json",
  "completed_episodes": [1, 2, 3],
  "current_episode": 4,
  "current_pointer": "EP04_Q2",
  "saved_layers": {
    "stage01": true,
    "stage02": false,
    "stage03": false
  },
  "last_structure_check": "PASS",
  "stage04_status": "NOT_STARTED",
  "next": "EP04_Q2",
  "notes": []
}
```

새 대화창은 `current_pointer`부터 이어가며 완료 회차를 다시 분석하지 않는다.

---

## 13. Stage04

모든 회차 Stage01~03가 저장된 뒤 한 번 수행한다.

### CandidateDisposition 100%

```text
PROMOTED_CROSS_EDGE
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL
RESOLVED_WITHIN_EPISODE
REJECTED_DUPLICATE
REJECTED_INSUFFICIENT_EVIDENCE
REJECTED_SOURCE_MISMATCH
```

미처리 후보가 있으면 Stage04 완료가 아니다.

### CrossEpisodeEdge

LocalEdge와 같은 12키를 사용하되:

```text
tgt_episode_no > src_episode_no
gap_episodes = target - source
edge_type ∈ callback, plant_payoff, subplot_counterpoint
```

실제 plant→보존·변형→payoff가 확인된 경우만 승격한다. 회차 경계 자동 브리지와 규칙적 n→n+2 연결을 금지한다.

### FullSeriesArc 정확히 17키

```text
series
episodes_total
scenes_total
sequences_total
logline
central_dramatic_question
theme_statement
protagonist
antagonist
season_structure
macro_turning_points
resolution
open_ending
tone
conflict_persist
series_core_dist
by
```

실제 전 시즌 매크로 전환을 기술한다.

---

## 14. 작품 완료검사

전 시즌 Stage04 완료 후 한 번만 실행한다.

- 전 회차 Stage01~03 존재
- ID·FK 유효
- Scene·Sequence counts 일치
- CandidateDisposition 100%
- CrossEpisodeEdge 참조 유효
- FullSeriesArc counts 일치
- 전 시즌 의미 품질검사 PASS
- 의미 실패 0
- 작품 ZIP 생성
- 작품 ZIP Fresh Extraction 1회

약 8회차 강검사, 회차별 ZIP, 반복 Fresh Extraction은 기본으로 실행하지 않는다.

---

## 15. 조건부 포렌식 검사

다음 상황에서만 과거 강검사 도구를 사용한다.

- 원본과 SceneCard 불일치
- 직접독해 없이 생성된 흔적
- 동일 문장 골격 대량 반복
- LocalEdge 과밀·자동 인접 연결
- GPT·Claude 동일 작품 결과 충돌
- SourceLock 해시 불일치
- 정본 교체·스키마 마이그레이션
- 사용자 요청

---

## 16. DB 편입

상태:

```text
DRAFT CANDIDATE QUARANTINE PASS_CANDIDATE CANONICAL SUPERSEDED SOURCE_HOLD
```

`CANONICAL`은 사용자 승인으로만 부여한다.

증분 편입:

1. 기존 정본 tree를 변경하지 않는다.
2. 신규 작품과 registry만 추가한다.
3. 신규 작품 구조 무결성을 검사한다.
4. 전역에서는 작품 ID 충돌·registry·경로를 확인한다.
5. 기존 전 작품 의미 검사를 반복하지 않는다.

Provider provenance 예:

```json
{
  "authored_provider": "claude",
  "normalized_by": "gpt",
  "semantic_reauthoring": false,
  "schema_normalization": true,
  "canonical_status": "CANONICAL"
}
```

---

## 17. 릴리즈 동결

- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 신규 작품은 작업 tree·정본 DB에 증분 편입할 수 있다.
- 전체 DB ZIP, 새 Governance 번호, release manifest는 사용자가 명시적으로 요청할 때만 만든다.
- 문서 변경, validator 변경, 작품 한 편 추가만으로 릴리즈 번호를 올리지 않는다.
- 최신 인증 DB 릴리즈는 사용자 승인 전까지 동결한다.

---

## 18. Claude 공동 규격

Claude도 다음을 동일하게 따른다.

- 원본 직접독해
- 회차 순차 처리
- exact Stage01~04 keyset
- 동일 ID·enum·FK
- LocalEdge 동일 회차
- CandidateDisposition 100%
- SourceLock Core
- 단일 checkpoint
- Provider provenance

Claude의 강점인 구체적 CharacterArc, 다축 RelationshipArc, 넓은 앙상블 독해, 인과 중간 메커니즘, plant 변형·회수 설명은 보존한다. 고정 수량과 기계적 전 인물·전 관계 Arc화, 과도한 Edge는 금지한다.

---

## 19. EXT6

```text
DEFAULT: EXT6_DISABLED
```

사용자의 명시적 지시, GPT×Claude 동일 작품 교차비교, 연구용 고밀도 코퍼스 등 별도 작업에서만 실행한다. EXT6 미적용은 Stage01~04 불완전이 아니다.

---

## 20. 보고 규칙

사용자가 중간 보고를 요구하지 않으면 최소 보고만 한다.

```text
작품 / 완료 회차 / current pointer / 저장 Stage / 구조검사 / 차단 오류
```

직접독해를 시작하지 않았는데 진행 중이라고 보고하지 않는다. 파일이 없으면 완료로 보고하지 않는다.

---

## 21. 금지 목록

- 직접독해 없는 의미 생성
- 구조검사 PASS만으로 의미·작품 완료 선언
- Python·템플릿 의미 저작
- 여러 회차 동시 의미 생성
- 미완료 파일 완료 선언
- 장면 인접 LocalEdge 자동 연결
- 회차 간 LocalEdge
- 고정 Arc·Edge·Candidate 수량
- 미처리 PayoffCandidate
- 사용자 승인 없는 CANONICAL
- 기본 분석에서 QuarterAudit 강제
- 기본 분석에서 8회차 강경검사 강제
- 매 작업 전체 DB 재검증
- 매 작품 새 DB 릴리즈
- 사용자 승인 없는 릴리즈 증가
- EXT6 자동 적용

---

## 22. 권위 우선순위

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
2. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 실행·검증·릴리즈 정책
3. `DRAMA_ANALYSIS_SEMANTIC_QUALITY_LESSONS_2026-07-19.md` — 의미 품질·재발 방지 상세
4. 작품 SourceLock·checkpoint
5. 과거 operating manual·incident 문서

과거 문서가 QuarterAudit, 블록 강검사, 반복 validator, 매 작품 DB 릴리즈를 기본 의무로 요구하더라도 이 문서의 현재 정책이 우선한다.
