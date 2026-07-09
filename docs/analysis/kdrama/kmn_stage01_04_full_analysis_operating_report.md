# 결혼못하는남자 Stage01~04 전체 분석 운영 보고서 및 허브 핸드오프

- work_id: `결혼못하는남자`
- scope: EP01~EP16, Stage01~Stage04
- package style: Claude `seqcard_ko.zip` 호환 골격 + GPT 직접독해 provenance 확장
- canonical developer package SHA256: `488ae8f23dc5c598836c8896ef421d8603cae3649a7f78f6364a55f8bc6c3755`
- precision audit SHA256: `e90e4dff2438cc2997a7a21efa74e1070d838a619b063d7c47f23682ae1ebd1c`
- final decision: `PASS_FINAL_STAGE01_04_PRECISION_AUDIT`
- raw_script_exported: `false`
- provider_call_count: `0`

## 0. 이 문서의 목적

이 보고서는 현재 대화방의 세션 한도 이후 새 대화방이나 개발자 환경에서 **다른 드라마를 즉시 같은 품질 기준으로 분석**할 수 있도록, 결혼못하는남자 분석에서 확정된 방식·순서·규격·검증법·실패 처리·패키징 규칙을 체계적으로 보존하기 위한 허브 로드 문서다.

핵심 전제는 다음이다.

```text
Stage01~02는 장면/시퀀스 직접독해의 저층 의미층이다.
Stage03~04는 저층 의미층을 바탕으로 Arc / Edge / Season Wiring을 구축하는 상위 구조층이다.
Stage03~04는 Stage01~02가 오염되면 반드시 재빌드한다.
Python은 의미 저작자가 아니라 추출·정렬·검증·패키징 도구다.
```

## 1. 최종 산출물 상태

### 1.1 개발자 전달 패키지

```text
file: kmn_stage01_04_developer_delivery_claude_style_v1.zip
sha256: 488ae8f23dc5c598836c8896ef421d8603cae3649a7f78f6364a55f8bc6c3755
size_bytes: 2406153
```

이 패키지는 Claude style 폴더 체계를 기준으로 다음을 포함한다.

```text
authored/          EP별 Stage01 seqcard 및 episode_meta
authored_seq/      EP별 Stage02 SequenceBlueprint JSONL 및 ALL index
authored_arc/      EP별 episode_arc 및 series_arc
authored_edges/    Stage03 local_edges / cross_episode_edges
authored_chararc/  Stage03 character_arc
authored_relarc/   Stage03 relationship_arc
authored_payoff/   Stage03 payoff_candidates
authored_series/   Stage03 series_arc
season_wiring/     Stage04 season_wiring_graph / closure matrix / episode role map / tension curve / closure report
validation/        EP별 및 Stage03~04 검증 산출물
source_lock/       no_raw source lock / source map
stage01_02/        canonical EP01~16 ZIP 보존
quarantine/        실패본·비승격본 manifest
method_comparison/ GPT vs Claude 방식 비교 문서
scripts_reference/ 재작성·검증·빌드 기준 스크립트 참조
```

### 1.2 정밀 감사 패키지

```text
file: kmn_stage01_04_precision_quality_audit_v4.zip
sha256: e90e4dff2438cc2997a7a21efa74e1070d838a619b063d7c47f23682ae1ebd1c
size_bytes: 4088
```

정밀 감사 결과는 다음을 확인했다.

```text
zip_integrity: PASS
sidecar_sha256_match: True
internal_sha256s_checked: 248
internal_sha256_failures: 0
raw_source_file_entries: []
final_decision: PASS_FINAL_STAGE01_04_PRECISION_AUDIT
```

## 2. 최종 정량 요약

```text
episode_count: 16
scene_count: 1249
sequence_count: 189
template_contamination_hits: 0
visible_reference_markers: 0
raw_script_exported: false
episode_failures: 0
```

Stage03~04 요약:

```text
character_arcs: 6
relationship_arcs: 9
local_edges: 173
cross_episode_edges: 15
payoff_candidates: 12
season_wiring_nodes: 217
season_wiring_edges: 401
payoff_closure_rows: 12
episode_role_rows: 16
tension_curve_points: 16
```

## 3. 회차별 최종 상태

