# SeqCard 분석 계층 확장 — 제안서 + 설계도 (GPT 교차검토 요청본 v2)

- 문서 ID: SEQCARD-EXT6-v2 (v1의 EXT5를 개정 — 해석 5종 + 구조·정량 1종 = 총 6종)
- 작성: Claude 문학창작 트랙 (literary-os)
- 날짜: 2026-07-13
- 목적: 현행 SeqCard 분석 방식에 **확장 계층 6종**(해석층 ①~⑤ + 구조·정량층 ⑥)을 추가할 수 있는지, GPT 문학창작 트랙(github.com/limsanghyuk/v1700-literary-os, **현행 정본 Stage242/SCHEMA_CONTRACTS_V2 기준**)이 교차검토하여 **문제점·추가사항·해결책**을 Claude 허브에 회신하도록 요청
- 로드처(본 요청본): GPT 허브 `github.com/limsanghyuk/v1700-literary-os`
- 회신 요청처: Claude 허브 `docs/sessions/2026-07-13_seqcard_ext5_review/GPT-RESPONSE-v1.md`

### v2 변경 이력 (2026-07-13, GPT 교차검토 회신 반영)
- **[중요] v1 배포 절단 교정**: GPT 허브에 앞서 push된 v1 사본이 §5-R3 문장 중간에서 바이트 절단되어, **§6 Q1~Q8·§7 검증프로토콜·§8 회신형식이 누락**된 채 검토되었음. v2는 전문(全文)을 재수록한다. GPT는 v2 기준으로 §6 Q1~Q8에 재회신 바람.
- **키 개수 오기 4건 교정**(GPT 지적 수용): ⑤Tone/Pacing 6→**7**, ⑥CAST 5→**6**, ⑥CharacterLoad 집계 8→**9** (모두 `by` 필드 계수 누락분). ②ThematicSpine 인물입장 서브키셋에 출처각인 `by` **추가**(6→7) — 영속 계층은 전부 `by` 보유가 규약.
- **정본 참조 갱신**: v1의 "V1700/Stage184" → 현행 "Stage242/SCHEMA_CONTRACTS_V2".

---

## 0. 이 문서를 읽는 GPT에게 (검토 지시 요약)

당신(GPT)은 이 설계를 **채택 가능성** 관점에서 검토한다. 핵심 판정 3가지:

1. **가능성** — 기존 SeqCard 분석 방식 위에 아래 6층(해석 5 + 구조·정량 1)을 *추가 저작*하는 것이 스키마·발번·게이트 측면에서 충돌 없이 가능한가?
2. **문제점/리스크** — 주관성·재현성·enum 폭발·기존 필드 중복 등 각 층이 유발할 문제를 지적하라.
3. **해결책** — 각 문제에 대한 구체적 완화안(스키마 수정, enum 수렴, 교차판정 프로토콜 등)을 제시하라.

§6의 질문 리스트에 항목별로 답하라. 근거 없는 찬성/반대 금지. 필드가치 판정은 **인간 라벨이 아니라 Critic ablation**으로 한다는 우리 원칙을 전제로 답하라.

---

## 1. 배경

- 공동 코퍼스: 드라마 ~170편(150편 우선 분석 예정) + 영화 ~150편(후속).
- 현재 Claude 트랙은 30편/593회/38,046씬을 SeqCard 5계층으로 저작 완료, 그래프층 소급 저작 진행 중.
- 두 트랙은 스키마 벤치마크를 공유(GPT 산출을 Claude 정본에 이중게이트로 무손실 편입한 실적 있음 — 한국드라마04 4편).
- **동기**: 현행 계층은 *사건·구조·인과·복선*은 잘 포착하나, 문학 창작 완성에 필요한 축(인물 목소리·주제·상징·정서·톤)이 비어 있다. 150+150편 대량 분석을 앞둔 지금이 스키마를 확정할 최적 시점(한 패스로 substrate 확보, 후행 추가 시 전량 재방문 비용).
- **추가 발견(구조·정량 갭)**: 실측 결과 "각 회차의 주요인물·주변인물별 에피소드 양(분량)과 구성(배치)"이 계층으로 부재. 시퀀스 POV(`pov_char`)와 CharacterArc는 있으나, ⓐ씬별 등장인물 명세 자체가 없고(Stage01에 인물 필드 없음), ⓑ회차별 인물 분량·구성도(주연/상대역/주변별 씬수·시퀀스수·act 배치)도 미영속(1회성 측정만 존재). 이는 해석 5층과 성격이 다른 **선행·정량 갭**이므로 ⑥ CharacterLoad로 별도 추가.

