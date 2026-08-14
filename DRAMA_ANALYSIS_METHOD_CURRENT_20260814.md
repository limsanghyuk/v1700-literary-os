# 한국 드라마 분석 현행 실행 방법 — 2026-08-14

## 1. 최상위 원칙
원본 드라마 대본과 SourceLock이 최상위 의미 권위다. 모델이 원문을 회차 순서대로 직접 독해하고 이해한 뒤 의미를 저작한다. Python은 추출·정규화·해시·직렬화·검증·비교·패키징에만 사용하며 장면/인물/관계/인과 의미를 생성하지 않는다.

## 2. 작업 단위
- 의미 저작 단위: 한 회차 전체.
- Q1→Q2→Q3→Q4: 긴 회차를 순서대로 읽기 위한 attention/checkpoint 단위이며 극적 4막을 뜻하지 않는다.
- Block: 실행 한도를 관리하기 위해 전 회차를 최대 8회차씩 묶는 운영 경계. Block은 의미 스키마가 아니다.
- 순서를 건너뛰지 않는다. EP01 완료 후 EP02, … 순으로 진행한다.

## 3. Stage01~04
### Stage01 SceneCard
9키: `work_id, scene_no, heading, title, intent_gist, core, core2, skin, by`. 장면별 사건·행동·정서·의도 변화를 원문에서 고유하게 저작한다.

### Stage02 SequenceBlueprint + EpisodeArc
SequenceBlueprint 18키, EpisodeArc 13키. SceneCard를 기계적으로 합치는 것이 아니라 장면군의 목표, 장애, 가치 이동, 전환, POV, 공간군, runtime share를 구조화한다.

### Stage03
CharacterArc 8키, RelationshipArc 9키, LocalEdge 12키, PayoffCandidate 7키. LocalEdge는 반드시 동일 회차 causal / `gap_episodes=0`이다. 회차를 넘는 연결을 LocalEdge에 넣지 않는다.

### Stage04
전 시즌 Stage01~03이 잠긴 뒤 FullSeriesArc 17키와 CrossEpisodeEdge를 fan-in한다. 회차 간 callback/plant-payoff/subplot/cross-episode causal은 Stage04에 둔다.

## 4. CANONICAL THICK
SequenceBlueprint의 경계는 사용하되 의미는 원문을 다시 읽어 독립 저작한다. 핵심은 `cast(character, desire_or_function, participation)`, 구체적 `event`, `info_shift`, `plant_payoff`, 모든 member scene을 덮는 `scene_notes`, `evidence_refs`와 `source_hashes`다. Stage02 event의 그대로 복사, Stage01/02 문장의 cast-function 재사용, generic cast 문구, strict 신규작의 동일 function 중복은 blocking error다. `1 Sequence = 1 atomic THICK transaction`이다.

## 5. PlannerInput R5 / Runtime R8
권위 순서: `Source/SourceLock → Stage01 → Stage02 → Stage03 → Stage04 → CANONICAL THICK → R5 → R8`.
- R5는 Episode N을 위한 planning boundary이며 N-1까지 확정된 상태만 사용한다. 미래/대상 회차 사실 역류를 금지한다.
- R8은 현재 THICK + 같은 회차 R5를 장면 단위로 펼치는 deterministic projection이다. 새 의미를 저작하지 않는다. THICK가 바뀌면 R8은 stale이므로 다시 만든다.

## 6. EXT6
EXT6는 Stage01~04/THICK를 대체하지 않는 `SELECTIVE_APPEND_ONLY` evidence sidecar다. 현재 exact registry의 7 record는 EntityRegistry, EntityBridge, CastPresence, CharacterLoad, CastCoverageLedger, SourceHeadingRegistry, SourceSceneAlignment이다. Base Stage01~04는 byte-immutable해야 한다. Entity mapping, presence/focality, source-scene alignment는 원문 근거와 독립 감사를 요구한다. CharacterLoad처럼 계약이 정한 결정론적 파생만 자동화할 수 있다. EXT6 PASS는 CharacterArc/RelationshipArc의 자동 승격을 뜻하지 않는다.

## 7. 검증과 승격
작품 저작 완료 후 `exact schema/member-scene/source range/provenance hash → semantic independence V3 strict → whole-work quality → R5/R8 validator`를 통과해야 한다. 기존 정본 작품은 신규작 승격 직전 byte-immutability를 확인한다. 물리 payload 검증 후에만 authority pointer/manifest를 승격한다.

## 8. 중단/재개 및 패키징
채팅의 진행 보고보다 디스크의 durable checkpoint가 우선이다. THICK atomic state는 `PENDING→SOURCE_READ→SEMANTIC_AUTHORED→FILE_SAVED→AUDIT_PASS→CHECKPOINT_LOCKED`이며 CHECKPOINT_LOCKED만 완료다. 장시간 작업은 semantic authoring, assembly, strong validation, R5/R8, authority promotion, checksum, ZIP, fresh extraction을 분리한다. THICK 신규 저작 응답은 response lease를 사용해 최대 3개 신규 Sequence만 허용하며, 응답 종료 시 checkpoint fsync·writer lock 해제·write surface 동결 후 종료한다. ZIP을 만든 뒤 별도 디렉터리에 다시 풀어 공식 검증과 체크섬을 재실행한다.

## 9. 실험 계층의 경계
Blind-forward/ablation/holdout/EXT6 Phase02 같은 실험은 기능 효용을 검증하기 위한 evidence다. 실험 PASS가 곧 canonical 의미 승격을 뜻하지 않는다. 측정값의 derivation, leakage, holdout 독립성, schema consistency가 별도로 검증되어야 한다.

## 10. 현재 정본 상태
Stage01~04: 98작 / 1,814회 / 114,371 SceneCards (V10.1, unchanged). EXT6 integrated cohort: 35작, append-only. CANONICAL THICK: 25작 / 3,735 Sequence. PlannerInput R5: 25작 / 450회. Runtime R8: 25작 / 450회 / 28,341 scene records. 25번째 작품은 구해줘이며 EP01~16 원문 직접 재독해 기반 THICK 162 Sequence가 strict/exact/R5-R8 gate를 통과했다.