| 회차 | Stage01 scenes | Stage02 sequences | depth_avg | depth_min | EP ZIP SHA | decision |
|---:|---:|---:|---:|---:|---|---|
| EP01 | 96 | 12 | 3.333 | 2.8 | c5ba72876390… | PASS_CANONICAL_INPUT |
| EP02 | 81 | 12 | 3.383 | 3.2 | 340d6c2139da… | PASS_CANONICAL_INPUT |
| EP03 | 77 | 12 |  |  | 12af821409d7… | PASS_CANONICAL_INPUT |
| EP04 | 72 | 12 |  |  | 7ded91a66ca6… | PASS_CANONICAL_INPUT |
| EP05 | 78 | 12 |  |  | 601f9a9d5753… | PASS_CANONICAL_INPUT |
| EP06 | 69 | 12 |  |  | 032083845570… | PASS_CANONICAL_INPUT |
| EP07 | 63 | 9 |  |  | 244158a52b7e… | PASS_CANONICAL_INPUT |
| EP08 | 102 | 12 | 3.55 | 3.05 | d3a956ea81ee… | PASS_CANONICAL_INPUT |
| EP09 | 59 | 12 |  |  | 875c98507aba… | PASS_CANONICAL_INPUT |
| EP10 | 52 | 12 |  |  | d593fb082430… | PASS_CANONICAL_INPUT |
| EP11 | 71 | 12 | 3.3 | 2.6 | 306c3f840d5b… | PASS_CANONICAL_INPUT |
| EP12 | 94 | 12 | 3.495 | 3.0 | 14f355556731… | PASS_CANONICAL_INPUT |
| EP13 | 81 | 12 | 3.48 | 2.8 | 28bef26713d1… | PASS_CANONICAL_INPUT |
| EP14 | 88 | 12 | 3.53 | 3.0 | d3ccb5d3f98b… | PASS_CANONICAL_INPUT |
| EP15 | 82 | 12 | 3.05 | 3.05 | 5fb753db55af… | PASS_CANONICAL_INPUT |
| EP16 | 84 | 12 | 3.454 | 3.2 | 27c41cbd6022… | PASS_CANONICAL_INPUT |

정밀 감사 scorecard:

| 회차 | decision | Stage1 cards | Stage2 seq | template cards | visible refs | field copy | runtime share |
|---:|---|---:|---:|---:|---:|---:|---:|
| EP01 | PASS | 96 | 12 | 0 | 0 | 0 | 1.0 |
| EP02 | PASS | 81 | 12 | 0 | 0 | 0 | 1.0 |
| EP03 | PASS | 77 | 12 | 0 | 0 | 0 | 1.0 |
| EP04 | PASS | 72 | 12 | 0 | 0 | 0 | 1.0 |
| EP05 | PASS | 78 | 12 | 0 | 0 | 0 | 1.0 |
| EP06 | PASS | 69 | 12 | 0 | 0 | 0 | 1.0 |
| EP07 | PASS | 63 | 9 | 0 | 0 | 0 | 1.0 |
| EP08 | PASS | 102 | 12 | 0 | 0 | 0 | 1.0 |
| EP09 | PASS | 59 | 12 | 0 | 0 | 0 | 1.0 |
| EP10 | PASS | 52 | 12 | 0 | 0 | 0 | 1.0 |
| EP11 | PASS | 71 | 12 | 0 | 0 | 0 | 1.0 |
| EP12 | PASS | 94 | 12 | 0 | 0 | 0 | 1.0 |
| EP13 | PASS | 81 | 12 | 0 | 0 | 0 | 1.0 |
| EP14 | PASS | 88 | 12 | 0 | 0 | 0 | 1.0 |
| EP15 | PASS | 82 | 12 | 0 | 0 | 0 | 1.0 |
| EP16 | PASS | 84 | 12 | 0 | 0 | 0 | 1.0 |

## 4. Stage01 — SceneCard 직접독해 계층

### 4.1 목적

Stage01은 원본 회차를 장면 단위로 잠그고, 각 장면의 의미 기능을 직접 독해하여 장면 카드로 기록하는 계층이다. 장면 요약이 아니라 **행동·발화/침묵·정보 변화·선택·구조 기능·후속 원인**을 분리해 기록한다.