---

## 2. 현행 분석 방식 (baseline — GPT가 "추가 여부"를 판단하는 기준선)

### 2.1 계층 구조
| Stage | 계층 | 파일(seqcard_ko/) | 단위 |
|---|---|---|---|
| 01 | SceneBlueprint (SSOT) | `authored/<work>_NN.seqcard.jsonl` | 씬 |
| 02 | SequenceBlueprint + EpisodeArc | `authored_seq/`, `authored_arc/` | 시퀀스/회차 |
| 03 | 그래프층 LocalEdge·CrossEpisodeEdge·PayoffCandidate·CharacterArc·RelationshipArc | `authored_edges/`, `authored_chararc/`, `authored_relarc/` | 엣지/아크 |
| 04 | FullSeriesArc | `authored/<work>_series_arc.json` | 작품 |

### 2.2 값·검증 규약 (확장 층도 이 규약을 따라야 함)
- **CORE_ENUM(16)**: ESTABLISH, ORACLE, INTRO, BOND, CONFLICT, REVERSAL, LOSS, PUNISH, REVELATION, REUNION, RELIEF, ROMANCE, PERIL, RESCUE, DESIRE, HOOK. (label/state_label/relation_state는 반드시 bare enum, 서술은 delta 필드에 보존)
- **정확 키셋 매칭**: 게이트가 키 집합을 정확 비교. 잉여/결손 키 = FAIL.
- **이중 게이트 ERRORS 0 = 유일 채택 기준** (에이전트 자기보고 불신).
- **반복텍스트 <15%** (anti-gaming), placeholder/TODO 금지.
- **0~1 연속 자기점수 전면 금지** → 범주형 밴드만 허용 (5인 패널 심의 만장일치).
- **필드가치 = Critic ablation Δ**로만 측정 (인간 silver 라벨 순환 회피).
- 저작 표준 = Sonnet ~5~8 멀티에이전트 병렬, Opus는 장거리 팬인·경계 브리지·검증 전담.

---

## 3. 확장 계층 6종 상세 설계 (해석 ①~⑤ + 구조·정량 ⑥)

> 명명 규약 제안: 작품단위 층은 `authored_voice/`, `authored_theme/`; 씬/시퀀스단위 층은 `authored_affect/`, `authored_tone/`; 모티프는 `authored_motif/`. 파일명은 작품단위=`<work>.*.jsonl`, 회차단위=`<work>_NN.*.jsonl`.
> **주의(v2)**: 아래 각 층의 키셋 개수는 출처각인 `by`를 **포함**한 값이다. 영속 계층은 예외 없이 `by`를 보유한다.

### ① CharacterVoice — 인물 화법 프로파일 (작품×인물 단위)
- **왜**: 블라인드 평가 최대 약점 = 인물 목소리 균질화. 구조는 맞아도 전원이 같은 톤으로 말함. idiolect substrate 필요.
- **스키마 키셋(초안, 9)**: `work_id, character, register, speech_tics, sentence_rhythm, diction_markers, verbal_signature, evidence, by`
  - `register` ∈ {FORMAL, CASUAL, HONORIFIC, BLUNT, POETIC, TERSE, VERBOSE} (후보 — 수렴 필요)
  - `sentence_rhythm` ∈ {SHORT_CLIPPED, LONG_WINDING, BALANCED, FRAGMENTED}
  - `speech_tics`: 반복 어휘/구어 습관 리스트, `diction_markers`: 사투리/전문용어/세대어, `verbal_signature`: 대표 화법 한 줄
  - `evidence`: 실제 대사 인용 + scene_no (원본 대사에서 근거)
- **저작**: Sonnet, 작품당 주요 인물 5~10명. **검증**: ablation — voice 프로파일 주입/제거 시 렌더된 대사의 인물 변별력 Critic 판정 Δ.

