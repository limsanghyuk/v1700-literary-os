# 드라마 분석 스키마·불변식 계약 v2

Document ID: GPT-DRAMA-SCHEMA-CONTRACTS-V2  
Status: AUTHORITATIVE  
Updated: 2026-07-12

이 문서는 Stage01~04 산출물의 정확한 키셋, 자료형, enum, ID, 참조 불변식을 정의한다. 키 누락뿐 아니라 임의 키 추가도 validator 계약에 따라 실패할 수 있다.

## 1. 공통 명명 규칙

### 작품 식별자

```text
work = 작품명 공백 제거 또는 정본 표기
회차 work_id = <work>_<NN>
시즌 work_id = <work>
```

예:

```text
시티헌터_01
내여자친구는구미호_16
```

### 회차·시퀀스 ID

```text
seq_id = <work>_<NN>_S<II>
```

- NN: 2자리 회차
- II: 회차 내 2자리 시퀀스 번호
- `seq_index`는 1부터 연속

### 엣지·후보 ID

권장:

```text
LocalEdge      <work>_e<NN><III>
PayoffCandidate <work>_p<NN><III>
CrossEpisodeEdge <work>_x<III>
```

ID는 작품 전체에서 유일해야 한다. 과거 패키지의 다른 접두 규칙은 lineage에 보존할 수 있으나 새 작품은 위 규칙으로 통일한다.

## 2. CORE_ENUM 16

Stage01 `core/core2`, Stage02 `core_mix`, Edge `label`의 기본 극적 기능 enum.

```text
ESTABLISH
ORACLE
INTRO
BOND
CONFLICT
REVERSAL
LOSS
PUNISH
REVELATION
REUNION
RELIEF
ROMANCE
PERIL
RESCUE
DESIRE
HOOK
```

다음과 같은 임의 값은 금지한다.

```text
SETUP, PLAN, IRONY, RECAP, RISE, FALL, REVEAL, STALL,
설정, 전환, 위기고조, 감정상승
```

`RISE/FALL/REVEAL/STALL`은 `turn_class`에만 사용한다.

## 3. Stage01 SceneCard — 정확히 9키

경로:

```text
authored/<work>_<NN>.seqcard.jsonl
```

키:

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

자료형:

```json
{
  "work_id": "string",
  "scene_no": 1,
  "heading": "string",
  "title": "string",
  "intent_gist": "string",
  "core": "CORE_ENUM",
  "core2": "CORE_ENUM or null",
  "skin": "string",
  "by": "string"
}
```

불변식:

- `scene_no = 1..N` 연속
- SourceLock의 canonical ordinal과 일치
- `heading`은 원본 provenance와 대응
- `title`과 `intent_gist`는 의미 있는 고유 문장
- `core/core2`는 CORE_ENUM 16
- 동일 장면에서 `core == core2`는 특별한 근거가 없으면 피함
- 존재하지 않는 인물·사건을 쓰지 않음

## 4. EpisodeMeta — 정확히 5키

경로:

```text
authored/<work>_<NN>.episode_meta.json
```

키:

```text
work_id
scene_count
core_dist
episode_function
by
```

`core_dist`는 모든 SceneCard의 `core`와 non-null `core2`를 함께 집계한다.

## 5. Stage02 SequenceBlueprint — 정확히 18키

경로:

```text
authored_seq/<work>_<NN>.seqblueprint.jsonl
```

키:

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

자료형:

```json
{
  "seq_id": "string",
  "work_id": "string",
  "episode_no": 1,
  "seq_index": 1,
  "member_scene_nos": [1, 2, 3],
  "scene_span": [1, 3],
  "scene_budget": 3,
  "sequence_intent": "string",
  "goal": "string",
  "obstacle": "string",
  "value_shift": {"from": "string", "to": "string"},
  "turn_type": "TURN_TYPE",
  "turn_class": "TURN_CLASS",
  "core_mix": ["CORE_ENUM"],
  "pov_char": "string",
  "place_cluster": "string",
  "runtime_share": 0.123456,
  "by": "string"
}
```

### turn_type registry와 turn_class 파생

```text
RISE    → RISE
BOND    → RISE
PUNISH  → RISE

FALL    → FALL
LOSS    → FALL

REVEAL  → REVEAL
ORACLE  → REVEAL
REVERSAL→ REVEAL

STALL   → STALL
HOOK    → STALL
CONFLICT→ STALL
```

새 작품의 `turn_type`은 위 11종만 사용한다. Stage01의 ROMANCE, RESCUE, REUNION, RELIEF, INTRO, DESIRE, PERIL 등은 의미를 보존해 위 registry의 상위 변화 유형으로 재판정한다.

### Stage02 불변식

#### I-COVER

```text
모든 scene_no가 정확히 한 시퀀스에 포함
```

#### I-PARTITION

```text
장면 중복 0
장면 누락 0
```

#### I-COUNT

```text
sum(scene_budget) == episode scene_count
```

추가:

- `member_scene_nos`는 오름차순·연속
- `scene_span == [first(member), last(member)]`
- `scene_budget == len(member_scene_nos)`
- `value_shift` 키는 정확히 `from/to`
- `turn_class`는 매핑 결과와 일치
- `core_mix`는 member SceneCard의 실제 `core/core2`에 존재
- `sum(runtime_share) == 1.0` 허용 오차 1e-6
- `sequence_count / scene_count >= 0.11`
- 권장 밀도대 0.12~0.17
- 균등 장면 수 분할만으로 시퀀스를 만들지 않음

## 6. Stage03 EpisodeArc — 정확히 13키

경로:

```text
authored_arc/<work>_<NN>.episodearc.json
```