### 4.2 기본 실행 순서

```text
1. 원본 회차 추출
2. scene marker 확인
3. canonical scene ordinal 부여
4. source_marker_no와 canonical ordinal 분리 보존
5. source_lock.no_raw 생성
6. episode를 Q1~Q4로 분할
7. Q1 Stage01 직접독해 작성
8. Q1 부분 Stage02 작성
9. Q1 검증 및 보강
10. Q2→Q3→Q4 동일 반복
11. Q1~Q4 통합 Stage01 생성
12. 회차 전체 Stage02 재정렬
13. 회차 synopsis 생성
14. 회차 validation 및 ZIP packaging
```

Q 단위는 사용자 승인 단위가 아니라 **자동화 전환 방지용 독해 단위**다. 사용자가 한 회차를 요청하면 내부적으로 Q1~Q4를 순차 처리하되, 사용자의 반복 승인을 요구하지 않는다.

### 4.3 Stage01 canonical 필드

```json
{
  "work_id": "작품명",
  "episode_no": 1,
  "scene_ordinal": 1,
  "source_marker_no": "원본 마커",
  "source_span": {"canonical_scene_ordinal": 1, "source_marker_no": 1, "body_sha16": "..."},
  "source_sha16": "...",
  "heading": "장면 표제",
  "title": "분석 제목",
  "scene_action": "장면에서 실제 벌어진 행동",
  "spoken_or_unspoken_move": "말한 것/피한 것/숨긴 것/행동으로 대신한 것",
  "information_delta": "이 장면 때문에 달라진 정보·오해·조건",
  "character_decision": "인물이 실제 선택·거부·회피·연기·보류한 것",
  "dramatic_function": "회차 구조 안에서 이 장면이 하는 기능",
  "forward_hook": "다음 장면·시퀀스를 밀어내는 구체 원인",
  "stage2_hint": null,
  "core": "16 taxonomy 중 1차값",
  "core2": "보조 taxonomy 또는 null",
  "pov_char": "주 관점 인물",
  "place_cluster": "공간 cluster",
  "evidence_control": {"raw_script_exported": false, "direct_reading_required": true, "python_meaning_generation": false}
}
```

### 4.4 Stage01 직접독해 원칙

`scene_action`은 표면 행동이다. `spoken_or_unspoken_move`는 대화 또는 회피 전략이다. `information_delta`는 새로 생긴 정보나 오해다. `character_decision`은 장면 안에서 인물이 실제로 선택한 것이다. `dramatic_function`은 구조적 역할이며, `forward_hook`은 다음 장면으로 넘어가는 압력이다.

이 여섯 의미 필드는 서로 독립해야 한다. 한 필드의 문장을 다른 필드에 확장 복사하면 실패다.

### 4.5 금지 규칙

```text
make_card()
keywords()
theme()
specific_delta()
auto_forward_hook()
derive_information_delta()
derive_character_decision()
generate_dramatic_function()
반복 문형으로 의미 필드 채우기
scene_action 문장을 다른 필드에 삽입하기
visible source marker를 의미 필드 안에 남기기
raw dialogue / raw script export
```

EP14~16 초기 실패와 EP14 최종 재오염은 이 규칙을 위반해 최종 감사에서 차단되었다. 최종 canonical은 재작성 및 정밀 감사를 거쳐 통과한 ZIP만 사용한다.

## 5. Stage02 — SequenceBlueprint 계층

### 5.1 목적

Stage02는 Stage01 장면들을 시퀀스 단위로 묶고, 회차 내부의 목표·장애·가치 변화·전환을 구조화한다. Stage02는 Stage01 이후 붙이는 요약이 아니라, Q 단위에서 Stage01을 되돌려 보강하는 feedback layer다.

### 5.2 18필드 SequenceBlueprint

```json
{
  "seq_id": "결혼못하는남자_01_S01",
  "work_id": "결혼못하는남자_01",
  "episode_no": 1,
  "seq_index": 1,
  "member_scene_nos": [1,2,3],
  "scene_span": [1,3],
  "scene_budget": 3,
  "sequence_intent": "시퀀스의 구조적 의도",
  "goal": "인물이 얻거나 지키려는 것",
  "obstacle": "목표를 막는 압력",
  "value_shift": {"from": "이전 가치", "to": "이후 가치"},
  "turn_type": "CONFLICT 등",
  "turn_class": "RISE/FALL/TURN 등",
  "core_mix": ["ESTABLISH","CONFLICT"],
  "pov_char": "주 관점 인물",
  "place_cluster": "공간 cluster",
  "runtime_share": 0.083333,
  "by": "gpt-5.5-direct-reading"
}
```

