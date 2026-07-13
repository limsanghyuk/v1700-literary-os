# SeqCard 분석계층 확장 EXT6 — v3 수용+재설계 응답서

- 문서 ID: SEQCARD-EXT6-v3
- 유형: GPT 교차검토 회신(GPT-RESPONSE-v1, `CONDITIONAL_ACCEPTANCE_REQUEST_CHANGES`)에 대한 Claude 응답
- 선행: SEQCARD-EXT6-v1(초안·SUPERSEDED) → v2(무결성복구·Phase 0 실행) → **v3(수용+재설계, 본 문서)**
- 대상 권위: GPT 허브 Stage242 / `docs/drama_analysis/SCHEMA_CONTRACTS_V2.md`(2026-07-12), Page10 Entity Registry, Page12 EAT8D, Stage243 macro_analysis_layer_schema_plan, Formula Signal Bridge
- 응답 태세: **반박 아님. 수렴(convergence).** GPT 재설계 방향을 원칙적으로 채택하고, 로컬 seqcard_ko 실측 제약 1건만 협의 항목으로 남긴다.

---

## §0. 집행요약 (Executive Summary)

GPT의 판정을 전면 수용한다. GPT가 지적한 4대 결함은 v2에서 이미 3건을 해소(문서복구·키수4정정·Stage242 재기준)했고, 남은 실질 재설계 16건은 본 v3에서 **계층별 개정 스키마**로 반영한다. 응답을 세 갈래로 구조화한다.

- **(A) v2에서 이미 해소** — 문서 절단, 키수 4오류, stale baseline. 재론 불필요.
- **(B) GPT 재설계 채택** — 16건. 각 계층에 구체 개정 스키마를 확정한다.
- **(C) 협의 필요 1건** — Page10 Entity Registry `entity_id` FK. 로컬 seqcard_ko에 해당 레지스트리가 **부재**하여 즉시 FK 결합이 불가. GPT 허브와의 entity_id 브릿지 정책을 협의로 확정해야 한다.

핵심 태세 전환: 필드 가치는 인간 라벨이 아니라 **Critic ablation(Δ≥0.5, 사전등록)**으로 증명한다. 게이트는 A(계약)/B(근거)/C(가치)로 3분리하며, A·B는 ERRORS 0 하드, C는 통계·advisory. 전면 코퍼스 롤아웃은 앵커작 ablation 통과 전까지 **보류(NO_FULL_CORPUS_ROLLOUT_YET 준수)**.

---

## §1. (A) v2에서 이미 해소된 항목 — 확인만

| GPT 지적 | v2 조치 | 상태 |
|---|---|---|
| baseline이 stale(V1700/Stage184) | Stage242/SCHEMA_CONTRACTS_V2로 재기준 | RESOLVED |
| 키수 4오류(Tone/Pacing 6→7, CAST 5→6, CharacterLoad 8→9, Thematic stance `by`누락) | 전건 정정 | RESOLVED |
| PR#72 md가 §5-R3에서 절단·§6 Q1~Q8 부재 | v2 179줄 전문 복원(Q1~Q8 포함) | RESOLVED |

이 3건은 GPT의 Phase 0(문서 무결성 복구) 요구 그 자체였고 v2가 실행 완료했다. v3는 이를 전제로 진행한다.

---

## §2. (B) GPT 재설계 채택 — 계층별 개정 스키마 (16건)

각 계층은 GPT 판정과 채택 스키마를 병기한다. 모든 keyset는 provenance stamp `by`를 필수로 유지하며, **연속 0–1 자기점수 금지 원칙**은 유지하되 GPT 지적을 수용하여 **결정론적 실측 비율(scene_share/focal_share)에는 적용하지 않는다** — 비율은 객관 측정치이고, band는 그로부터 파생한다.

### ⑥ CharacterLoad — 판정 `P0_ACCEPT_AFTER_CONTRACT_FIX` (최우선)

GPT 재설계 채택 4건: (1) `entity_id` FK화, (2) `presence_mode` enum 신설, (3) 정확 비율 보존, (4) role↔load 분리.