키:

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

### turning_point

```json
{
  "seq_index": 4,
  "desc": "실제 전환 설명"
}
```

`scene_no/event` 형태 또는 문자열은 금지한다.

### act_structure

```json
[
  {"act": "ACT1", "seq_span": [1, 3], "function": "..."},
  {"act": "ACT2", "seq_span": [4, 6], "function": "..."}
]
```

불변식:

- 모든 시퀀스를 정확히 한 act가 덮음
- act 간 overlap/gap 없음
- 실제 시퀀스 전환을 근거로 함
- 무조건 4개 act일 필요는 없으나 프로젝트 validator가 4막을 요구하면 사전에 계약을 고정

## 7. CharacterArc — 정확히 8키

경로:

```text
authored_chararc/<work>_<NN>.chararc.jsonl
```

키:

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

불변식:

- `character`가 trigger scene에 실제 등장
- 인물×회차 단위
- state_delta는 이번 회차 변화량
- 동일 evidence를 여러 인물에 복사 금지
- 실제 변화 없는 인물을 수량 채우기 위해 생성 금지

## 8. RelationshipArc — 정확히 9키

경로:

```text
authored_relarc/<work>_<NN>.relarc.jsonl
```

키:

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

불변식:

- 두 인물이 trigger scene에 함께 등장·통화·교신
- 관계쌍×회차 단위
- `(A,B)`와 `(B,A)` 중복 금지
- 관계 상태와 변화량을 구분
- 동일 evidence 반복 금지

## 9. LocalEdge — 정확히 12키

경로:

```text
authored_edges/<work>_<NN>.local_edges.jsonl
```

키:

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

불변식:

```text
edge_type == causal
src_episode_no == tgt_episode_no
gap_episodes == 0
```

- source/target 장면 실재
- `label == target SceneCard.core`
- `confidence`는 0~1
- note는 구체적 인과
- 단순 인접·유사 주제·시퀀스 순서는 인과가 아님

## 10. PayoffCandidate — 정확히 7키

경로:

```text
authored_edges/<work>_<NN>.payoff_candidates.jsonl
```

키:

```text
candidate_id
work_id
episode_no
scene_no
edge_type_guess
description
by
```

허용 `edge_type_guess`:

```text
plant_payoff
callback
subplot_counterpoint
resolved_here
```

후속 회차 확인 전 확정 엣지로 사용하지 않는다.

## 11. CrossEpisodeEdge — 정확히 12키

경로:

```text
authored_edges/<work>_cross_episode_edges.jsonl
```

키셋은 LocalEdge와 동일하다.

기본 불변식:

```text
tgt_episode_no > src_episode_no
gap_episodes == tgt_episode_no - src_episode_no
edge_type ∈ {callback, plant_payoff, subplot_counterpoint}
```

- source/target 장면 실재
- target `label`은 target SceneCard의 실제 CORE
- 실제 전 시즌 fan-in으로 확인
- 인접 회차 자동 브리지 금지

## 12. FullSeriesArc — 정확히 17키

경로:

```text
authored/<work>_full_series_arc.json
```

키:

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

자료형 요점:

- `protagonist`: object
- `antagonist`: object
- `season_structure`: list of movement objects
- `macro_turning_points`: list
- `open_ending`: boolean
- `series_core_dist`: CORE_ENUM별 int 집계

불변식:

- counts가 실제 전체 데이터와 일치
- movement episode span에 gap/역전 없음
- 기계적 4분기 대신 실제 매크로 전환
- resolution과 conflict_persist를 구분

## 13. QuarterAudit — 15키 기준

권장 경로:

```text
quarter_audits/<work>_<NN>_Q<Q>.json
```

키:

```text
schema
work_id
episode_no
quarter
scene_range
scene_count
source_scene_hashes
stage01_subset_sha256
placeholder_count
duplicate_title_count
duplicate_intent_count
direct_reading_completed
python_semantic_generation
status
by
```

통과 조건:

```text
direct_reading_completed == true
python_semantic_generation == false
placeholder_count == 0
status == LOCKED_PASS
```

## 14. SourceLock 최소 계약

SourceLock은 작품별 원본 형식에 따라 확장 가능하나 최소 다음을 포함한다.

```text
schema
work_id
episodes_total
canonical_scene_count_total
source_archive
scene_boundary_policy 또는 numbering_policy
direct_reading_required
python_semantic_generation
raw_script_exported
status
episodes
current_completed_episodes
next
```

각 episode:

```text
episode_no
source_filename
source_encoding
original_bytes_sha256
canonical_scene_count
quarter_ranges
scene_hashes 또는 heading hashes
source marker anomaly
```

## 15. CandidateDisposition ledger

Stage04는 모든 PayoffCandidate에 최종 disposition을 남긴다.

권장 상태:

```text
PROMOTED_CROSS_EDGE
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL
RESOLVED_WITHIN_EPISODE
REJECTED_DUPLICATE
REJECTED_INSUFFICIENT_EVIDENCE
REJECTED_SOURCE_MISMATCH
```

미처리 후보가 한 건이라도 있으면 Stage04 완료가 아니다.

## 16. 상태 enum

```text
DRAFT
CANDIDATE
QUARANTINE
PASS_CANDIDATE
CANONICAL
SUPERSEDED
```

세부 실행 판정은 접미어를 붙일 수 있다.

```text
PASS_CANDIDATE_FIRST_HALF_EP01_08
PASS_CANDIDATE_FULL_SERIES_STAGE01_04
PASS_LIMITED_HOLDOUT_NONBLINDED
```

`CANONICAL`은 사용자 승인 후에만 사용한다.
