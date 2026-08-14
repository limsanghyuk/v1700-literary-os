# 한국 드라마 분석 현행 실행 방법 — 2026-08-15 V9

## 최상위 원칙
원본 드라마 대본과 SourceLock이 최상위 의미 권위다. 모델이 원문을 회차 순서대로 직접 독해하고 이해한 뒤 의미를 저작한다. Python은 추출·정규화·해시·직렬화·검증·비교·조립·패키징에만 사용하며 장면/인물/관계/인과 의미를 생성하지 않는다.

## Stage01~04
- Stage01 SceneCard: 9키 `work_id, scene_no, heading, title, intent_gist, core, core2, skin, by`.
- Stage02: SequenceBlueprint 18키, EpisodeArc 13키.
- Stage03: CharacterArc 8키, RelationshipArc 9키, LocalEdge 12키, PayoffCandidate 7키. LocalEdge는 동일 회차 causal이며 `gap_episodes=0`.
- Stage04: 전 시즌 Stage01~03 잠금 후 FullSeriesArc 17키와 CrossEpisodeEdge. 회차 간 callback/plant-payoff/subplot/cross-episode causal은 Stage04에 둔다.

Q1→Q2→Q3→Q4는 attention/checkpoint 단위이며 극적 4막이 아니다. 한 회차 전체가 Stage01~04 의미 저작 단위다. Block은 최대 8개의 연속 회차를 묶는 실행 경계다.

## CANONICAL THICK
SequenceBlueprint는 경계만 사용하고 원문을 다시 읽어 독립 저작한다. Stage02 event 그대로 복사, Stage01/02 cast-function 재사용, generic cast, 동일 시퀀스에서 인물명만 바꾼 동일 기능문, unresolved evidence는 blocking error다.

`1 Sequence = 1 atomic transaction`이며 `SOURCE_READ → SEMANTIC_AUTHORED → FILE_SAVED → AUDIT_PASS → CHECKPOINT_LOCKED` 순서로 잠근다.

## Thread Continuity R1 — 신규 작품 필수
- 실제 새 극적 실이 시작되는 `PLANT`/`HOOK`에서만 새 semantic `thread_id`를 발급한다.
- 동일 실의 `CONTINUE / ESCALATION / CALLBACK / REACTIVATION / REVERSAL / PAYOFF`는 기존 ID를 재사용한다.
- episode/sequence 번호 기반 serial ID를 장기 semantic identity로 사용하지 않는다.
- 신규 ID 발급 전 원문, 기존 thread, `existing_refs`, source-grounded Stage03/04 evidence를 확인한다.
- 관련 주제라는 이유만으로 다른 실을 병합하지 않는다.
- multi-episode 40%, R5 coupling 30%는 provisional diagnostic이며 hard gate가 아니다.
- 점수를 위한 오결속을 금지한다.
- `resolves_thread`는 현재 exact schema가 아니며 experimental이다.

## PlannerInput R5 / Runtime R8
권위 순서: `Source/SourceLock → Stage01 → Stage02 → Stage03 → Stage04 → CANONICAL THICK → R5 → R8`.
R5 Episode N은 N−1까지 확정된 상태만 사용하며 target/future leakage를 금지한다. R8은 current THICK + same-episode R5의 deterministic projection이다. THICK가 바뀌면 R5/R8을 재생성한다.

## 품질 균질성
구조 PASS와 의미 품질 PASS를 분리한다. 전작 동일 평가표에서 event/cast/info/plant-payoff 밀도, Stage01 skin 구체성·반복, character-prefix-stripped cast duplicate, Stage02 추상 템플릿, 직접-source 표본, Semantic V3, exact/provenance, R5/R8를 검사한다. 지표를 맞추기 위한 의미 자동 생성이나 잘못된 인물·thread 귀속은 금지한다.

## 중단/재개 — Block-Atomic V2
- 최대 8개의 연속 회차를 한 Block으로 실행한다.
- **응답당 고정 Sequence 수 제한은 없다. 과거 3 Sequence hard cap은 폐기됐다.**
- 각 Sequence는 `CHECKPOINT_LOCKED` 후 다음으로 이동한다.
- 회차 완료 시 episode assembly/checkpoint, Block 완료 시 strong gate를 남긴다.
- background/late writer를 금지하고 overrun은 quarantine한다.

Durable phases: `THICK_BLOCK_AUTHORING → BLOCK_GATE → WHOLE_WORK_GATE → R5_BUILD → R8_BUILD → DB_INTEGRATION → CHECKSUM_BUILD → ZIP_BUILD → FRESH_EXTRACTION → HUB_PROMOTION`.

## 현재 CANONICAL — V9
- Stage01~04 schema authority: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`.
- Stage01/02 일부는 26작 품질 균질화를 위해 source-grounded 선택 보강되었다. 따라서 V8 대비 blanket byte-immutability를 주장하지 않는다.
- Stage03/04, Source/SourceLock, EXT6는 V9 품질/thread 작업에서 변경하지 않았다.
- CANONICAL THICK: `DB98_THICK_26WORK_QUALITY_THREAD_R1_CANONICAL_AUTHORITY_20260815_V1`, 26작 / 3,883 records.
- Quality: Q25 4/4 26/26, Stage01 skin 반복과 same-sequence cast duplicate 강검사 PASS.
- Thread Continuity R1: 26작 review 완료, source-grounded 적용. 진단선은 hard gate가 아니다.
- PlannerInput R5: 470회.
- Runtime R8: 470회 / 29,628 scenes.
- Full DB: `DB98_98WORK_STAGE04_26THICK_QUALITY_THREAD_R1_CLEAN_V9_FINAL_20260815.zip`.
- SHA256: `0c205207bad085f31b002fe6bb06b65123baec578649cc0c337ec6cfb268014f`.
- Final fresh extraction: PASS.

## 새 세션 최신성
정적 번들은 snapshot이다. 새 세션은 live Hub `main`의 integrated pointer, overlay, active-work claims, 이 방법론, Thread Continuity R1을 먼저 다시 읽는다. live Hub가 더 최신이면 live Hub가 우선이며 과거 snapshot으로 되돌리지 않는다.
