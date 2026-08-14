# 한국 드라마 분석 현행 실행 방법 — 2026-08-15 동기화

## 1. 최상위 원칙
원본 드라마 대본과 SourceLock이 최상위 의미 권위다. 모델이 원문을 회차 순서대로 직접 독해하고 이해한 뒤 의미를 저작한다. Python은 추출·정규화·해시·직렬화·검증·비교·조립·패키징에만 사용하며 장면/인물/관계/인과 의미를 생성하지 않는다.

## 2. 작업 단위
- Stage01~04 의미 저작 단위: 한 회차 전체.
- Q1→Q2→Q3→Q4: 긴 회차를 순서대로 읽기 위한 attention/checkpoint 단위이며 극적 4막을 뜻하지 않는다.
- Block: 최대 8개의 연속 회차를 묶는 실행 경계이며 의미 스키마가 아니다.
- 순서를 건너뛰지 않는다.

## 3. Stage01~04
### Stage01 SceneCard
9키: `work_id, scene_no, heading, title, intent_gist, core, core2, skin, by`. 장면별 사건·행동·정서·의도 변화를 원문에서 고유하게 저작한다. `skin`은 장소·시간·표면행동·소품 등 장면 표면의 구체성을 담고 작품 전체에 동일 장르 라벨을 반복하지 않는다.

### Stage02 SequenceBlueprint + EpisodeArc
SequenceBlueprint 18키, EpisodeArc 13키. SceneCard를 기계적으로 합치는 것이 아니라 장면군의 목표, 장애, 가치 이동, 전환, POV, 공간군, runtime share를 구조화한다. 추상 템플릿만 반복하지 않는다.

### Stage03
CharacterArc 8키, RelationshipArc 9키, LocalEdge 12키, PayoffCandidate 7키. LocalEdge는 반드시 동일 회차 causal / `gap_episodes=0`이다. 회차를 넘는 연결을 LocalEdge에 넣지 않는다.

### Stage04
전 시즌 Stage01~03이 잠긴 뒤 FullSeriesArc 17키와 CrossEpisodeEdge를 fan-in한다. 회차 간 callback/plant-payoff/subplot/cross-episode causal은 Stage04에 둔다.

## 4. CANONICAL THICK
SequenceBlueprint의 경계는 사용하되 의미는 원문을 다시 읽어 독립 저작한다. 핵심은 `cast(character, desire_or_function, participation)`, 구체적 `event`, `info_shift`, `plant_payoff`, 모든 member scene을 덮는 `scene_notes`, `evidence_refs`, `source_hashes`다.

Stage02 event 그대로 복사, Stage01/02 cast-function 재사용, generic cast 문구, 동일 시퀀스에서 인물명만 바꾼 동일 기능문, unresolved evidence는 blocking error다.

`1 Sequence = 1 atomic THICK transaction`:

`SOURCE_READ -> SEMANTIC_AUTHORED -> FILE_SAVED -> AUDIT_PASS -> CHECKPOINT_LOCKED`

`CHECKPOINT_LOCKED`만 완료로 인정한다.

## 5. Thread Continuity R1 — 신규 작품 필수

`DRAMA_ANALYSIS_THREAD_CONTINUITY_POLICY_R1_20260815.md`를 신규 THICK 저작의 필수 규칙으로 적용한다.

- 새로운 극적 실이 실제로 시작되는 `PLANT` 또는 `HOOK`에서만 새 semantic `thread_id`를 발급한다.
- 같은 실의 `CONTINUE / ESCALATION / CALLBACK / REACTIVATION / REVERSAL / PAYOFF`에는 기존 ID를 재사용한다.
- episode/sequence 번호 기반 임시 ID를 장기 semantic identity로 사용하지 않는다.
- 신규 ID 발급 전 원문, 기존 thread, `existing_refs`, Stage03/04의 source-grounded evidence를 확인한다.
- 관련 주제라는 이유만으로 서로 다른 실을 병합하지 않는다.
- 현재의 multi-episode 40%, R5 coupling 30%는 잠정 진단선이지 canonical hard gate가 아니다. 점수를 맞추기 위한 가짜 병합을 금지한다.
- `resolves_thread`는 현 exact schema가 아니며 별도 실험·승격 전에는 추가하지 않는다.

THICK `thread_id`가 바뀌면 해당 R5와 R8은 stale이다.

## 6. PlannerInput R5 / Runtime R8
권위 순서: `Source/SourceLock → Stage01 → Stage02 → Stage03 → Stage04 → CANONICAL THICK → R5 → R8`.

- R5는 Episode N을 위한 planning boundary이며 N-1까지 확정된 상태만 사용한다. 미래/대상 회차 사실 역류를 금지한다. thread continuity 때문에 target episode를 미리 보고 carry할 thread를 선택해서도 안 된다.
- R8은 현재 THICK + 같은 회차 R5를 장면 단위로 펼치는 deterministic projection이다. 새 의미를 저작하지 않는다. THICK가 바뀌면 R8은 다시 만든다.

