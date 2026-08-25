# 결혼못하는남자 EP01~EP04 직접독해 분석 방식 및 결과 적재 기록

## 0. 문서 목적

이 문서는 `결혼못하는남자` EP01~EP04에 대해 ChatGPT가 수행한 직접독해 기반 드라마 분석의 **방식, 순서, 필드 계약, 품질 검증, 산출물 manifest**를 허브에 고정하기 위한 기록이다.

이 문서는 원문 대본을 저장하지 않는다. 분석 산출물은 `no_raw` source map, Stage1 SceneCard, Stage2 SequenceBlueprint, synopsis, validation, manifest 중심으로 관리한다.

## 1. 핵심 판정

| Episode | Scenes | Sequences | Decision | SHA256 |
|---:|---:|---:|---|---|
| EP01 | 96 | 12 | `PASS_FINAL_EP01_DIRECT_READING_VALIDATED` | `c5ba72876390402c131030f598e7f6962dc7f0a48ea300ba01ee0f75db67afb1` |
| EP02 | 81 | 12 | `PASS_FINAL_EP02_DIRECT_READING_VALIDATED` | `340d6c2139dab6c37bb2cf98141402e5c1344c57be7b554f6393bd052ae36248` |
| EP03 | 77 | 12 | `PASS_FINAL_EP03_DIRECT_READING_VALIDATED` | `12af821409d7c049d61ae34673b43d17b649e1ed7a016e6dd360abdfe67fc349` |
| EP04 | 72 | 12 | `PASS_FINAL_EP04_DIRECT_READING_VALIDATED` | `7ded91a66ca64c7850c8ce1fd448ff2504ec160dcb1770f431d3fd622072c8f6` |

Aggregate:

- Episodes: 4
- Total scenes: 326
- Total SequenceBlueprint records: 48
- Raw script exported: `false`
- Promotion status: `canonical candidate`, subject to independent future re-audit

## 2. 분석 운영 원칙

### 2.1 Q는 사용자 승인 단위가 아니라 내부 품질 루프다

한 회차는 내부적으로 Q1~Q4로 분리한다. 그러나 Q마다 사용자에게 승인을 요청하지 않는다. 각 Q는 다음 품질을 만족해야 다음 Q로 진행한다.

1. 해당 Q의 모든 scene ordinal 존재
2. Stage1 의미 필드 직접 저작
3. Stage2 partial sequence hint 생성
4. 반복 골격과 keyword artifact 검사
5. 실패 장면은 Q 내부에서 repair 후 진행

### 2.2 회차 잠금 순서

```text
source extract
→ scene boundary normalization
→ source_lock.no_raw
→ Q1 Stage1 + partial Stage2
→ Q2 Stage1 + partial Stage2
→ Q3 Stage1 + partial Stage2
→ Q4 Stage1 + partial Stage2
→ full episode Stage2 rebuild
→ synopsis from sequence turns
→ validation
→ package manifest + SHA256
```

### 2.3 2회차 이상 확장의 교훈

EP05~06 batch 실패에서 확인된 원칙은 다음이다.

```text
batch = 검증·포장 단위
batch ≠ 의미 필드 동시 생성 단위
```

따라서 이후 2회차 이상 진행은 다음 중 하나만 허용된다.

1. **순차 회차 잠금:** EPn 완료·검증·LOCK 후 EPn+1 시작
2. **진짜 멀티 에이전트:** Writer Agent가 제한된 회차를 맡고, Supervisor/Verifier가 별도 검증

## 3. Stage1 SceneCard 필드 계약

Required fields:

```text
work_id
episode_no
scene_ordinal
source_marker_no
source_span
source_sha16
heading
title
scene_action
spoken_or_unspoken_move
information_delta
character_decision
dramatic_function
forward_hook
stage2_hint
evidence_control
```

의미 필드 해석:

- `scene_action`: 실제 장면에서 벌어지는 행동축
- `spoken_or_unspoken_move`: 말해진 것, 회피된 것, 숨겨진 것, 행동으로 대체된 것
- `information_delta`: 새 정보, 오해, 압력, 관계 조건의 변화
- `character_decision`: 선택, 거절, 연기, 은폐, 수행
- `dramatic_function`: 회차 구조 안에서 이 장면이 존재하는 이유
- `forward_hook`: 다음 장면/sequence를 미는 구체적 원인

Forbidden:

```text
scene_action을 다른 의미 필드에 복사
EPxx-yyy visible reference marker를 의미 필드에 삽입
원문 대사/본문 export
keyword fragment 기반 문장 생성
반복 skeleton phrase
Python으로 의미 필드 생성
검증 전 PASS 선언
```

## 4. Stage2 SequenceBlueprint 18필드 계약

Required fields:

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

`core_mix`는 다음 16기능 taxonomy 내부 값만 허용한다.

```text
ESTABLISH, ORACLE, INTRO, BOND, CONFLICT, REVERSAL, LOSS, PUNISH,
REVELATION, REUNION, RELIEF, ROMANCE, PERIL, RESCUE, DESIRE, HOOK
```

## 5. 회차별 처리 결과 요약

### EP01

- Package: `kmn_ep01_forced_direct_reading_final_v1.zip`
- Scenes: `96`
- SequenceBlueprint: `12`
- Q split: `1~24 / 25~48 / 49~72 / 73~96`
- Content depth avg/min: `3.333 / 2.8`
- Repeated ngram warning: `0`
- Banned phrase hits: `0`
- Duplicate semantic field: `0`
- Core mix provenance errors: `0`

### EP02

- Package: `kmn_ep02_forced_direct_reading_final_v1.zip`
- Scenes: `81`
- SequenceBlueprint: `12`
- Q split: `1~20 / 21~40 / 41~60 / 61~81`
- Content depth avg/min: `3.383 / 3.2`
- Repeated ngram warning: `0`
- Banned phrase hits: `0`
- Duplicate semantic field: `0`
- Core mix provenance errors: `0`

### EP03

- Package: `kmn_ep03_forced_direct_reading_final_v1.zip`
- Scenes: `77`
- SequenceBlueprint: `12`
- Q split: `1~19 / 20~39 / 40~58 / 59~77`
- Content depth avg/min: `3.42 / 3.0`
- Repeated ngram warning: `0`
- Banned phrase hits: `0`
- Duplicate semantic field: `0`
- Core mix provenance errors: `0`
- Non-blocking warning: `short_semantic_fields:4`

### EP04

- Package: `kmn_ep04_forced_direct_reading_final_v1.zip`
- Scenes: `72`
- SequenceBlueprint: `12`
- Q split: `1~18 / 19~36 / 37~54 / 55~72`
- Content depth avg/min: `3.752 / 3.47`
- Repeated ngram warning: `0`
- Banned phrase hits: `0`
- Duplicate semantic field: `0`
- Core mix provenance errors: `0`

## 6. 허브 반영 범위

허브에는 다음을 반영한다.

```text
허용:
- 방식/순서/품질 계약 문서
- manifest / SHA256 / validation summary
- no_raw source policy
- release gate script
- Codex 실험 설계

금지:
- 원문 HWP/TXT/DOC/PDF
- 대사/장면 본문 전문
- source excerpt
- provider live output
- raw vector payload
- adapter/model weight
- token/secret
```

## 7. 다음 단계

1. EP05~06 실패 batch는 quarantine record로 보존한다.
2. Codex 실험은 멀티 에이전트 구조로 설계하되, 원문 처리는 로컬 private archive에서 수행한다.
3. Writer Agent는 1~2회차만 담당하고, Supervisor/Verifier가 독립 검증한다.
4. 최종 허브 적재는 metadata-only release pack만 허용한다.
