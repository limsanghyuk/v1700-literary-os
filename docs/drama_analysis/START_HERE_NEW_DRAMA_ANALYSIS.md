# 새 대화창 드라마 분석 START HERE

- 문서 상태: `AUTHORITATIVE / CURRENT`
- 갱신일: `2026-07-18`
- 적용 대상: GPT·Claude 공동 드라마 분석 진영
- exact schema 권위: `SCHEMA_CONTRACTS_V2.md`
- DB 릴리즈 정책: **동결. 사용자의 명시적 승인 없이는 새 릴리즈 번호·전체 DB 패키지를 생성하지 않는다.**
- EXT6 정책: **기본 비활성. 별도 지시가 있을 때만 적용한다.**

이 문서는 새로운 프로젝트 또는 새로운 대화창에서 새 드라마를 분석할 때 가장 먼저 읽는 단일 실행 진입점이다. 과거 대화 전체와 모든 역사 문서를 다시 학습하지 않는다. 이 문서, exact schema, 최신 작품 인덱스만으로 분석을 시작할 수 있어야 한다.

---

## 1. 절대 원칙

### 1.1 본 작업은 직접독해와 의미 저작이다

```text
원본 대본 직접독해
→ 장면의 행동·전략·변화·선택·구조 기능 해석
→ Stage01~03 직접 저작
→ 전 시즌 완료 후 Stage04 직접 저작
```

검증은 직접독해를 대신하지 않는다. Python·템플릿·규칙 기반 프로그램으로 의미 필드를 생성하지 않는다. 프로그램은 원본 추출, 인코딩 정규화, 해시, JSON 직렬화, 참조 검사, 패키징에만 사용한다.

### 1.2 회차를 순서대로 수직 처리한다

```text
EP01 Q1→Q4 직접독해
→ EP01 Stage01~03 저작
→ 정본 파일 저장
→ 최소 구조검사
→ 단일 checkpoint 갱신
→ EP02
```

계층별로 전 시즌을 한꺼번에 작성하지 않는다. 여러 회차의 의미 레코드를 동시에 생성하지 않는다.

### 1.3 GPT와 Claude는 공동 저작 Provider다

- 최종 데이터 스키마와 DB 규격은 동일하다.
- 각 Provider의 내부 메모·프롬프트·세션 분할 방식은 달라도 된다.
- 원저작 Provider와 정규화 Provider를 provenance에 기록한다.
- Claude 산출물은 GPT 산출물보다 하위가 아니며, GPT 산출물도 Claude 산출물보다 상위가 아니다.
- 사용자 승인으로 정본이 된 작품은 Provider와 무관하게 공동 `CANONICAL`이다.

### 1.4 검증은 최소화한다

기존의 다음 항목은 일반 작품의 기본 절차에서 제거한다.

- Quarter마다 상세 감사 JSON
- 회차마다 다수의 검증 증빙 파일
- 여러 종류의 checkpoint
- 회차·블록·전 시즌에서 반복되는 동일 validator
- 반복 checksum
- 회차별 ZIP과 Fresh Extraction
- 동일 정보를 복제하는 validation registry
- 약 8회차마다 의무적인 강경 의미검사

이 기능은 삭제된 것이 아니라 **사고·충돌·정본 교체·원본 불일치가 있을 때만 사용하는 포렌식 도구**로 이동한다.

---

## 2. 새 대화창 최소 로드

새 대화창은 다음 순서로 읽는다.

1. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 문서
2. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
3. 최신 DB 작품 인덱스 또는 작품 목록 1개 — 중복 분석 방지
4. 중단 작업이라면 해당 작품의 `checkpoint.json` 1개

다음 문서는 문제가 생겼을 때만 조회한다.

- 상세 close-reading 사례
- 과거 incident 보고서
- QuarterAudit 구계약
- 고강도 semantic validator 규칙
- 과거 릴리즈 manifest
- EXT6 문서

새 대화창 시작 전에 과거 대화 전체, 세션 README 전체, 허브 전체를 전수 조사하지 않는다.

---

## 3. 작품 선정과 원본 잠금

### 3.1 선정 절차

```text
제공된 원본 목록 확인
→ 최신 DB 작품 목록과 차집합
→ 회차 완전성 확인
→ 중복·수정본·재수록·누락 확인
→ 인코딩과 장면 표식 확인
→ 가장 안정적인 신규 작품 1편 선정
```

다음은 `SOURCE_HOLD`다.

