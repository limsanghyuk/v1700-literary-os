# GPT 독립 설계안 — EXT6 Phase 01 계약·이중 분석 트랙

- 문서 ID: `GPT-EXT6-PHASE01-INDEPENDENT-v1`
- 상태: `INDEPENDENT_DRAFT_FOR_CROSS_COMPARISON`
- 작성일: 2026-07-14
- 작성 주체: GPT 트랙
- 목적: Claude 독립안과 비교하기 전 GPT 단독 설계안을 봉인한다.
- 권위 경계: 본 문서는 제안서이며 Stage01~04 정본을 변경하거나 Stage05를 공식화하지 않는다.

---

## 0. 결론

Phase 01의 목적은 새 문학 분석층을 곧바로 대규모 저작하는 것이 아니다. 다음 네 가지를 먼저 고정하는 것이다.

1. 기존 Stage01~04를 훼손하지 않는 EXT6 포착·파생·종합 시점
2. P0인 EntityBridge / CastPresence / CharacterLoad의 정확 계약
3. GPT와 Claude가 같은 원문을 독립 분석할 때 결과를 덮어쓰지 않는 이중 트랙 계약
4. 두 결과를 비교·판정하되 자동 평균이나 무근거 병합을 금지하는 합의 절차

최종 권고:

```text
Phase01 = 계약·식별자·포착시점·이중트랙·검증기 설계
Phase02 = 비밀의숲 P0 파일럿
Phase03 = GPT/Claude 독립 결과 비교
Phase04 = 사용자 승인 합의 계약 동결
```

---

## 1. 비타협 원칙

### 1.1 기존 분석 권위 불변

```text
SourceLock
→ Stage01 SceneCard
→ Stage02 SequenceBlueprint
→ Stage03 EpisodeArc/CharacterArc/RelationshipArc/LocalEdge/PayoffCandidate
→ Stage04 CrossEpisodeEdge/FullSeriesArc/Disposition
```

EXT6는 위 파일의 keyset에 임의 필드를 추가하지 않는다.

### 1.2 직접독해 의미 저작

GPT와 Claude는 각자 원문을 직접 읽는다. 한 모델의 분석 결과를 다른 모델이 원문 대신 입력으로 사용해서는 안 된다.

### 1.3 이중 분석 결과의 독립 보존

```text
GPT 결과 ≠ Claude 결과
```

서로 다르다는 이유로 하나를 즉시 오류로 판정하지 않는다. 사실 오류, 계약 오류, 해석 차이를 분리한다.

### 1.4 자동 병합 금지

두 모델 결과를 다수결, 문자열 평균, 단순 union으로 정본화하지 않는다. 합의본은 근거 장면 재대조와 사용자 승인 후 생성한다.

### 1.5 Python/Codex 의미 생성 금지

Python과 Codex는 추출, 직렬화, 계산, 검증, 비교표 생성만 담당한다. 의미 필드의 최초 저작은 GPT 또는 Claude의 직접독해로만 수행한다.

---

## 2. Phase 01 범위

### 포함

- 공통 식별자와 provider-neutral 경로
- AnalysisRunManifest
- EntityBridgeRecord
- CastPresenceRecord
- CharacterLoadRecord
- CastCoverageLedger
- Stage 부착 시점
- Gate A/B
- GPT↔Claude 비교 프로토콜
- negative fixtures와 validator 요구사항

### 제외

- CharacterVoice 전체 저작
- MotifLedger 전체 저작
- AffectRegister 전체 저작
- ThematicStance 전체 저작
- 공식 Stage05 선언
- 300편 전체 적용
- CANONICAL 승격

---

## 3. 분석 포착 시점

### 3.1 SourceLock 이후 EXT preflight

의미 분석 전에 다음을 준비한다.

- `work_slug`
- `character_key` 생성 규칙
- alias normalization policy
- EXT contract version
- provider run id
- EntityBridge staging

### 3.2 Stage01 Q1→Q4 직접독해 직후