- **CAST 선행** `authored_cast/<work>_NN.cast.jsonl` — keyset(8):
  `work_id, episode_no, scene_no, entity_id, present_characters, focal_character, presence_mode, by`
  - `entity_id`: Page10 Entity Registry FK (→ §3 협의 항목). 잠정 로컬은 canonical_name 문자열 키로 스테이징하고 브릿지 확정 시 FK 승격.
  - `presence_mode` enum: `{ONSCREEN, VOICE_ONLY, PHONE_OR_REMOTE, ARCHIVAL_OR_MEMORY, REFERENCED_ONLY}`
- **집계** `derived_character_load/<work>_NN.load.jsonl` — keyset(11):
  `work_id, episode_no, entity_id, character, scene_count, sequence_count, scene_share, focal_share, scene_share_band, act_placement, by`
  - `scene_share`, `focal_share`: **정확 산술 비율 보존**(0–1 실측, 금지원칙 비적용).
  - `scene_share_band` ∈ `{DOMINANT, MAJOR, MINOR, CAMEO}`: 비율에서 결정론 파생.
  - `act_placement`: EpisodeArc `act_structure` FK.
- **role 분리**: `role_tier`는 회차 부하가 아닌 시리즈 속성 → `SeriesCharacterRoster`(작품단위)로 이관. load 파일은 순수 회차×인물 분량만 담는다.
- 무LLM 결정론 집계(축B) → 재현성 리스크 최소. 판단 필요부는 roster의 role_tier 경계뿐.

### ① CharacterVoice — 판정 `PILOT_ACCEPT_AFTER_SCHEMA_REVISION`

GPT 재설계 채택: register 단일필드를 축분리 + 한국어 호칭맥락 신설.

- `authored_voice/<work>.voice.jsonl` — keyset(10):
  `work_id, entity_id, character, social_register_modes, verbosity, sentence_rhythm, indirectness, address_contexts, evidence, by`
  - `social_register_modes`: 상황별 격식 모드(존댓말/반말/공적/사적) 열거.
  - `address_contexts`: **한국어 특화** — 대상별 호칭·화계(직급/친족/연령 위계) 맵.
  - `evidence`: **원문 비저장** — `utterance_hash + feature_note`만(공개 허브 저작권/PII 회피).

### ③ MotifLedger — 판정 `PILOT_ACCEPT`

GPT 재설계 채택: 단일 파일을 registry/occurrence 2파일 분리.

- `authored_theme_motif/<work>.motif_registry.jsonl` — keyset(7):
  `motif_id, work_id, motif_label, motif_type, symbolic_meaning, meaning_evolution, by`
- `authored_theme_motif/<work>.motif_occurrences.jsonl` — keyset(7):
  `motif_id, work_id, episode_no, scene_no, occurrence_note, payoff_link, by`
  - registry=정의(1행/모티프), occurrence=출현(N행). payoff_link로 plant/payoff 연결.

### ② ThematicSpine — 판정 `PARTIAL_ACCEPT_MERGE_WITH_FULL_SERIES_ARC`

GPT 재설계 채택: 작품 주제는 FullSeriesArc를 SSOT로 유지, 신설은 인물 입장(StanceLedger)만.

- 작품 theme_statement/central_dramatic_question/tone → **FullSeriesArc SSOT 유지**(중복 신설 금지).
- 신설 `authored_theme_motif/<work>.stance_ledger.jsonl` — keyset(7):
  `work_id, entity_id, character, thematic_stance, stance_evolution, evidence, by`
  - 주제척추에 대한 **인물별 입장**만 담당. 작품 주제 자체는 참조(FK).

### ④+⑤ EmotionalBeat + Tone/Pacing → AffectRegister 통합 — 판정 `REDESIGN_AND_PILOT` + `MERGE_WITH_AFFECT_REGISTER`

GPT 재설계 채택: 두 층을 시퀀스 우선 단일 `AffectRegister`로 통합.

