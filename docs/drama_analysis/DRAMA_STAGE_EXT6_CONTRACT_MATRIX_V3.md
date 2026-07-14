# Stage01~04 및 EXT6 계약 매트릭스 v3

- Document ID: `DRAMA-STAGE-EXT6-CONTRACT-MATRIX-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Exact Stage01~04 schemas remain governed by `SCHEMA_CONTRACTS_V2.md`.

## 1. 계층 배치

| 시점 | 기존 계층 | EXT6 Phase 1 | 생성 방식 |
|---|---|---|---|
| Source preflight | SourceLock | SourceSceneAlignment 준비 | 결정론+수동 경계 판정 |
| Stage01 Q 직접독해 | SceneCard | EntityBridge, CastPresence, CastCoverageLedger | 직접 저작 |
| Stage02 완료 | SequenceBlueprint | CharacterLoad의 scene→sequence FK 준비 | 기존 저작+결정론 |
| Stage03 완료 | EpisodeArc/CharacterArc/RelationshipArc/LocalEdge/PayoffCandidate | CharacterLoad 확정 | Load는 결정론 |
| Stage04 완료 | CrossEpisodeEdge, FullSeriesArc, disposition | 시즌 Cast/Load 종합은 advisory | 직접 검증·종합 |

EXT6은 기존 SceneCard·SequenceBlueprint·Arc 파일에 필드를 추가하지 않는다. 모든 레코드는 sidecar로 저장한다.

## 2. Stage01~04 exact keyset 요약

### SceneCard — 9키

```text
work_id, scene_no, heading, title, intent_gist,
core, core2, skin, by
```

### EpisodeMeta — 5키

```text
work_id, scene_count, core_dist, episode_function, by
```

### SequenceBlueprint — 18키

```text
seq_id, work_id, episode_no, seq_index,
member_scene_nos, scene_span, scene_budget,
sequence_intent, goal, obstacle, value_shift,
turn_type, turn_class, core_mix, pov_char,
place_cluster, runtime_share, by
```

### EpisodeArc — 13키

```text
work_id, episode_no, scene_count, sequence_count,
dramatic_question, act_structure, entry_state, exit_state,
turning_point, central_conflict_axis, episode_function,
core_dist, by
```

### CharacterArc — 8키

```text
work_id, character, episode_no, state_label,
state_delta, trigger_scene_no, by, evidence
```

### RelationshipArc — 9키

```text
work_id, char_a, char_b, episode_no,
relation_state, relation_delta, trigger_scene_no,
evidence, by
```

### Local/Cross Edge — 12키

```text
edge_id, work_id, edge_type,
src_episode_no, src_scene_no,
tgt_episode_no, tgt_scene_no,
gap_episodes, label, confidence, note, by
```

### PayoffCandidate — 7키

```text
candidate_id, work_id, episode_no, scene_no,
edge_type_guess, description, by
```

### FullSeriesArc — 17키

```text
series, episodes_total, scenes_total, sequences_total,
logline, central_dramatic_question, theme_statement,
protagonist, antagonist, season_structure,
macro_turning_points, resolution, open_ending, tone,
conflict_persist, series_core_dist, by
```

## 3. EXT6 Phase 1 동결 행 스키마

### EntityBridgeRecord — 9키

Grain: `series work_id × character_key`.

```text
work_id
character_key
canonical_name
aliases
entity_id
mapping_status
source_registry_ref
source_registry_sha
by
```

- `character_key = <work_slug>:<canonical_name_slug>`.
- `entity_id`는 Page10 Entity Registry 매핑 전 `null`.
- `mapping_status ∈ {PROVISIONAL, MAPPED, CONFLICT}`.
- 장소·조직·시설을 인물로 등록하지 않는 Gate B7을 적용한다.

### CastPresenceRecord — 10키

Grain: `episode × scene × character`.

```text
work_id
episode_no
scene_no
character_key
entity_id
presence_mode
focality
speaking_status
evidence_ref
by
```

Enums:

```text
presence_mode:
ONSCREEN
VOICE_ONLY
PHONE_OR_REMOTE
ARCHIVAL_OR_MEMORY
REFERENCED_ONLY

focality:
PRIMARY
SECONDARY
PRESENT_ONLY

speaking_status:
SPEAKING
NONSPEAKING
```

규칙:

- `REFERENCED_ONLY`는 등장 분량에서 제외.
- scene당 PRIMARY는 0~복수 가능.
- `evidence_ref`는 짧은 근거 지시·offset·hash이며 원문 장문 저장을 금지.

### CharacterLoadRecord — 17키

Grain: `episode × character`.

```text
work_id
episode_no
character_key
entity_id
canonical_name
present_scene_count
focal_scene_count
speaking_scene_count
present_sequence_count
scene_share
focal_share
scene_share_band
act_placement
first_scene_no
last_scene_no
max_absence_gap
by
```

결정론 식:

```text
present_scene_count = distinct scenes where presence_mode != REFERENCED_ONLY
focal_scene_count = distinct scenes where focality == PRIMARY
speaking_scene_count = distinct scenes where speaking_status == SPEAKING
present_sequence_count = distinct seq_id containing a present scene
scene_share = present_scene_count / episode_scene_count
focal_share = focal_scene_count / episode_scene_count
max_absence_gap = max(adjacent present scene_no difference - 1)
```

Band:

```text
DOMINANT: 0.50 <= x
MAJOR:    0.20 <= x < 0.50
MINOR:    0.05 <= x < 0.20
CAMEO:            x < 0.05
```

## 4. EXT6 보조 아티팩트 v2

### CastCoverageLedger

```text
work_id
episode_no
episode_scene_count
annotated_scene_nos
empty_cast_scene_nos
unresolved_scene_nos
union_count
by
```

불변식:

```text
세 집합은 상호배타
합집합 == 1..episode_scene_count
union_count == episode_scene_count
```

### SourceSceneAlignmentRecord

권장 키:

```text
work_id
episode_no
scene_no
scene_heading
source_heading_indexes
alignment_type
source_char_offsets
source_line_refs
source_hashes
source_text_sha256
alignment_note
status
by
```

Enums:

```text
alignment_type:
ONE_TO_ONE
MERGED_PHYSICAL_HEADINGS
DUPLICATE_SOURCE_ARTIFACT

status:
VERIFIED_AUTOMATED
VERIFIED_MANUAL_REVIEWED
```

문자 offset과 블록별 hash를 1급 provenance로 사용한다. line reference는 추출기 의존 참고값이다.

## 5. 작품/회차 식별자 경계

Stage01~04의 기존 회차 파일에서는:

```text
work_id = <work>_<NN>
```

EXT6 sidecar에서는 비교·집계 안정성을 위해:

```text
work_id = <work>
episode_no = NN
```

을 사용한다. 두 규칙을 파일 내부에서 혼용하지 않는다.

## 6. 실험 계층

다음은 필요성이 합의됐으나 exact schema가 동결되지 않았다.

- CharacterVoice
- MotifLedger
- ThematicStance
- AffectRegister
- Tone/Pacing
- Narration/POV substrate

이들은 근거 후보를 별도 advisory 파일에 기록할 수 있으나 정본 승격·전 코퍼스 rollout은 금지한다.