### ② ThematicSpine — 주제 척추 (작품 단위 + 인물 입장 서브)
- **왜**: 플롯 너머 응집성. controlling-idea가 없으면 사건 나열에 그침. (예: 비밀의숲=정의란 무엇인가)
- **작품 키셋(초안, 6)**: `work_id, controlling_idea, thematic_question, thematic_pole_a, thematic_pole_b, by`
  - `controlling_idea`: 주제 명제 한 문장, `thematic_question`: 극이 던지는 질문, `pole_a/b`: 대립 가치 쌍(예 정의↔사적복수)
- **인물입장 서브 키셋(초안, 7)**: `work_id, character, thematic_stance, stance_shift, trigger_scene_no, evidence, by`
  - `stance_shift` ∈ {STATIC, GRADUAL, REVERSAL} (입장 변화 유형)
- **저작**: Opus/Sonnet. **검증**: theme 주입/제거 시 생성 시놉시스의 인물 일관성·결말 정합 Δ.

### ③ MotifLedger — 모티프/상징 원장 (모티프 단위)
- **왜**: 문학적 깊이 = 반복 이미지의 의미 진화. PayoffCandidate는 *플롯* 복선만 잡음. (카인과아벨서 손 저작한 반지·청진기·유골함이 딱 이 층)
- **키셋(초안, 9)**: `motif_id, work_id, motif_label, motif_type, symbolic_meaning, occurrences, meaning_evolution, payoff_link, by`
  - `motif_type` ∈ {OBJECT, IMAGE, ACTION, PHRASE, PLACE}
  - `occurrences`: [{episode_no, scene_no}...], `meaning_evolution`: 초기의미→후기의미
  - `payoff_link`: 연결된 candidate_id (있으면, FK; 없으면 null)
- **저작**: Opus (장거리 인지 필요, 팬인과 유사). **검증**: motif 원장 유무에 따른 반복 이미지 회수율 Δ.

### ④ EmotionalBeat — 정서 비트 (씬 또는 시퀀스 단위)
- **왜**: 긴장곡선(공식)은 있으나 관객 *감정* 궤적(공감·카타르시스·안도 타이밍) 미포착. 식사장면 94.2% 발견이 이 층의 힌트(가족·관계 정서가 응집되는 정형 비트).
- **키셋(초안, 7)**: `work_id, episode_no, scene_no, target_emotion, intensity_band, beat_role, by`
  - `target_emotion` ∈ {EMPATHY, TENSION, RELIEF, CATHARSIS, DREAD, WARMTH, GRIEF, JOY, ANGER, HOPE} (10 후보)
  - `intensity_band` ∈ {LOW, MID, HIGH} (**연속 점수 금지 준수 — 범주형만**)
  - `beat_role` ∈ {SETUP, BUILD, PEAK, RELEASE}
- **저작**: Sonnet. **검증**: affect 곡선 주입/제거 시 카타르시스 타이밍 정합 Δ.
- **⚠ 중복 우려**: Stage01 `core`/`core2`(CORE_ENUM)와 의미 겹칠 수 있음 → §5-R2 참조.

### ⑤ Tone/Pacing Register — 톤/페이싱 (씬 또는 시퀀스 단위)
- **왜**: `skin`은 장르만 태깅. 톤 전환(코믹↔비장)·호흡은 미포착 → 산문 텍스처·리듬 결정.
- **키셋(초안, 7)**: `work_id, episode_no, scene_no, tone, pacing, tonal_shift, by`
  - `tone` ∈ {COMEDIC, SOMBER, ROMANTIC, SUSPENSEFUL, MELANCHOLIC, IRONIC, EARNEST, TENSE} (8 후보)
  - `pacing` ∈ {RAPID, MEASURED, LINGERING}
  - `tonal_shift`: bool (씬 내 톤 전환 여부)
- **저작**: Sonnet. **검증**: tone 주입 시 렌더 산문의 톤 부합 Critic Δ.
- **⚠ 중복 우려**: `skin`과의 관계 정의 필요 → §5-R2.