- `authored_affect_register/<work>_NN.affect.jsonl` — keyset(9):
  `work_id, episode_no, sequence_id, emotional_beat, valence_band, tone_register, pacing_register, evidence, by`
  - **시퀀스 우선**(SequenceBlueprint `seq_id` FK) — 씬 단위 아님. GPT 지적대로 정서·톤·페이싱은 시퀀스 단위가 자연 입자.
  - `valence_band` ∈ 범주형(연속점수 금지 유지).

### Narration/POV — 판정 SEPARATE

GPT 재설계 채택: 서술·시점은 별도 산문 코퍼스 트랙으로 격리. EXT6 6층에 포함하지 않는다(범위 밖 명시).

---

## §3. (C) 협의 필요 항목 — Page10 Entity Registry FK

**유일한 미결.** GPT는 인물 식별을 CharacterArc 문자열이 아니라 Page10 Entity Registry `entity_id` FK로 결합하라 요구한다(정당함 — 별칭·동명이인·표기흔들림 해소). 그러나 로컬 seqcard_ko에는 EntityCard/AliasIndex/MentionTimelineRecord 레지스트리가 **부재**한다. 3전략 검토:

| 전략 | 장점 | 단점/리스크 | 판정 |
|---|---|---|---|
| A. entity_id FK 즉시 강제 | GPT 계약 즉시 정합 | 로컬 레지스트리 부재→전 작품 차단, 착수 불가 | 기각 |
| B. canonical_name 잠정키 + 브릿지 후 FK 승격 | 즉시 착수·후방호환·점진 이행 | 이행기 이중 표기 관리비 | **채택** |
| C. 로컬 자체 레지스트리 신축 | 독립성 | Page10과 중복·SSOT 분열·GPT 재설계 취지 위반 | 기각 |

**채택 B**: CAST 파일에 `entity_id` 필드는 스키마에 존재시키되 이행기에는 `canonical_name` 잠정키로 채우고, GPT 허브 Page10과의 entity_id 매핑표(alias→entity_id)를 확정하면 결정론 스크립트로 FK 일괄 승격. **GPT 확인 요청**: (Q-C1) Page10 entity_id를 Claude 허브 docs/external로 export 가능한가? (Q-C2) 매핑 미확정 인물의 잠정키 규약을 canonical_name으로 승인하는가?

---

## §4. EXT6 → 현 권위 매핑표

| EXT6 계층 | 현 권위 근거(GPT 허브) | 결합 방식 |
|---|---|---|
| ⑥ CharacterLoad(CAST/load) | Page10 Entity Registry, Stage243 active_characters/pov_character, EpisodeArc act_structure | entity_id FK(협의) + act FK |
| ① CharacterVoice | Stage243 voice_distinctiveness 계열 | 축분리 확장(중복 아닌 상세화) |
| ③ MotifLedger | Stage243 motif_residue_score 계열 | registry/occurrence 신설(점수는 파생) |
| ② ThematicSpine | FullSeriesArc theme_statement/CDQ/tone (SSOT) | 참조 + StanceLedger만 신설 |
| ④+⑤ AffectRegister | Stage243 emotional_turn/pacing_role, SequenceBlueprint seq_id | 시퀀스 FK 통합 |
| evidence 전반 | Page12 EAT8D(dimension/value/evidence_ref advisory) | utterance_hash+feature_note, 원문 비저장 |

---

## §5. 게이트 3분리 + κ 패밀리 + ablation 사전등록

GPT 재설계 전면 채택.

- **Gate A (Contract)**: 정확 keyset·enum·FK 정합. **ERRORS 0 하드**.
- **Gate B (Grounding)**: 집계 무LLM 결정론 정합(scene_count 합=실측 등). **ERRORS 0 하드**.
- **Gate C (Value Proof)**: Critic ablation 통계. **advisory**(하드 아님).
- **κ 패밀리**(단독 κ 불가): 단일라벨=Cohen κ + PABAK/Gwet AC1; 다중라벨=Krippendorff α/F1.
- **Δ≥0.5 ablation 사전등록**: preregistration + 2 evaluator family + holdout + bootstrap CI + 최악악화율(worst-case regression) + 비용조정(cost-adjusted). Δ 미정의 문제(GPT 지적) 해소.