- 실제 회차 누락
- 서로 충돌하는 판본을 판별할 수 없음
- 회차 번호와 실제 내용이 불일치
- 인코딩 복구 불가
- 장면 경계를 안정적으로 확정할 수 없음

### 3.2 SourceLock Core

작품당 한 파일만 유지한다. 예: `source_lock/<work>.source_lock.json`.

최소 내용:

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

각 회차 최소 내용:

```text
episode_no
source_filename
original_bytes_sha256
canonical_scene_count
scene_range 또는 Q1~Q4 범위
source_marker_anomaly
```

장면별 해시, Quarter별 해시, 상세 원문 offset은 기본 필수가 아니다. 원본 충돌이나 장면 번호 사고가 있을 때만 SourceLock Extended로 추가한다.

---

## 4. 장면 경계와 Q1~Q4

Q1~Q4는 극적 4막이 아니라 **직접독해의 작업 분할 단위**다.

1. 원본의 장면 표식과 장소·시간·행동 전환을 확인한다.
2. canonical `scene_no`를 `1..N`으로 연속 부여한다.
3. 장면 경계를 자르지 않는 범위에서 약 4분할한다.
4. Q1부터 Q4까지 원문 순서대로 읽는다.
5. Q별 별도 감사 파일은 만들지 않는다.
6. 세션이 끊길 가능성이 있으면 Stage01 부분 파일을 안전 저장할 수 있으나, 정본 완료는 회차 전체 Q1~Q4가 끝난 뒤 선언한다.

각 장면을 읽을 때 내부적으로 다음 여섯 질문에 답한다.

1. 실제로 무슨 행동이 일어나는가.
2. 누가 어떤 목표·전략을 쓰며 무엇을 숨기거나 피하는가.
3. 정보·오해·관계·권력·의존 조건 중 무엇이 바뀌는가.
4. 누가 무엇을 선택·거부·유예하는가.
5. 이 장면은 회차 구조에서 어떤 기능을 하는가.
6. 어떤 잔여 압력이나 미해결 조건이 다음 장면·시퀀스를 미는가.

이 답을 새로운 임의 키로 추가하지 않고 SceneCard의 `title`, `intent_gist`, `core/core2`, `skin`에 역할을 나누어 압축한다.

---

## 5. 회차별 실행 순서

모든 회차는 아래 순서를 지킨다.

```text
Q1 직접독해
→ Q2 직접독해
→ Q3 직접독해
→ Q4 직접독해
→ SceneCard 완성
→ EpisodeMeta
→ SequenceBlueprint
→ EpisodeArc
→ CharacterArc
→ RelationshipArc
→ LocalEdge
→ PayoffCandidate
→ 정본 파일 저장
→ 회차 최소 구조검사
→ checkpoint 갱신
→ 다음 회차
```

### 완료 보고의 기준

채팅에서 “진행 중”이라고 말하는 것은 완료 증거가 아니다. 다음 파일이 실제로 저장되어야 해당 회차가 완료다.

- Stage01 SceneCard
- EpisodeMeta
- Stage02 SequenceBlueprint
- EpisodeArc
- CharacterArc
- RelationshipArc
- LocalEdge
- PayoffCandidate
- checkpoint의 완료 회차 갱신

---

## 6. Stage01 저작

### 6.1 SceneCard exact keyset

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

### 6.2 필드 역할

- `heading`: 원본 장면 heading과 장소·시간 provenance
- `title`: 장면의 고유한 극적 행동 또는 전환
- `intent_gist`: 누가 무엇을 원하고, 어떤 전략·장애·변화를 만들었는지
- `core`: 장면의 주된 극적 기능
- `core2`: 실제로 두 번째 기능이 명확할 때만 사용
- `skin`: 표면 사건·상황·감정의 구체적 표현
- `by`: 저작 Provider 또는 모델

### 6.3 CORE_ENUM 16

```text
ESTABLISH ORACLE INTRO BOND CONFLICT REVERSAL LOSS PUNISH
REVELATION REUNION RELIEF ROMANCE PERIL RESCUE DESIRE HOOK
```

### 6.4 품질 기준

좋은 SceneCard는 줄거리 한 줄 요약이 아니다. 다음 중 적어도 여러 항목이 구체적이어야 한다.

- 행동 주체
- 목표 또는 전략
- 장애·은폐·오해
- 정보·관계·권력 변화
- 선택·거부·유예
- 구조 기능
- 다음 행동을 밀어내는 잔여 압력

금지:

- 원문 문장을 제목에 단순 복사
- 모든 장면에 같은 문장 골격 사용
- 인물명과 장소명만 바꾼 템플릿
- 존재하지 않는 감정·인과·사건 추가
- `title`, `intent_gist`, `skin`에 같은 문장 반복

---

## 7. Stage02 SequenceBlueprint 저작

### 7.1 exact keyset

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

### 7.2 시퀀스 경계

시퀀스는 장면 수를 균등하게 나눈 묶음이 아니다. 다음 중 하나가 바뀌는 지점에서 경계를 둔다.

- 목표 주체
- 목표
- 장애의 성격
- 정보·관계·권력 가치
- 행동 계획
- POV 중심
- 장소 클러스터
- 극적 방향

### 7.3 구조 불변식

- 모든 장면은 정확히 한 시퀀스에 포함
- 누락·중복 0
- `scene_span`은 member의 첫·마지막 장면과 일치
- `scene_budget == len(member_scene_nos)`
- 모든 `runtime_share` 합은 1.0
- `core_mix`는 member SceneCard의 실제 CORE에서 가져옴
- `seq_index`는 1부터 연속

### 7.4 turn registry

`turn_type`은 다음 11종만 사용한다.

```text
RISE BOND PUNISH FALL LOSS REVEAL ORACLE REVERSAL STALL HOOK CONFLICT
```

`turn_class`는 `RISE / FALL / REVEAL / STALL` 중 하나이며 기존 매핑을 따른다.

---

## 8. EpisodeArc 저작

exact keyset:

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

작성 원칙:

- `dramatic_question`: 회차가 실제로 묻고 끝에서 어떤 상태로 바꾸는가
- `entry_state`: 시작 조건
- `exit_state`: 종료 조건
- `turning_point`: 실제 시퀀스 번호와 설명
- `central_conflict_axis`: 회차를 지배한 대립 축
- `episode_function`: 전 시즌에서 이 회차가 수행한 기능
- `act_structure`: 실제 시퀀스 경계를 따라 모든 시퀀스를 한 번씩 덮음

기계적으로 항상 같은 4막 설명을 복사하지 않는다.

---

## 9. Stage03 저작

### 9.1 CharacterArc

exact keyset:

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

다음 구조를 권장한다.

```text
이전 상태
→ trigger 사건
→ 인물의 선택·거부
→ 새로운 상태
→ 다음 행동에 미치는 영향
```

단순 등장만으로 만들지 않는다. 실제 상태 변화가 있는 인물만 기록한다. 주인공 외 가족·팀·조직·경쟁 진영도 실제 변화가 있으면 포함한다.

### 9.2 RelationshipArc

exact keyset:

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

관계 변화 축:

```text
신뢰 권력 정보비대칭 의존 적대 거래 은폐 공모 보호 통제 위계
```

두 인물이 trigger 장면에서 직접 만나거나 통화·교신해야 한다. `(A,B)`와 `(B,A)`를 중복 생성하지 않는다.

### 9.3 LocalEdge