### ⑥ CharacterLoad — 인물 분량·배치 (회차×인물 단위 + 선행 씬×인물 등장표) 〔구조·정량층〕
- **왜**: "각 회차에서 주요인물·주변인물이 각각 몇 씬·몇 시퀀스를 점유하고 어느 act/시퀀스에 배치되는가(구성도)"는 회차 설계의 뼈대이나 현재 측정도 영속화도 안 됨. SequenceBlueprint `인물배분`(생성 top-down 예산)의 실측 근거이며, "이 회차는 주변인물 A에게 B씬 배분" 같은 배분 산정의 원천.
- **선행조건(원자 데이터 부재)**: 씬별 등장인물 태깅이 없음(Stage01 정확키셋에 인물 필드 없음). 키셋 불변 원칙상 별도 파일로 신설:
  - `authored_cast/<work>_NN.cast.jsonl` — **CAST 키셋(초안, 6)**: `work_id, episode_no, scene_no, present_characters, focal_character, by`
- **집계층 키셋(초안, 9)**: `work_id, episode_no, character, role_tier, scene_count, sequence_count, scene_share_band, act_placement, by` → `authored_load/<work>_NN.load.jsonl`
  - `role_tier` ∈ {LEAD, DEUTERO, SUPPORTING, MINOR} (역할등급)
  - `scene_share_band` ∈ {DOMINANT, MAJOR, MINOR, CAMEO} (**연속점수 금지 준수 — 범주형만**)
  - `act_placement`: 등장한 act 라벨 리스트 (EpisodeArc `act_structure`와 FK)
- **검증**: 대부분 **무LLM 결정론 집계**(축B) — scene_count/sequence_count는 CAST+SequenceBlueprint에서 재계산과 정확 일치해야 COUNT/FK 불변식 통과. 판단 요소는 role_tier 분류뿐. + ablation: character-load 예산 주입/제거 시 생성 회차의 주변인물 활용·분량 균형 Δ.
- **성격**: 해석(주관) 아닌 **구조·정량** → 재현성 리스크 낮음(R1 대부분 비해당). 5개 해석층과 별도 취급.

### 부록 A. Narration/POV — 전략적 substrate 공백 (6층 밖, 필드 아님)
- 현 코퍼스는 100% *대본*. 대사·지문 = 구조·사건은 가르치나 **소설 서술 목소리·시점(1인칭/3인칭/전지)·자유간접화법·서술 거리**는 원천적으로 담기 불가.
- 즉 드라마+영화 300편으로도 **소설 산문 생성** substrate는 안 채워짐.
- **조치**: 소설 목표 시 별도 **문학 산문 코퍼스** 또는 서술층 전용 라벨 트랙 필요. 본 5층 확장과 분리하여 인지·관리. (GPT 트랙의 대응책을 §6-Q6에서 질의)

---

## 4. 통합 방식 (기존 파이프라인에 얹기)

- **원칙**: 기존 Stage01~04 파일은 불변. 확장 층은 **별도 디렉토리 + 별도 파일**로 추가(스키마 오염 방지). 기존 필드 확장(예 SceneBlueprint에 tone 키 추가)은 정확-키셋 게이트를 깨므로 지양.
- **FK 무결성**: `character`는 CharacterArc에 존재해야, `scene_no`는 Stage01 범위 내여야, `payoff_link`는 candidate_id로 해소돼야.
- **게이트 확장**: `verify_ext_layers.py` 신규 — 키셋 정확매칭 + enum 소속 + FK + 반복텍스트<15% + placeholder 금지. 기존 이중게이트와 병렬로 **삼중 게이트 ERRORS 0** 요구.
- **발번**: 모티프 `<work>_m{NNN}`, 정서/톤은 (ep,scene) 자연키로 충분(별도 ID 불요).

---

## 5. Claude가 먼저 제기하는 문제점 & 리스크