각 quarter에서 SceneCard를 먼저 저작한 뒤 같은 원문 범위에서 별도 sidecar로 CastPresence를 포착한다.

```text
원문 독해
→ SceneCard 저작
→ 동일 quarter 짧은 재확인
→ CastPresence
→ QuarterAudit
```

Stage01 SceneCard 9키에는 EXT 필드를 넣지 않는다.

### 3.3 Stage02 이후

SequenceBlueprint가 확정되면 `present_sequence_count` 계산 기반이 생긴다. 다만 CharacterLoad 최종 계산은 EpisodeArc의 act_structure가 필요한 관계로 Stage03 이후 실행한다.

### 3.4 Stage03 이후

```text
CastPresence
+ SequenceBlueprint
+ EpisodeArc act_structure
→ CharacterLoad 결정론 계산
```

회차 잠금 전에 Gate A/B를 통과해야 한다.

### 3.5 Stage04 이후

전 시즌 CharacterLoad 곡선과 SeriesCharacterRoster를 종합할 수 있다. 이는 기능적으로 Stage05 후보이지만 파일럿 동안 `EXT6_FULL_SERIES_SYNTHESIS`라 부른다.

---

## 4. 이중 분석 트랙 구조

GPT와 Claude가 동일 작품을 분석하므로 데이터 파일 자체와 실행 provenance를 분리한다.

### 4.1 논리 경로

```text
analysis_runs/
  <work>/<contract_version>/<provider>/<run_id>/
```

예:

```text
analysis_runs/비밀의숲/ext6-p0-v1/gpt/run_20260714_01/
analysis_runs/비밀의숲/ext6-p0-v1/claude/run_20260714_01/
```

### 4.2 정본 스키마와 provider 정보 분리

CastPresenceRecord와 CharacterLoadRecord에 `model_id`, `provider`, `run_id`를 반복 삽입하지 않는다. exact keyset은 provider-neutral하게 유지한다.

실행 정보는 `AnalysisRunManifest`가 보유한다.

### AnalysisRunManifest — 정확히 14키

```text
run_id
work_id
provider
model_id
contract_version
source_lock_sha256
input_episode_span
quarter_policy
started_at
completed_at
direct_reading_attested
python_semantic_generation
status
by
```

규칙:

- `provider ∈ {GPT, CLAUDE}`
- `direct_reading_attested == true`
- `python_semantic_generation == false`
- 동일 `work_id/provider/run_id` 조합은 유일
- 비교 대상 두 run은 동일 `source_lock_sha256`와 `contract_version`을 가져야 함

---

## 5. 공통 P0 계약

## 5.1 EntityBridgeRecord — 정확히 9키

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

규칙:

- `character_key = <work_slug>:<canonical_name_slug>`
- `entity_id`는 Page10 매핑 전 `null` 허용
- canonical name을 `entity_id`에 넣지 않음
- `mapping_status ∈ {PROVISIONAL, MATCHED, AMBIGUOUS, UNRESOLVED}`
- docs/external에는 Page10 authority 복제본이 아니라 source ref/SHA를 가진 projection만 저장

## 5.2 CastPresenceRecord — 정확히 10키

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

grain:

```text
장면 × 인물 = 1행
```

허용 enum:

```text
presence_mode ∈ {
  ONSCREEN,
  VOICE_ONLY,
  PHONE_OR_REMOTE,
  ARCHIVAL_OR_MEMORY,
  REFERENCED_ONLY
}

focality ∈ {PRIMARY, SECONDARY, PRESENT_ONLY}

speaking_status ∈ {SPEAKING, NON_SPEAKING, NOT_APPLICABLE}
```

불변식:

- `(work_id, episode_no, scene_no, character_key)` 유일
- 장면과 character_key 실재
- `REFERENCED_ONLY`는 등장 분량 집계에서 제외
- `ARCHIVAL_OR_MEMORY`는 별도 집계 가능하나 기본 present count에서 제외
- evidence_ref는 원문 전문이 아닌 SourceLock 장면 hash 또는 scene ref