### 5.3 16 taxonomy

```text
ESTABLISH, ORACLE, INTRO, BOND, CONFLICT, REVERSAL, LOSS, PUNISH,
REVELATION, REUNION, RELIEF, ROMANCE, PERIL, RESCUE, DESIRE, HOOK
```

### 5.4 Stage02 검증

```text
required 18 fields present
core_mix taxonomy values valid
member_scene_nos coverage exact
missing scenes = 0
duplicate coverage = 0
runtime_share sum = 1.0
scene_span/member_scene_nos consistency
sequence_count acceptable for episode shape
```

## 6. Stage03 — Arc / Edge 확장

### 6.1 목적

Stage03은 Stage01의 장면 카드와 Stage02의 시퀀스 블루프린트를 연결하여 작품 전체의 인물 변화, 관계 변화, 근거리/장거리 인과망, 복선 후보를 만든다. 이 계층은 raw script가 아니라 **scene id / sequence id / taxonomy / synopsis / evidence metadata**만 사용한다.

### 6.2 산출물

```text
SeriesArc
CharacterArc
RelationshipArc
LocalEdge
CrossEpisodeEdge
PayoffCandidate
```

### 6.3 CharacterArc

한 인물이 EP01~EP16을 거치며 겪는 가치관·관계성·행동전략의 궤적이다. 이 패키지는 6개 character arc를 포함한다.

핵심 필드:

```text
character_arc_id
work_id
character
episode_span
appearance_episode_count
arc_summary
arc_phase_map
trigger_beats
evidence_control
by
```

### 6.4 RelationshipArc

두 인물 또는 관계 단위가 어떤 동역학으로 시작해 어떤 결말로 닫히는지를 기록한다. 이 패키지는 9개 relationship arc를 포함한다.

핵심 필드:

```text
relationship_arc_id
work_id
source_character
target_character
relationship_type
episode_span
arc_statement
trigger_beats
evidence_control
by
```

### 6.5 LocalEdge

단일 회차 또는 인접한 시퀀스 사이의 즉각적 인과 연결이다. 이 패키지는 173개 local edge를 포함한다.

핵심 필드:

```text
edge_id
work_id
edge_type
src_episode_no
src_sequence_id
src_scene_no
tgt_episode_no
tgt_sequence_id
tgt_scene_no
gap_episodes
label
core_bridge
confidence
note
by
```

### 6.6 CrossEpisodeEdge

먼 회차 또는 회차 경계 사이의 장기 인과 연결이다. 이 패키지는 15개 cross episode edge를 포함한다.

### 6.7 PayoffCandidate

시즌 후반 또는 결말에서 회수되어야 하는 setup/closure 후보군이다. 이 패키지는 12개 payoff candidate를 포함한다.

## 7. Stage04 — Season Wiring / Payoff Closure 통합

### 7.1 목적

Stage04는 Stage03의 Arc / Edge / Payoff 후보를 하나의 시즌 구조로 통합하고, 설정·복선·관계·인물 아크가 결말까지 닫히는지 검증한다.

### 7.2 산출물

```text
season_wiring_graph
payoff_setup_closure_matrix
episode_role_map
tension_role_curve
character_relation_closure_report
```

### 7.3 season_wiring_graph

시즌 전체에서 episode node, character arc node, relationship arc node, edge node, payoff node를 연결한다. 최종 감사 기준 nodes 217, edges 401이다.

### 7.4 payoff_setup_closure_matrix

Stage03의 payoff candidates 12개가 setup_ref와 closure_ref를 가지는지 검증한다. unresolved setup이 있으면 Stage04는 PASS할 수 없다.

### 7.5 episode_role_map

EP01~EP16 각 회차가 시즌 전체에서 맡는 전략적 역할을 기록한다. 필수 회차 set은 1~16이며 누락이 없어야 한다.