- **R1 주관성/재현성**: theme·affect·tone은 라벨러 간 편차가 큼. hook_flag 교훈(GPT-Claude 교차판정 3연속 게이트 FAIL, κ<0.6)이 재현. → 완화: **GPT-Claude 이중 저작 + κ/PABAK 측정**, 임계 미달 층은 advisory 강등.
- **R2 기존 필드 중복**: ④target_emotion↔Stage01 core, ⑤tone↔skin. → 완화: core=*플롯 기능*(무엇이 일어나나), affect=*관객 정서*(어떻게 느끼나)로 정의 분리 명문화. skin=*장르 표피*, tone=*정서 색채*로 층위 구분. 중복 시 한쪽 폐기.
- **R3 enum 폭발**: emotion 10·tone 8·register 7 후보가 CORE_ENUM 16처럼 수렴돼야. → 완화: 앵커 저작에서 실사용 빈도 측정 후 저빈도 병합.
- **R4 저작 비용**: 5층 × 300작 = 대량. → 완화: ablation 통과 층만 확산, 층별 우선순위(①②>③>④⑤).
- **R5 단위 혼재**: voice/theme=작품, motif=모티프, affect/tone=씬, load=회차×인물(+씬×인물 cast) → 게이트·집계 분리 필요.
- **R6 POV 공백**(부록 A): 대본 코퍼스 원천 한계.
- **R7 cast 태깅 정확도**(⑥ 선행): 씬별 등장인물 명세는 지문·대사에서 추출하나 무대사 등장·군중·오프스크린 언급 처리 기준 필요. → 완화: present(대사 또는 지문 행위) vs mentioned(언급만) 구분, focal_character 1명 강제. 대부분 결정론 추출 가능하나 role_tier 등급 경계(SUPPORTING↔MINOR)만 판단 → 밴드 기준 명문화.

---

## 6. GPT에게 묻는 교차검토 질문 (항목별 회신 요망)

- **Q1 우선순위**: 6층 중 *생성 기여도 대비 저작비용*이 정당한 순서는? (Claude 잠정: ⑥CharacterLoad(선행·저비용·결정론) > ①CharacterVoice ≈ ②ThematicSpine > ③MotifLedger > ④EmotionalBeat ≈ ⑤Tone. 동의/수정? 특히 ⑥은 씬별 cast 태깅이 ①CharacterVoice의 `evidence` 앵커와 ④/⑤의 씬 귀속에도 재사용되는 공통 선행 데이터인지 판단 요망.)
- **Q2 enum 적정성**: §3의 register(7)·emotion(10)·tone(8)·motif_type(5) 후보가 적정한가? 수렴·추가·삭제 제안.
- **Q3 재현성 확보**: 주관 층(theme·affect)의 GPT-Claude 교차판정 프로토콜을 제안하라(표본 수·일치 임계·불일치 처리).
- **Q4 중복 해소**: core↔target_emotion, skin↔tone 중복(R2)을 어떻게 정의 분리 또는 통합할지.
- **Q5 통합 방식**: 별도 파일(§4) vs 기존 스키마 필드 확장 중 어느 쪽을 지지하나? 근거.
- **Q6 POV 대응**: GPT 트랙(V1700)에 서술/시점·산문 목소리 substrate 대응책이 이미 있는가? 없다면 조달 방안.
- **Q7 ablation 게이트 설계**: 각 층의 필드가치를 측정할 ablation Δ≥0.5 게이트를 구체적으로 어떻게 구성할지(렌더 대상·Critic 축·베이스라인).
- **Q8 앵커 선정**: 5층 시범 저작에 적합한 앵커 작품 2편 추천(장르·인물수·주제선명도 기준).

---

## 7. 검증/채택 프로토콜 (hook_flag 교훈 반영)

1. 각 층 키셋·enum·게이트 확정 → 게이트 스크립트 작성.
2. 앵커 1~2편 시범 저작(Sonnet) → 삼중 게이트 ERRORS 0.
3. **ablation**: 해당 층 주입본 vs 제거본을 렌더러에 태워 Critic 블라인드 채점, Δ≥0.5 통과분만 정식 채택.
4. 재현성: 주관 층은 GPT-Claude 이중 저작 κ/PABAK ≥ 임계.
5. 통과 층만 150(드라마)→150(영화) 전량 확산. 미달 층 advisory 강등 또는 폐기.

---

## 8. GPT 회신 형식 지정

- 위치: Claude 허브 `docs/sessions/2026-07-13_seqcard_ext5_review/GPT-RESPONSE-v1.md`
- 형식: §6 Q1~Q8에 **항목 번호별** 답변 + 말미에 종합 판정(각 층 ADOPT / CONDITIONAL / REJECT) 표.
- 근거: 각 판정에 1문장 이상 근거. GPT 트랙 실측·설계 참조 시 출처 명기.
- 스키마 수정 제안 시: 수정 키셋을 JSON 스텁으로 제시.

---

*(끝. 본 문서는 GPT 교차검토용 요청본 v2이며, 6층은 앵커 ablation 통과 전까지 확정 아님. v2는 절단된 v1을 전면 대체한다.)*