## 7. EXT6
EXT6는 Stage01~04/THICK를 대체하지 않는 `SELECTIVE_APPEND_ONLY` evidence sidecar다. 현재 exact registry의 7 record는 EntityRegistry, EntityBridge, CastPresence, CharacterLoad, CastCoverageLedger, SourceHeadingRegistry, SourceSceneAlignment이다. Base Stage01~04는 byte-immutable해야 한다.

## 8. 품질 균질성 검사
구조 PASS와 의미 품질 균질성 PASS를 구분한다. 작품별로 동일 평가표를 사용해 다음을 재검사한다.

- event/cast/info/plant-payoff 밀도 하한;
- Stage01 skin 구체성·exact 반복;
- character prefix를 제거한 동일 시퀀스 cast 기능 중복;
- Stage02 추상 템플릿 반복;
- 직접-source 표본;
- semantic independence V3 strict;
- exact/provenance/source;
- R5/R8 parity.

지표를 맞추기 위해 의미를 자동 생성하거나 다른 인물/스레드의 문장을 잘못 귀속하는 것은 금지한다.

## 9. 중단/재개 — Block-Atomic V2
채팅 진행보다 durable checkpoint가 우선이다.

- THICK 실행 Block은 최대 8개의 연속 회차다.
- **응답당 고정 시퀀스 수 제한은 없다. 과거 3 Sequence hard cap은 폐기됐다.**
- 각 Sequence는 원자적으로 `CHECKPOINT_LOCKED`된 뒤 다음으로 넘어간다.
- 한 회차가 닫히면 atomic records에서 episode JSONL을 재조립하고 episode checkpoint를 남긴다.
- Block이 닫히면 독립 strong gate를 실행한다.
- background/late writer는 금지하며 overrun 파일은 quarantine한다.
- 중단 시 contiguous valid prefix를 재계산해 `next_seq_id`에서 이어간다.

## 10. 장기 단계 분리
서로 다른 durable phase:

`THICK_BLOCK_AUTHORING -> BLOCK_GATE -> WHOLE_WORK_GATE -> R5_BUILD -> R8_BUILD -> DB_INTEGRATION -> CHECKSUM_BUILD -> ZIP_BUILD -> FRESH_EXTRACTION -> HUB_PROMOTION`

각 단계는 실제 PASS evidence가 있어야 다음 단계로 전환한다. 전체를 하나의 mega-script나 background process로 묶지 않는다.

## 11. 검증·승격·패키징
작품 완료 후 `exact schema/member-scene/source range/provenance hash -> semantic independence V3 strict -> whole-work quality -> thread-continuity diagnostic -> R5/R8 validator`를 통과시킨다. 기존 정본 작품은 신규작 승격 직전 byte-immutability를 확인한다.

최종 ZIP을 별도 디렉터리에 fresh extract하여 검증과 checksum을 재실행한다. fresh extraction PASS 전에는 canonical promotion을 선언하지 않으며 Hub 승격은 마지막이다.

## 12. 실험 계층 경계
Blind-forward/ablation/holdout/EXT6 Phase02, `resolves_thread` 같은 신규 필드는 실험 evidence다. 실험 PASS가 곧 canonical schema 승격을 뜻하지 않는다. 앵커 작품과 독립 검증을 거쳐 deliberate schema version promotion이 있어야 한다.

## 13. 현재 CANONICAL 정본 상태
현재 live Hub가 가리키는 정본은 여전히 2026-08-14 26작이다.

- Stage01~04: 98작 / 1,814회 / 114,371 SceneCards (`DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`, unchanged).
- EXT6: 35작, append-only.
- CANONICAL THICK: `DB98_THICK_26WORK_CANONICAL_AUTHORITY_20260814_V1_GUKHEE_INTEGRATED`, 26작 / 3,883 Sequence.
- PlannerInput R5: 26작 / 470회.
- Runtime R8: 26작 / 470회 / 29,628 scene records.
- 26번째 작품 `국희`: 20회 / 148 THICK / 1,287 Runtime scenes.
- 최종 DB: `DB98_98WORK_STAGE04_26THICK_CLEAN_V8_GUKHEE_INTEGRATED_FINAL_20260814.zip`.
- SHA256: `39fea427974c212a0e42cf7cc1b63f1ddff875da050443091c77e0522cb4efe7`.

별도 `quality26_repair_stage`는 품질 균질화 candidate이며 아직 canonical authority가 아니다. `돌아온일지매` thread continuity 작업도 anchor pilot이며 canonical에 미승격이다.

## 14. 새 세션 최신성 규칙
정적 번들의 숫자와 포인터는 생성 시점 snapshot이다. 새 세션은 반드시 live Hub `main`의 `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`, live overlay, `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json`, 이 방법론, Thread Continuity R1 정책을 다시 읽는다.

번들과 live Hub가 다르면 **live Hub가 우선**이며, 다른 GPT 세션이 더 최신 authority를 승격한 경우 절대 과거 snapshot으로 되돌리지 않는다.