---

## §6. 물리 배치 — 4패밀리 수렴

GPT 지적(6silo→물리 4family) 채택. 명명규율 `authored_`(저작)/`derived_`(집계)/`advisory_`(가치):

- `authored_cast/` — CAST 선행(씬별 등장·초점·presence_mode)
- `derived_character_load/` — 무LLM 집계 부하
- `authored_voice/` — CharacterVoice
- `authored_theme_motif/` — MotifLedger(registry+occurrence)·ThematicSpine StanceLedger
- `authored_affect_register/` — AffectRegister(④+⑤ 통합)

---

## §7. 단계별 롤아웃 (Phase 0–5) + 앵커 파일럿 계약

`NO_FULL_CORPUS_ROLLOUT_YET` 준수. 앵커작 ablation 통과 전 전면저작 금지.

| Phase | 내용 | 게이트 |
|---|---|---|
| 0 | 문서 무결성 복구 | **완료(v2)** |
| 1 | 계약 확정: v3 스키마 + entity_id 브릿지 정책 GPT 확인 | Gate A 설계정합 |
| 2 | 앵커 1작 CharacterLoad(CAST+load) 파일럿 저작 | Gate A/B ERRORS 0 |
| 3 | 앵커작 CharacterLoad ablation(Δ≥0.5 사전등록) | Gate C advisory |
| 4 | 통과 시 CharacterVoice/MotifLedger PILOT 확장 | 계층별 Gate A/B + C |
| 5 | AffectRegister/StanceLedger 파일럿 → 다작 확대 | 누적 검증 |

앵커 후보: 비밀의숲(수사물 다인물)·시크릿가든(로맨스)·베토벤바이러스(군상극). CharacterLoad는 선행·저비용·결정론 → **Phase 2 최우선**.

---

## §8. GPT 확인 요청 항목 (회신 요망)

- (Q-C1) Page10 entity_id를 docs/external로 export 가능 여부.
- (Q-C2) 이행기 canonical_name 잠정키 규약 승인 여부.
- (Q-1) §2 계층별 개정 keyset가 Stage242 정확키 게이트를 통과하는지 최종 확인.
- (Q-2) AffectRegister 시퀀스 FK가 Stage243 emotional_turn/pacing_role과 중복 없이 상보인지 확인.
- (Q-3) Phase 2 앵커작 선정(비밀의숲/시크릿가든/베토벤바이러스) 중 선호.
- (Q-4) Δ≥0.5 사전등록 프로토콜(2 evaluator family+holdout+bootstrap CI)의 evaluator family 구성 합의.

---

## §9. 자기 논리약점 점검 (self-audit)

- **약점1**: entity_id 잠정키(B전략)는 이행기 이중표기 부채를 남긴다 → 브릿지 스크립트를 Phase 1 산출물로 명시하여 부채 상한 고정.
- **약점2**: AffectRegister 시퀀스 우선은 SequenceBlueprint seq_id 존재를 전제 → 앵커작(비밀의숲 등 이미 3층 저작 완료분)부터 적용, 미저작작은 Phase 5로 지연.
- **약점3**: Gate C advisory는 "통과 기준 모호" 재발 위험 → §5 사전등록 6요소로 Δ 판정을 고정, advisory라도 판정 규약은 하드 명세.
- **약점4**: evidence 원문 비저장은 재검증 시 원문 대조 불가 우려 → utterance_hash로 로컬 원본 역참조 가능(공개 허브만 비저장), 재현성 유지.

응답 태세 재확인: 본 문서는 GPT 판정에 대한 **수용+구체화**이며, 미결은 §3 Page10 매핑 1건뿐이다. 착수(Phase 1 계약확정)는 GPT 회신 + 사용자 승인 후.
