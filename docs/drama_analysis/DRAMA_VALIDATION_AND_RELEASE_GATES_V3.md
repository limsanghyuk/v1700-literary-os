# 드라마 검증 및 릴리스 게이트 v3

- Document ID: `DRAMA-VALIDATION-RELEASE-GATES-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Principle: fail closed. 보고서보다 실제 레코드 검증 결과가 우선한다.

## 1. 게이트 체계

```text
Gate 0 — Source Integrity
Gate 1 — Quarter Direct-Reading Integrity
Gate 2 — Stage01/02 Structural Integrity
Gate 3 — Stage01/03 Semantic Grounding
Gate 4 — EXT6 Contract and Recalculation
Gate 5 — Stage04 Full-Series Fan-in
Gate 6 — Package, Lineage, and Release
```

한 단계라도 실패하면 다음 단계 입력으로 승격하지 않는다.

## 2. Gate 0 — Source Integrity

필수 검사:

- 원본 archive/file SHA256
- 회차 파일 존재와 인코딩
- 물리 헤딩 수와 이상 마커
- canonical ordinal `1..N`
- 원본의 중복 파싱·누락·병합 여부
- SourceSceneAlignment coverage
- 원본 장문이 배포 패키지에 포함되지 않음

판정:

```text
PASS_SOURCE_LOCKED
FAIL_SOURCE_MISMATCH
FAIL_SCENE_ALIGNMENT
```

## 3. Gate 1 — Quarter Direct-Reading Integrity

QuarterAudit 필수 조건:

```text
direct_reading_completed == true
python_semantic_generation == false
placeholder_count == 0
status == LOCKED_PASS
```

반게이밍 검사:

- keyword list artifact
- 가시적 `[EPxx-Syy]` 참조 템플릿
- 동일 시작구·동일 골격 반복
- SceneCard 필드 간 문장 복사
- 의미 없는 짧은 문장·미치환 변수
- 원문 대사 장문 복사

Q1 실패 시 Q2 진행 금지. 각 Quarter는 다음 Quarter 시작 전 저장·검증한다.

## 4. Gate 2 — Stage01/02 Structural Integrity

### Stage01

- exact 9 keys
- `scene_no=1..N`
- CORE_ENUM 16
- `core2` null 또는 CORE_ENUM
- heading provenance 존재
- EpisodeMeta.scene_count 및 core_dist 재계산 일치

### Stage02

- exact 18 keys
- seq_id/seq_index 연속
- I-COVER, I-PARTITION, I-COUNT
- member scenes 오름차순·연속
- scene_span·scene_budget 일치
- `value_shift` exact `from/to`
- turn_type registry와 turn_class 일치
- core_mix가 member SceneCard의 실제 core/core2의 부분집합
- runtime_share 합계 1.0, 허용오차 1e-6 권장
- sequence density 하한 0.11

## 5. Gate 3 — Stage01/03 Semantic Grounding

### EpisodeArc

- exact 13 keys
- counts 일치
- act_structure가 모든 sequence를 gap/overlap 없이 덮음
- turning_point가 실제 seq_index를 참조

### CharacterArc

- exact 8 keys
- character가 trigger scene에 실제 등장
- state_delta가 회차별 변화량
- 동일 evidence 대량 복사 금지

### RelationshipArc

- exact 9 keys
- trigger scene에 양쪽 인물 등장·통화·교신
- unordered pair 중복 금지

### LocalEdge

```text
edge_type == causal
src_episode_no == tgt_episode_no
gap_episodes == 0
label == target SceneCard.core
```

- source/target 장면 실재
- note는 구체 인과
- 단순 인접성 금지

### PayoffCandidate

- exact 7 keys
- ID 전역 유일
- scene reference 실재
- enum 유효
- 미확인 장거리 연결은 후보 상태 유지

## 6. Gate 4 — EXT6

### Gate A: 계약·결정론

- Bridge 9키, Cast 10키, Load 17키 exact keyset
- enum/type/null 규칙
- grain uniqueness
- Cast.scene FK, Cast.character_key FK
- Load.character_key FK
- CharacterLoad 전 필드 재계산 일치
- scene_share_band 반개구간 판정

### Gate B: 근거·커버리지

- evidence_ref가 해당 장면을 가리킴
- placeholder·상수 evidence 금지
- CastCoverageLedger 세 집합 상호배타
- 합집합이 전체 장면과 일치
- unresolved는 0이 원칙; 존재 시 명시적 HOLD
- 장소·조직의 인물 오등록을 Gate B7에서 탐지
- SourceSceneAlignment가 전체 SceneCard를 덮음

## 7. Gate 5 — Stage04

- 모든 PayoffCandidate에 disposition 존재
- CrossEpisodeEdge exact 12 keys
- `tgt_episode_no > src_episode_no`
- `gap_episodes` 산술 일치
- 허용 유형: callback, plant_payoff, subplot_counterpoint
- source/target 장면 실재
- target label이 target SceneCard.core와 일치
- 자동 회차 브리지 0
- FullSeriesArc counts 재계산 일치
- season_structure의 episode span에 gap/역전 없음

## 8. Gate 6 — Package and Release

필수:

- PACKAGE_MANIFEST
- SHA256SUMS 전수 일치
- ZIP integrity PASS
- source_lock 포함
- quarter_audits 포함
- validation report 포함
- supersession/quarantine ledger 포함
- raw source 및 의미 생성 Python 미포함
- 사람용 report와 machine validation 판정 일치

## 9. 내용 깊이·반복 기준

권장:

```text
content_depth_avg >= 3.0 / 4
content_depth_min >= 2.5 또는 재저작
exact repeated semantic sentences = 0 above justified threshold
masked skeleton repetition < 15%
```

반복 탐지는 CORE_ENUM·인물명·장소명을 마스킹한 뒤에도 수행한다. 문장 단어만 바꾼 템플릿을 통과시키지 않는다.

## 10. 교정 분류

### 결정론적 계약 교정

의미를 바꾸지 않고 허용:

- Edge label을 target core로 정렬
- runtime_share 반올림·합계 교정
- coverage ledger 중복 제거
- ID/FK 표기 정규화
- core_mix에서 실제 장면에 없는 값 제거

모든 변경 전 SHA와 변경 이벤트를 correction ledger에 기록한다.

### 의미 재저작 필요

- 원문과 다른 사건·인물
- 부정확한 목표·장애·전환
- 잘못된 인물/관계 변화
- 허위 인과·복선·회수
- 템플릿·키워드 기반 의미 필드

의미 결함은 자동 교정하지 않고 원문 재독해 후 새 lineage로 작성한다.

## 11. 상태 enum

```text
DRAFT
QUARANTINE
PASS_CANDIDATE
PASS_CANDIDATE_AFTER_DETERMINISTIC_REPAIR
CANONICAL
SUPERSEDED
```

`CANONICAL`은 모든 게이트 통과와 사용자 승인 후에만 선언한다.