### 7.6 tension_role_curve

16개 episode point로 시즌의 긴장 곡선을 표시한다. 단순 숫자 그래프가 아니라 episode role, dominant core mix, arc pressure를 종합한 구조적 리듬이다.

### 7.7 character_relation_closure_report

피날레에서 주요 character arc와 relationship arc가 결말 논리와 부합하는지 설명한다. raw script 인용 없이 Stage01~03의 evidence id만 사용한다.

## 8. 품질 밀도 및 깊이 기준

### 8.1 Stage01 content depth scoring

SceneCard는 0~4점 기준으로 밀도를 본다.

```text
4점: 행동·발화/침묵·정보 변화·선택·구조 기능·후속 원인이 모두 구체적이다.
3점: 대체로 구체적이나 하나의 필드가 약하다.
2점: 장면 요약은 있으나 선택·정보 변화가 추상적이다.
1점: 키워드 중심 또는 반복 문형 중심이다.
0점: 자동 생성·필드 복사·원문 조각 삽입이다.
```

통과 기준:

```text
content_depth_avg >= 3.0 권장
content_depth_min >= 2.5 권장
zero_score_cards = 0
one_score_cards = 0
field_copy_errors = 0
keyword_artifacts = blocking only when semantic corruption exists
visible_ref_templates = 0
```

### 8.2 정밀 감사의 hard blocking 조건

```text
template_contamination_cards > 0
visible_reference_markers > 0
field_copy_errors > 0
required semantic fields missing
Stage02 required fields missing
Stage02 coverage missing/extra/duplicate
raw source file entries present
SHA256 mismatch
ZIP integrity failure
Stage03 edge/payoff reference errors
Stage04 missing episode role or payoff closure rows
```

## 9. 실패/격리 사례와 학습된 규칙

### 9.1 EP05~06 batch 실패

초기 EP05~06 배치는 2회차를 묶으면서 직접독해 모드가 산출물 완성 모드로 전환되었다. 이때 Python/템플릿 기반 의미 생성 흔적이 검출되어 quarantine 처리되었다.

학습 규칙:

```text
2회차 이상 묶음은 validation/package 단위일 수는 있으나 의미 저작 단위가 되면 안 된다.
기본 생산 단위는 1회차 × 4Q다.
```

### 9.2 EP14~16 template contamination

EP14~16 초기 산출물에는 `장면001`, `맥락001`, `발화층`, `정보변화`, `결정층` 계열의 템플릿 골격이 남아 있었다. 최종 감사에서 EP14~16 전체가 FAIL 처리되었고, clean rewrite 후 Stage03~04를 재빌드했다.

### 9.3 EP14 재오염 및 최종 교정

EP14는 한 번 재작성 후에도 `행동독해001`, `발화독해001`, `정보독해001` 계열 토큰이 정밀 감사에서 다시 검출되었다. 최종 조치에서 EP14를 다시 고치고 Stage03~04와 개발자 전달 ZIP을 재생성했다.

이 사례가 확정한 원칙:

```text
보고서상 PASS를 신뢰하지 않는다.
항상 최종 ZIP 내부의 authored/*.seqcard.jsonl을 직접 검사한다.
Stage03~04는 하위 입력 오염이 발견되면 무조건 재빌드한다.
```

## 10. 검증 방법

### 10.1 ZIP / SHA 검증

```text
outer package SHA256 계산
sidecar SHA256 비교
internal SHA256SUMS.txt 존재 확인
internal SHA256SUMS 전체 검사
zipfile.testzip() 통과
```

### 10.2 Stage01 검증

```text
required field presence
semantic field non-empty
forbidden template tokens scan
visible reference marker scan
keyword artifact scan
field-copy / scene_action embedding scan
exact duplicate semantic value scan
repeated n-gram scan
raw_script_exported false
python_meaning_generation false
```

### 10.3 Stage02 검증

```text
18 required fields present
taxonomy values valid
member_scene_nos coverage exact
runtime_share sum 1.0
sequence_count valid
```

### 10.4 Stage03 검증

```text
character_arc required keys
relationship_arc required keys
local_edge required keys
cross_episode_edge required keys
payoff_candidate required keys
edge src/tgt refs point to existing episodes/scenes/sequences
payoff setup/closure refs point to known records
series_arc present
```