exact keyset:

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
gap_episodes = 0
label = target SceneCard.core
```

반사실 질문:

```text
source 장면의 행동·정보가 없었다면 target 사건이 발생하지 않거나 실질적으로 달라지는가?
```

아니라면 LocalEdge를 만들지 않는다. 장면 인접성, 같은 시퀀스, 비슷한 감정은 인과 근거가 아니다.

### 9.4 PayoffCandidate

exact keyset:

```text
candidate_id
work_id
episode_no
scene_no
edge_type_guess
description
by
```

허용 guess:

```text
plant_payoff callback subplot_counterpoint resolved_here
```

구체적인 물건·정보·약속·위협·선택처럼 장거리 회수 가능성이 있는 것만 남긴다. 다음 장면이나 같은 회차에서 이미 닫힌 문제는 장거리 후보로 과장하지 않는다. 고정 수량은 없다.

---

## 10. 회차 최소 구조검사

회차마다 단 한 번 실행한다. 의미를 다시 채점하거나 대본을 재독해하는 검사가 아니다.

검사 항목:

1. JSON/JSONL parse
2. exact keyset과 자료형
3. ID 중복
4. SceneCard `scene_no=1..N` coverage
5. Sequence의 장면 누락·중복·span·budget
6. `runtime_share` 합
7. Arc trigger와 turning point 참조 존재
8. LocalEdge 동일 회차·gap 0·source/target 존재
9. 필수 파일 존재

결과는 별도 다중 JSON으로 만들지 않고 `checkpoint.json`에 한 줄 상태로 기록한다.

```json
{
  "episode_no": 8,
  "direct_reading_completed": true,
  "stage01_03_saved": true,
  "structure_check": "PASS",
  "next": "EP09_Q1"
}
```

검사 실패 시 해당 회차만 수정한다. 이전 전 회차를 자동 재검증하지 않는다.

---

## 11. 단일 checkpoint

작품당 checkpoint는 하나다.

권장 구조:

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

새 대화창은 이 파일을 읽고 이미 완료된 회차를 다시 분석하지 않는다. `current_pointer`부터 이어간다.

---

## 12. Stage04 전 시즌 fan-in

Stage04는 모든 회차 Stage01~03가 저장된 뒤 한 번 수행한다.

### 12.1 후보 처분

모든 PayoffCandidate를 원본의 후속 회차와 대조한다.

권장 disposition:

```text
PROMOTED_CROSS_EDGE
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL
RESOLVED_WITHIN_EPISODE
REJECTED_DUPLICATE
REJECTED_INSUFFICIENT_EVIDENCE
REJECTED_SOURCE_MISMATCH
```

미처리 후보가 있으면 Stage04는 완료가 아니다.

### 12.2 CrossEpisodeEdge

LocalEdge와 동일한 12키를 사용하되:

```text
tgt_episode_no > src_episode_no
gap_episodes = target - source
edge_type ∈ callback, plant_payoff, subplot_counterpoint
```

실제 plant→보존·변형→payoff가 확인된 경우만 승격한다. 회차 마지막 장면과 다음 회차 첫 장면을 자동 연결하지 않는다. 규칙적인 `EP n→EP n+2`를 자동 생성하지 않는다.

### 12.3 FullSeriesArc

exact keyset:

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

실제 전 시즌 매크로 전환을 기술한다. 기계적 4분기 요약을 만들지 않는다.

---

## 13. 작품 완료검사와 패키징

전 시즌 Stage04까지 끝난 뒤 한 번만 실행한다.

최소 검사:

- 모든 회차 Stage01~03 존재
- 모든 ID·FK 유효
- Scene·Sequence counts 일치
- PayoffCandidate disposition 100%
- CrossEpisodeEdge 참조 유효
- FullSeriesArc counts 일치
- 작품 ZIP 생성 가능
- 최종 작품 ZIP Fresh Extraction 1회

일반 작품에서 블록별 강검사, 회차별 ZIP, 반복 Fresh Extraction은 하지 않는다.

### 의미 정밀감사가 필요한 조건

다음 중 하나가 실제로 발견될 때만 포렌식 검사를 실행한다.

- 원본과 SceneCard가 불일치
- 직접독해 없이 자동 생성된 흔적
- 대량 동일 문장 골격
- LocalEdge 과밀 또는 자동 인접 연결
- Provider 간 동일 작품 결과가 충돌
- SourceLock 해시 불일치
- 정본 교체 또는 스키마 마이그레이션
- 사용자 요청

---

## 14. 데이터베이스 편입

### 14.1 정본 계층

상태:

```text
DRAFT
CANDIDATE
QUARANTINE
PASS_CANDIDATE
CANONICAL
SUPERSEDED
SOURCE_HOLD
```

`CANONICAL`은 사용자 승인으로만 부여한다. GPT와 Claude의 공동 분석 작품은 Provider provenance를 보존하면서 동일 정본 계층에 편입한다.

권장 provenance:

```json
{
  "authored_provider": "claude",
  "normalized_by": "gpt",
  "semantic_reauthoring": false,
  "schema_normalization": true,
  "canonical_status": "CANONICAL"
}
```

### 14.2 증분 편입

신규 작품을 편입할 때:

1. 기존 정본 tree는 변경하지 않는다.
2. 신규 작품 경로와 registry만 추가한다.
3. 신규 작품 구조 무결성을 검사한다.
4. DB 전역에서는 작품 ID 충돌·registry·경로만 확인한다.
5. 기존 전 작품의 의미 검사를 매번 재실행하지 않는다.

### 14.3 릴리즈 동결

- 작품 분석 완료가 곧 새 DB 릴리즈 생성을 의미하지 않는다.
- 신규 작품은 작업 DB 또는 정본 tree에 증분 편입할 수 있다.
- 전체 DB ZIP, 새 Governance 번호, 새 release manifest는 사용자가 명시적으로 요청할 때만 만든다.
- 문서 변경, validator 변경, 작품 한 편 추가만으로 릴리즈 번호를 증가시키지 않는다.
- 최신 인증 DB 패키지의 번호는 사용자의 다음 릴리즈 승인 전까지 동결한다.

---

## 15. Claude 공동 규격

Claude가 분석할 때도 다음은 동일하다.

- 원본 직접독해
- 회차 순차 처리
- exact Stage01~04 keyset
- 동일 ID와 enum
- LocalEdge 동일 회차
- CandidateDisposition 100%
- SourceLock Core
- 단일 checkpoint
- Provider provenance

Claude가 강점을 보이는 다음 저작 방식은 유지한다.

- 구체적인 CharacterArc 상태 변화
- 다축 RelationshipArc
- 조직·가족·팀·경쟁 진영의 넓은 앙상블 독해
- 인과의 중간 메커니즘을 설명하는 Edge note
- plant의 보존·변형·회수 과정을 설명하는 CrossEdge

그러나 고정 수량, 전 인물 기계적 Arc화, 과도한 LocalEdge는 사용하지 않는다.

---

## 16. EXT6 정책

EXT6는 기본 Stage01~04 분석에 포함하지 않는다.

```text
DEFAULT: EXT6_DISABLED
```

다음 경우에만 별도 실행한다.

- 사용자가 특정 작품에 명시적으로 지시
- GPT×Claude 동일 작품 교차비교
- 연구용 고밀도 코퍼스 구축
- 별도 실행 예산과 세션이 확보됨

EXT6 미적용은 Stage01~04 불완전이 아니다.

---

## 17. 개발자 보고 규칙

사용자가 중간 보고를 요구하지 않는 한 보고는 최소화한다.

보고할 때 실제 저장 상태만 말한다.

```text
작품
완료 회차
현재 pointer
저장된 Stage
구조검사 상태
차단 오류
```

직접독해를 시작하지 않았는데 “진행 중”이라고 보고하지 않는다. 파일이 없으면 완료로 보고하지 않는다.

---

## 18. 금지 목록

- 대본을 읽지 않고 의미 레코드 생성
- Python·템플릿 의미 저작
- 여러 회차 동시 의미 생성
- 미완료 파일을 정본으로 선언
- 장면 인접성을 LocalEdge로 자동 연결
- 회차 간 LocalEdge
- 고정 Arc·Edge·Candidate 수량
- 미처리 PayoffCandidate
- 사용자 승인 없는 CANONICAL
- 매 회차 다중 검증 JSON 생성
- 기본 분석에서 QuarterAudit 강제
- 기본 분석에서 8회차 강경검사 강제
- 매 작업마다 전체 DB 재검증
- 매 작품마다 새 DB 릴리즈 생성
- 사용자 승인 없는 릴리즈 번호 증가
- EXT6 자동 적용

---

## 19. 새 작품 실행 체크리스트

### 시작

- [ ] START_HERE와 SCHEMA_CONTRACTS를 읽음
- [ ] DB 중복 작품이 아님
- [ ] 원본 회차 완전성 확인
- [ ] SourceLock Core 생성
- [ ] checkpoint 생성

### 매 회차

- [ ] Q1→Q4 원본 직접독해
- [ ] SceneCard·EpisodeMeta 저장
- [ ] SequenceBlueprint·EpisodeArc 저장
- [ ] CharacterArc·RelationshipArc 저장
- [ ] LocalEdge·PayoffCandidate 저장
- [ ] 최소 구조검사 PASS
- [ ] checkpoint의 next 갱신

### 전 시즌

- [ ] 모든 회차 Stage01~03 완료
- [ ] PayoffCandidate 전수 처분
- [ ] CrossEpisodeEdge 확정
- [ ] FullSeriesArc 작성
- [ ] 작품 완료검사
- [ ] 작품 ZIP Fresh Extraction 1회
- [ ] 사용자 승인 상태에 맞게 DB 증분 편입
- [ ] 새 릴리즈는 만들지 않음

---

## 20. 권위 충돌 시 우선순위

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
2. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 실행·검증·릴리즈 정책
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` — 요약 실행 가이드
4. 작품 SourceLock과 checkpoint
5. 과거 상세 playbook·incident 문서

과거 문서가 QuarterAudit, 블록 강검사, 반복 validator, 매 작품 DB 릴리즈를 기본 의무로 요구하더라도 현재 문서의 간소화 정책이 우선한다.