## 5.3 CastCoverageLedger — 정확히 9키

```text
work_id
episode_no
quarter
scene_range
annotated_scene_nos
empty_cast_scene_nos
unresolved_scene_nos
coverage_status
by
```

목적:

CastPresence 행이 없는 장면이 실제 무인 외경인지 누락인지 구분한다.

통과 조건:

```text
annotated ∪ empty_cast = quarter 모든 scene_no
annotated ∩ empty_cast = ∅
unresolved_scene_nos = []
coverage_status = LOCKED_PASS
```

## 5.4 CharacterLoadRecord — 정확히 17키

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

결정론 계산:

```text
present_scene_count
= ONSCREEN + VOICE_ONLY + PHONE_OR_REMOTE가 존재하는 고유 scene 수

focal_scene_count
= focality가 PRIMARY 또는 SECONDARY인 고유 scene 수

speaking_scene_count
= speaking_status == SPEAKING인 고유 scene 수

scene_share
= present_scene_count / episode_scene_count

focal_share
= focal_scene_count / episode_scene_count
```

`scene_share_band` threshold는 파일럿 전에 고정하고 결과를 본 뒤 바꾸지 않는다.

---

## 6. Provider 독립 분석 규칙

GPT와 Claude는 다음 공통 입력만 공유한다.

- 동일 원본 archive
- 동일 SourceLock
- 동일 Stage01~04 계약
- 동일 EXT6 P0 계약
- 동일 quarter 및 8~10회 블록 정책

공유 금지:

- 상대 모델의 SceneCard
- 상대 모델의 CastPresence
- 상대 모델의 CharacterLoad
- 상대 모델의 분석 메모
- 상대 모델의 중간 품질 점수

각 모델은 먼저 자기 패키지를 봉인한다.

```text
GPT_RUN_LOCKED
CLAUDE_RUN_LOCKED
```

두 상태가 모두 존재한 뒤 비교를 시작한다.

---

## 7. GPT↔Claude 비교 계약

### 7.1 비교 단위

CastPresence는 `(episode_no, scene_no, character_key)` 단위로 비교한다.

CharacterLoad는 `(episode_no, character_key)` 단위로 비교한다.

### 7.2 차이 유형

```text
FACT_CONFLICT
한쪽이 존재하지 않는 인물·장면을 기록

BOUNDARY_CONFLICT
같은 원본이나 SourceLock 장면 경계를 다르게 사용

IDENTITY_CONFLICT
별칭·동명이인 매핑 불일치

PRESENCE_MODE_DIVERGENCE
등장 유형 판정 차이

FOCALITY_DIVERGENCE
초점성 해석 차이

VALID_INTERPRETIVE_DIVERGENCE
양쪽 모두 근거가 있으나 해석이 다름

CONTRACT_ERROR
keyset/enum/FK/COUNT 오류
```

### 7.3 비교 산출물

#### CrossProviderComparisonRecord — 정확히 12키

```text
comparison_id
work_id
record_type
record_key
gpt_value
claude_value
agreement_status
divergence_type
evidence_refs
adjudication_required
adjudication_result
by
```

`agreement_status ∈ {AGREE, PARTIAL, DISAGREE, NOT_COMPARABLE}`

### 7.4 병합 원칙

- FACT_CONFLICT와 CONTRACT_ERROR는 hard adjudication
- FOCALITY_DIVERGENCE는 원문 재독 후 복수 라벨 허용 여부 검토
- VALID_INTERPRETIVE_DIVERGENCE는 반드시 한쪽을 삭제하지 않음
- 합의본은 별도 `consensus/` 경로에 생성
- 원본 GPT/Claude run은 영구 보존

---

## 8. 검증 게이트

## Gate A — Contract

- exact keyset
- enum
- type
- uniqueness
- FK
- source lock SHA
- run manifest compatibility

판정: `ERRORS 0`

## Gate B — Grounding / Recalculation

- 장면 실재
- 인물 실재
- CastCoverage 완전성
- CharacterLoad 재계산 일치
- 원문 전문 미포함
- 반복 placeholder 없음
- Python 의미 생성 없음