### 10.5 Stage04 검증

```text
season_wiring_graph present
season_wiring nodes/edges non-empty
payoff_setup_closure_matrix covers all payoff candidates
episode_role_map covers EP01~EP16
tension_role_curve has 16 points
character_relation_closure_report present
```

## 11. Claude 방식과 GPT 방식의 차이

Claude 확장 방식은 `seqcard_ko.zip` 계열처럼 `authored`, `authored_seq`, `authored_arc`, `authored_edges`, `authored_chararc`, `authored_relarc`의 폴더 체계와 확장 스키마 discipline이 강하다. 비밀의숲과 내이름은김삼순의 최신 확장 방식은 Stage03 계층의 ID namespace, edge/arc schema, anti-gaming 검증에 비교 기준을 제공한다.

GPT 방식은 이번 결혼못하는남자 분석에서 다음이 강점이었다.

```text
직접독해 provenance
source_lock.no_raw
Q 단위 독해 루프
Stage01/2 오염 감지
quarantine-first 정책
하위 입력 오염 시 Stage03/4 재빌드
raw script zero
최종 ZIP 내부 직접 감사
```

최종 표준은 다음의 hybrid이다.

```text
Claude-style expanded schema discipline
+ GPT-style direct-reading provenance and fail-closed input audit
= canonical Stage01~04 drama analysis operating protocol
```

## 12. 다른 드라마에 즉시 적용하는 실행 절차

새 드라마는 아래 순서로 실행한다.

```text
A. Source inventory
   - 작품/회차 목록 작성
   - raw script는 export 금지
   - 회차별 source lock 생성

B. Stage01/2 per episode
   - 1회차 4Q로 분할
   - Q1 Stage01 + partial Stage02 작성
   - Q1 검증 및 보강
   - Q2/Q3/Q4 반복
   - integrated Stage01 + full Stage02 생성
   - 회차 ZIP 생성

C. Stage01/2 full season audit
   - authored/*.seqcard.jsonl 직접 검사
   - authored_seq/*.seqblueprint.jsonl coverage 검사
   - 모든 회차 PASS 후 다음 단계 진행

D. Stage03 build
   - CharacterArc / RelationshipArc / LocalEdge / CrossEpisodeEdge / PayoffCandidate / SeriesArc 생성
   - raw script 사용 금지
   - scene_id / sequence_id evidence만 사용

E. Stage04 build
   - season_wiring_graph 생성
   - payoff_setup_closure_matrix 생성
   - episode_role_map 생성
   - tension_role_curve 생성
   - character_relation_closure_report 작성

F. Developer delivery package
   - Claude-style 폴더 체계로 정규화
   - GPT provenance / validation / quarantine / method comparison 추가
   - SHA256SUMS 생성

G. Precision audit
   - final ZIP 내부를 직접 검사
   - PASS 전까지 canonical 승격 금지
```

## 13. 다음 대화방 시작 지시문

```text
Continue the V1700 Literary OS drama-analysis pipeline from the KMN Stage01~04 hub handoff. Read docs/analysis/kdrama/kmn_stage01_04_full_analysis_operating_report.md, docs/development/kmn_stage01_04_next_chat_handoff.md, and release/current/drama_close_reading/kmn/stage01_04_final_delivery_manifest.json. Use the KMN protocol as the canonical operating standard for new drama analysis: one episode × four quarters, Stage01 SceneCard direct reading, Stage02 SequenceBlueprint feedback, Stage03 Arc/Edge, Stage04 Season Wiring, no raw script export, fail-closed validation, quarantine contaminated outputs, and rebuild upper stages whenever lower-stage contamination is found.
```

## 14. Hub load rule

GitHub에는 raw script나 원문 대사를 올리지 않는다. 최종 ZIP은 binary artifact로 별도 보관하거나 release asset으로 관리하고, repo에는 아래를 커밋한다.

```text
운영 보고서
핸드오프 문서
manifest
precision audit summary
package inventory
method comparison
artifact SHA256 records
```

이 문서는 결혼못하는남자 분석 결과를 단순 결과물이 아니라 **다음 드라마 분석을 재현 가능한 프로토콜**로 승격시키기 위한 기준 문서다.