판정: `ERRORS 0`

## Gate C — Cross-provider value proof

- GPT/Claude agreement matrix
- 사실 오류율
- 해석 다양성 보존율
- adjudication 비용
- CharacterLoad 사용 전후 구조 진단 성능
- blind critic 효과

Gate C는 파일 손상 PASS/FAIL이 아니라 다음을 결정한다.

```text
PROMOTE_P0
REVISE_CONTRACT
KEEP_ADVISORY
DEFER
REJECT
```

---

## 9. 앵커 파일럿

### 1차 앵커

```text
비밀의숲
```

이유:

- 다인물 수사극
- focality와 주변 인물 배치가 복잡
- 기존 Stage01~04 기반이 충분
- GPT/Claude 차이를 비교하기 적합

### 2차 앵커

```text
시크릿가든
```

수사극에 과적합된 계약인지 로맨스에서 재검증한다.

### 파일럿 분석 범위

처음부터 전 시즌 전체를 요구하지 않는다.

```text
비밀의숲 EP01~02
→ 계약·비용·차이 유형 확인
→ 이상 없으면 정식 8회 블록
```

단, 정식 사용자 제출·품질 판정은 8~10회 블록 규칙을 유지한다. EP01~02는 Phase01 기술 fixture일 뿐 정식 분석 납품이 아니다.

---

## 10. 비교 후 최종 합의 절차

```text
1. GPT 독립안 봉인
2. Claude 독립안 봉인
3. keyset 자동 비교
4. stage timing 비교
5. validator/gate 비교
6. 이견 목록 작성
7. 각 모델이 상대안 비평
8. 사용자 판단이 필요한 항목 분리
9. 합의 계약 v1 작성
10. 사용자 승인 후 Codex 구현
```

최종 합의 문서에는 각 조항의 출처를 남긴다.

```text
GPT_ONLY
CLAUDE_ONLY
BOTH_AGREED
USER_DECIDED
```

---

## 11. Phase 01 완료 기준

다음이 모두 있어야 Phase 01 완료다.

- GPT 독립 설계안
- Claude 독립 설계안
- 비교 매트릭스
- 합의·미합의 원장
- 확정 schema registry
- positive fixture
- negative fixtures
- Gate A validator specification
- Gate B recalculation specification
- 사용자 승인 기록

아직 완료가 아닌 것:

```text
새 Stage05 공식화
전면 코퍼스 적용
CANONICAL 승격
```

---

## 12. GPT 자기비판

1. CastPresence 자체도 focality에서 해석 차이가 크므로 등장 사실과 초점 판단을 동일 레코드에 두는 것이 장기적으로 분리 필요할 수 있다.
2. `character_key` slug 규칙은 한국어 띄어쓰기·동명이인에서 충돌할 수 있어 EntityBridge가 빠르게 필요하다.
3. 두 모델을 완전 블라인드하게 운영하기 어렵기 때문에 최소한 상대 산출물 미열람 선언과 run lock을 기록해야 한다.
4. 비교 비용이 커질 수 있으므로 모든 의미 필드가 아니라 P0부터 이중 분석해야 한다.
5. 합의율이 높다고 품질이 높은 것은 아니므로 원본 근거 정확성과 blind value proof를 별도로 봐야 한다.

---

## 13. 최종 제안

```text
GPT와 Claude가 모두 드라마를 분석하는 전략은 타당하다.
다만 한쪽을 정답 생성기, 다른 쪽을 검사기로 고정하지 않는다.
두 모델은 독립 저작자이며, 공통 계약과 SourceLock 아래 별도 run을 만든다.
비교는 오류 탐지와 해석 다양성 보존을 동시에 목표로 한다.
```

상태:

```text
GPT_INDEPENDENT_DRAFT_LOCKED
READY_FOR_CLAUDE_INDEPENDENT_DRAFT
NO_IMPLEMENTATION_BEFORE_COMPARISON
```