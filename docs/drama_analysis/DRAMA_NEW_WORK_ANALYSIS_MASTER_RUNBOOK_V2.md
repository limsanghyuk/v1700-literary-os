# 신규 드라마 분석 마스터 런북 V2

- Document ID: `DRAMA-NEW-WORK-ANALYSIS-MASTER-RUNBOOK-V2`
- Status: `AUTHORITATIVE_CANDIDATE`
- Date: 2026-07-17
- Scope: 새로운 한국 드라마 원본의 SourceLock, Stage01~04 직접독해, 앙상블 인물·관계 추적, 검증, 패키징, `seqcard_ko` 편입
- Exact schema authority: `docs/drama_analysis/SCHEMA_CONTRACTS_V2.md`
- Default extension policy: `EXT6/HXT6 = DEFERRED_DISABLED`
- Promotion policy: 사용자 승인 전 `PASS_CANDIDATE`, 승인 후에만 `CANONICAL`

---

## 0. 이 문서의 목적

이 문서는 새 대화창·새 모델·새 실행 환경이 과거 대화 전체를 다시 조사하지 않고도 새로운 드라마 한 작품을 즉시 분석하도록 만든 단일 실행 런북이다.

이 문서만으로 다음 전체 흐름을 이해하고 시작할 수 있어야 한다.

```text
원본 확보·정규 저장
→ SourceLock
→ 회차 Q1→Q4 직접독해
→ Stage01 SceneCard
→ Stage02 SequenceBlueprint·EpisodeArc
→ Stage03 앙상블 CharacterArc·RelationshipArc·선별적 LocalEdge·PayoffCandidate
→ 회차 경량 게이트
→ 약 8회차 블록 강검증
→ 전 시즌 Stage01~03 강검증
→ Stage04 후보 100% disposition
→ CrossEpisodeEdge·FullSeriesArc
→ 독립 작품 패키지
→ 전체 DB 편입
→ fresh extraction·실제 CLI 재검증
→ PASS_CANDIDATE
```

이 문서는 기존 exact schema를 변경하지 않는다. 키셋·자료형·enum·ID·FK·불변식이 충돌하면 언제나 `SCHEMA_CONTRACTS_V2.md`가 우선한다.

---

## 1. 새 대화창 최소 로드 순서

새로운 드라마 분석을 시작할 때 다음 문서만 순서대로 읽는다.

```text
1. docs/drama_analysis/README.md
2. docs/drama_analysis/DRAMA_NEW_WORK_ANALYSIS_MASTER_RUNBOOK_V2.md
3. docs/drama_analysis/SCHEMA_CONTRACTS_V2.md
4. docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json
```

다음 문서는 충돌 해결·정밀 감사·중단 복구 시 사용한다.

```text
DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md
DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md
DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md
DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md
DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md
DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md
DRAMA_SESSION_EXECUTION_SAFETY_V1.md
EXT6_DEFERRED_SIDECAR_POLICY_V1.md
```

### 1.1 권위 순서

```text
1. SCHEMA_CONTRACTS_V2
2. 이 MASTER_RUNBOOK_V2
3. CURRENT_OPERATING_SUPPLEMENT
4. DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT
5. ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY
6. CLOSE_READING_MASTER_PROTOCOL
7. VALIDATION_AND_RELEASE_GATES
8. LINEAGE_PACKAGE_HANDOFF
9. SESSION_EXECUTION_SAFETY
10. DATABASE_STATUS
11. 최신 세션 README
```

---

## 2. 절대 원칙

### 2.1 원본이 최종 증거다

- 기존 SceneCard·요약·시놉시스는 탐색 색인일 뿐이다.
- 의미 판단이 충돌하면 원본 대본을 다시 읽는다.
- 원본이 누락되거나 중복되면 추정·줄거리·방송 기억으로 채우지 않는다.

### 2.2 Python은 의미를 생성하지 않는다

Python 허용 범위:

```text
ZIP/HWP/TXT 해제·변환
인코딩 확인
파일 정렬
헤딩·ordinal 보조
SHA256·offset·line span
JSON/JSONL 직렬화
keyset·enum·FK·coverage·중복·반복 검증
결정론적 count/runtime/core_mix/ID 교정
manifest·checksum·ZIP
```

Python 금지 범위:

```text
SceneCard 의미 문장
Sequence goal·obstacle·value_shift·turn
EpisodeArc 의미
CharacterArc·RelationshipArc 의미
LocalEdge 인과 판단
PayoffCandidate 선택
candidate disposition
CrossEpisodeEdge 의미
FullSeriesArc 의미
```

### 2.3 형식 PASS와 내용 PASS를 구분한다

```text
JSON 파싱 PASS ≠ 의미 PASS
Stage02 coverage PASS ≠ Stage01 깊이 PASS
수량이 많음 ≠ 앙상블 품질이 높음
ZIP CRC PASS ≠ 분석 품질 PASS
사람용 보고서 PASS ≠ 실제 데이터 PASS
```

### 2.4 기존 정상 자산은 보존한다

업그레이드 작품은 결함 범위만 다시 읽는다. 형식 오류를 고치면서 의미를 은밀히 바꾸지 않는다.

- `semantic_text_changed=false`: ID·FK·count·runtime·label 같은 결정론적 교정
- `semantic_text_changed=true`: 원본 재독해가 필요한 새 run

---

## 3. 시작 전 작품 분류

원본과 기존 자산을 조사해 반드시 하나로 분류한다.

### 3.1 `NEW_ANALYSIS`

- 원본은 존재한다.
- Stage01~04 의미 자산이 없다.
- EP01 Q1부터 시작한다.

### 3.2 `NORMAL_UPGRADE`

- Stage01·02가 원본에 밀착돼 있다.
- 현행 keyset·ID 정규화 후 Stage03·04 보완이 가능하다.

### 3.3 `STAGE02_PARTIAL_REAUTHOR`

- 일부 회차에만 목표·장애·전환 드리프트가 있다.
- 결함 회차만 원본과 Stage01을 다시 읽고 Stage02 이후를 재저작한다.

### 3.4 `STAGE02_FULL_REAUTHOR`

다음 중 하나가 광범위하면 전면 재저작한다.

- 같은 문장 골격 반복
- 장면 수를 수학적으로 균등 분할한 시퀀스
- 미래 회차 정보가 앞 회차로 유입
- goal·obstacle·value_shift가 원본과 불일치
- POV·turn·act가 실제 극적 행동 단위와 불일치

### 3.5 `SOURCE_HOLD`

- 원본 회차 누락
- 서로 다른 회차 파일이 동일 바이트
- 번호 위장·중복 판본
- 인코딩 손상으로 원문 판독 불가
- 원본 장면 수와 Stage01을 잠글 수 없음

`SOURCE_HOLD`에서는 의미 분석을 진행하지 않는다.

### 3.6 `LONG_FORM_BLOCK_PLAN`

30회 이상 작품은 약 8회차 전달·검증 블록으로 계획한다. 그러나 의미 저작·잠금은 한 회차씩 수행한다.

---

## 4. 원본 저장과 SourceLock

### 4.1 원본 정규 저장 경로

분석 전에 먼저 다음 폴더를 만든다.

```text
seqcard_ko/original_extracted/{작품명}/
  {작품명}_01.txt
  {작품명}_02.txt
  ...
```

루트에 회차 TXT를 흩어 놓지 않는다. 작품별 폴더가 없으면 완전한 SourceLock으로 보지 않는다.

### 4.2 원본 preflight

각 작품에서 확인한다.

1. 예상 회차 수와 파일 수
2. 파일명 회차와 본문 회차 표식 일치
3. 누락·중복·추가 부속 파일
4. HWP/CP949/UTF-16 등 원래 인코딩
5. UTF-8 canonical storage 변환 성공
6. 물리 장면 마커와 논리 장면 경계
7. 분석 참조용 canonical `scene_no=1..N`
8. 원본 및 정규 저장본 SHA256
9. 원본 번호 이상·결번·하위 씬 번호
10. 다음 재개 지점

### 4.3 이중 해시

SourceLock은 반드시 구분한다.

```text
original_bytes_sha256
= 입수 ZIP/HWP/CP949 등 원래 바이트

canonical_storage_sha256
= original_extracted에 저장된 UTF-8 TXT 바이트
```

인코딩 변환으로 두 해시가 다른 것은 정상이다. SceneCard JSON 해시를 원본 장면 해시로 기록하면 실패다.

### 4.4 SourceLock 필수 상태

```text
source_provenance_class
original archive/file identity
canonical storage path
canonical storage encoding
회차별 SHA256
canonical scene count
quarter ranges
source marker anomaly
excluded noncanonical files
current completed episode
next pointer
direct_reading_attested
python_semantic_generation=false
```

### 4.5 SourceLock 실패 시

- 분석 파일을 만들지 않는다.
- `SOURCE_HOLD` 사유와 허용 가능한 복구 원본을 기록한다.
- 원본이 복구되기 전까지 Stage01을 시작하지 않는다.

---

## 5. 안전 작업 단위와 상태 전이

### 5.1 고정 작업 단위

```text
의미 독해 최소 단위 = quarter
원자 잠금 단위 = 1 episode
강검증 기본 블록 = 약 8 episodes
Stage04 = full-series fan-in
```

### 5.2 회차 상태

```text
INTERRUPTED_BEFORE_PERSISTENCE
FILES_PRESENT_VALIDATION_PENDING
EPISODE_LIGHT_LOCKED
BLOCK_STRONG_LOCKED
FULL_STAGE01_03_LOCKED
STAGE04_LOCKED
```

대화에서 완료했다고 말했어도 실제 파일이 없으면 완료가 아니다.

### 5.3 회차 실행 루프

```text
EPxx source preflight
→ Q1 직접독해·Stage01·QuarterAudit·저장
→ Q2
→ Q3
→ Q4
→ EpisodeMeta
→ Stage02 SequenceBlueprint
→ EpisodeArc
→ Stage03 앙상블 스캔
→ CharacterArc
→ RelationshipArc
→ LocalEdge
→ PayoffCandidate
→ 회차 경량 게이트
→ 체크포인트
→ 다음 회차
```

---

## 6. 직접독해 핵심: 장면 6질문

각 장면에서 내부적으로 반드시 답한다.

1. **행동** — 실제로 누가 무엇을 했는가.
2. **전략** — 말하기·숨기기·회피·유도·거부 중 어떤 수를 썼는가.
3. **정보 변화** — 누가 무엇을 새로 알거나 오해하게 됐는가.
4. **선택** — 무엇을 결정·거부·보류·포기했는가.
5. **구조 기능** — 설정·압박·전환·회수 중 무엇을 수행하는가.
6. **잔여 압력** — 다음 장면·시퀀스·후속 회차를 움직이는 미해결 원인은 무엇인가.

### 6.1 장면을 잘못 읽는 전형적 방식

- 사건을 한 문장으로 요약하고 모든 필드에 복사
- 인물 감정을 원문 근거 없이 추정
- 장소 전환을 극적 전환으로 오인
- 후속 회차를 알고 앞 장면에 미래 의미를 소급
- 대사 키워드만 보고 CORE를 선택

### 6.2 좋은 장면 분석의 최소 조건

```text
구체적 행동
+ 사용된 전략
+ 정보 또는 조건 변화
+ 선택의 변화
+ 회차 내 기능
+ 다음 압력
```

---

## 7. Stage01 — SceneCard

정본은 exact 9키다.

```text
work_id, scene_no, heading, title, intent_gist,
core, core2, skin, by
```

### 7.1 필드 저작 원칙

- `heading`: 원본 provenance와 대응한다.
- `title`: 사건 표면이 아니라 장면의 고유 전환을 압축한다.
- `intent_gist`: 욕망·압력·전략·정보·선택 중 핵심 서사 기능을 쓴다.
- `core/core2`: 실제 극적 기능만 CORE_ENUM 16에서 고른다.
- `skin`: 표면 장르·연출 질감이며 core를 반복하지 않는다.

### 7.2 Stage01 금지

- 키워드 조각
- 가시적 `[EPxx-Syy]` 참조 표식
- 동일 시작구·동일 문장 골격
- title과 intent의 사건 요약 복사
- 원문 장문 대사 복사
- 원문에 없는 인물·행동·감정·인과
- Python·템플릿 의미 생성

### 7.3 내용 깊이 기준

```text
4: 행동·전략·정보·선택·구조·잔여 동력이 모두 구체적
3: 대부분 구체적이나 한 축이 약함
2: 사건 요약은 있으나 선택·정보 변화가 추상적
1: 키워드·템플릿 중심
0: 자동 생성·복사·환각
```

권장:

```text
회차 평균 >= 3.0
최저 >= 2.5 또는 해당 장면 재저작
0점·1점 장면 = 0
```

---

## 8. EpisodeMeta

exact 5키다.

```text
work_id, scene_count, core_dist, episode_function, by
```

- `scene_count`와 `core_dist`는 SceneCard에서 결정론적으로 재계산한다.
- `episode_function`은 이번 회차가 시즌에서 수행하는 기능을 구체적으로 기록한다.

---

## 9. Stage02 — SequenceBlueprint

exact 18키다.

```text
seq_id, work_id, episode_no, seq_index,
member_scene_nos, scene_span, scene_budget,
sequence_intent, goal, obstacle, value_shift,
turn_type, turn_class, core_mix, pov_char,
place_cluster, runtime_share, by
```

### 9.1 시퀀스 3축

- **Goal**: POV 인물이 이 구간에서 당장 얻으려는 것
- **Obstacle**: 인물·정보·제도·내적 저항 중 실제 방해
- **Turn**: 구간 종료 시 되돌리기 어려운 상태 변화

### 9.2 시퀀스 경계

다음 중 하나가 바뀔 때 분리를 검토한다.

- 목표 주체 또는 목표
- 장애의 성격
- 정보·관계·권력 가치
- 새로운 극적 행동 단위

장소가 바뀌어도 목표가 계속되면 같은 시퀀스일 수 있다. 같은 장소에서도 목표·권력 조건이 바뀌면 분리할 수 있다.

### 9.3 Stage02 불변식

```text
모든 scene_no가 정확히 하나의 sequence에 포함
중복 0 / 누락 0
sum(scene_budget) == scene_count
runtime_share 합계 == 1.0 ± 1e-6
core_mix ⊆ member SceneCard의 실제 core/core2
turn_class == turn_type registry 파생값
sequence_count / scene_count >= 0.11
```

밀도 하한은 경보이며 숫자를 맞추기 위한 기계 분할 지시가 아니다.

---

## 10. EpisodeArc

exact 13키다.

```text
work_id, episode_no, scene_count, sequence_count,
dramatic_question, act_structure, entry_state, exit_state,
turning_point, central_conflict_axis, episode_function,
core_dist, by
```

### 10.1 회차 독해 축

```text
Entry state
→ Dramatic question
→ Escalation
→ Turning point
→ Exit state
```

### 10.2 금지

- 시퀀스 수를 수학적으로 4등분해 act 생성
- 실제 시퀀스를 참조하지 않는 turning point
- 미래 회차 결과를 현재 회차 질문에 소급
- 사건 목록을 dramatic question이나 central conflict로 대체

---

## 11. Stage03 — 클로드식 앙상블 폭의 선택적 채택

### 11.1 채택하는 장점

새 드라마 분석은 주인공 2~3명에만 제한하지 않는다. 회차마다 다음 층을 폭넓게 스캔한다.

```text
주인공·대립자
핵심 조력자·경쟁자
조직의 의사결정자
반대 진영의 기능 인물
반복 등장하는 실무자·가족·동료
이번 회차에서 사건축을 바꾸는 단역
동맹·경쟁·상하·공모·거래·은폐 관계
```

이것이 클로드식 분석에서 채택하는 핵심 장점이다.

### 11.2 채택하지 않는 방식

```text
등장인물 전원을 기계적으로 CharacterArc화
모든 관계쌍을 RelationshipArc화
회차마다 고정 수량 생성
같은 evidence 복사
모든 장면을 다음 장면과 LocalEdge로 연결
회차 간 연결을 LocalEdge에 저장
후보를 만들고 disposition 없이 방치
레코드 수량을 품질 점수로 사용
```

### 11.3 A/B/C 앙상블 분류

Stage03 저작 전 회차 인물을 세 집합으로 나눈다.

- **A**: 회차 시작과 끝의 상태가 실제로 달라진 인물
- **B**: 신뢰·권력·정보·의존·적대 조건이 이동한 관계쌍
- **C**: 단순 등장 또는 변화 없음

Stage03 대상은 A와 B다. C를 수량 채우기 위해 Arc로 만들지 않는다.

### 11.4 앙상블 누락 감사 질문

```text
실제 변화가 있는데 빠진 핵심 의사결정자가 있는가?
실제 변화가 있는데 빠진 동맹·갈등·상하 관계가 있는가?
수량을 맞추기 위해 변화 없는 인물·관계를 넣었는가?
```

누락은 보강하고 수량 채우기는 삭제한다.

---

## 12. CharacterArc

exact 8키다.

```text
work_id, character, episode_no, state_label,
state_delta, trigger_scene_no, by, evidence
```

### 12.1 생성 조건

- 회차 입구와 출구 사이에 식별 가능한 상태 변화가 있다.
- trigger 장면에 해당 인물이 실제 등장한다.
- evidence가 변화의 구체 근거를 설명한다.
- 변화가 이후 행동의 선택 가능성을 바꾼다.

### 12.2 제외 조건

- 단순 등장
- 반복 대사만 있음
- 상태 변화 없음
- 작품 전체 성격 요약
- 다른 인물 evidence 복사
- trigger 장면에 인물이 없음

고정 최소치와 고정 최대치는 없다.

---

## 13. RelationshipArc

exact 9키다.

```text
work_id, char_a, char_b, episode_no,
relation_state, relation_delta, trigger_scene_no,
evidence, by
```

### 13.1 생성 조건

- 양쪽 인물이 함께 등장하거나 직접 통화·교신한다.
- 신뢰·권력·의무·갈등·거리·연합·거래 조건 중 하나가 바뀐다.
- `relation_state`와 `relation_delta`를 구분한다.
- 이후 선택 조건이 달라진다.

### 13.2 제외 조건

- 같은 공간에 있었을 뿐 상호작용 없음
- 관계 변화 없음
- 다른 회차의 변화 요약 복사
- `(A,B)`와 `(B,A)` 중복

---

## 14. LocalEdge — 선별적 동일 회차 인과

LocalEdge는 exact 12키 계약을 따르며 다음이 하드 게이트다.

```text
edge_type == causal
src_episode_no == tgt_episode_no
gap_episodes == 0
label == target SceneCard.core
source/target scene exists
```

### 14.1 필수 반사실 질문

```text
source 장면의 행동·정보·선택이 없었더라도
target 장면이 같은 방식으로 발생했는가?
```

- **예**: LocalEdge가 아니다.
- **아니오**: 구체 인과를 note로 설명할 수 있을 때만 생성한다.

### 14.2 배제 규칙

- 장면 번호 인접성을 인과로 간주하지 않는다.
- 같은 시퀀스라는 이유로 연결하지 않는다.
- 유사 주제·감정·모티프만으로 연결하지 않는다.
- 모든 장면을 다음 장면과 사슬로 연결하지 않는다.
- 회차를 넘는 연결을 LocalEdge에 저장하지 않는다.
- LocalEdge 수량을 품질 목표로 삼지 않는다.

### 14.3 과밀 경고

다음은 자동 실패가 아니라 수동 재감사 트리거다.

```text
LocalEdge / SceneCard > 0.10
또는
바로 다음 장면을 target으로 하는 LocalEdge 비율 > 0.50
```

회차 간 LocalEdge가 한 건이라도 있으면 blocking error다.

---

## 15. PayoffCandidate — 장거리 가능성의 임시 원장

exact 7키다.

```text
candidate_id, work_id, episode_no, scene_no,
edge_type_guess, description, by
```

### 15.1 후보로 남길 것

- 이후 의미가 달라질 수 있는 정보
- 반복될 가능성이 있는 물건·약속·위협
- 관계나 권력 조건을 바꿀 미해결 선택
- 구체적 후속 회수 가능성이 있는 장면

### 15.2 후보에서 제외할 것

- 다음 장면에서 바로 해결되는 문제
- 일반적인 대사
- 회말이라는 이유만의 훅
- 장르 관습상 그럴듯하지만 원문 근거가 약한 복선
- 회차당 수량을 맞추기 위한 후보

### 15.3 살아 있는 후보 원장

Stage03 동안 내부 상태를 관리한다.

```text
OPEN
→ TARGET_FOUND
→ PROMOTE / REJECT / RECLASSIFY
```

이는 Stage04 판단을 자동화하지 않고 나중에 원본을 다시 찾기 위한 색인이다.

---

## 16. 회차별 경량 게이트

각 회차 종료 직후 검사한다.

```text
파일 저장 여부
JSON/JSONL 파싱
exact key 존재
ID 형식·중복
SceneCard ordinal 1..N
Stage02 coverage·partition·count·runtime
EpisodeArc count·turning point 참조
CharacterArc trigger participant
RelationshipArc 양쪽 participant
LocalEdge 동일 회차·scene 참조
PayoffCandidate scene 참조
placeholder·가시적 템플릿·명백한 반복
SourceLock progress
next pointer
```

회차 경량 게이트는 전체 의미 품질을 확정하는 것이 아니라 손상을 조기에 차단한다.

---

## 17. 약 8회차 블록 강검증

권장 블록:

```text
16회: 1~8 / 9~16
20회: 1~8 / 9~16 / 17~20
24회: 1~8 / 9~16 / 17~24
31회: 1~8 / 9~16 / 17~24 / 25~31
54회: 1~8 / 9~16 / 17~24 / 25~32 / 33~40 / 41~48 / 49~54
```

블록 종료 시:

- exact keyset·enum·FK
- Stage01↔02↔03 참조
- 시퀀스 density·core_mix
- 정확 중복·마스킹 골격 반복
- CharacterArc 인물명 정합성
- RelationshipArc unordered pair 중복
- LocalEdge 과밀·인접 편향
- ID 전역성
- 후보 원장 진행 상태
- SourceLock·checkpoint 해시

오류가 난 회차·필드만 다시 읽는다.

---

## 18. 전 시즌 Stage01~03 강검증

Stage04로 이동하기 전에 전 작품을 하나의 validator와 수동 의미 감사로 검사한다.

### 18.1 구조 게이트

- SourceLock 장면 수와 Stage01 일치
- SceneCard9·EpisodeMeta5·Sequence18·EpisodeArc13
- coverage·partition·runtime·density·core_mix
- act tiling·turning point FK
- CharacterArc8·RelationshipArc9
- Edge12·Payoff7
- ID 전역 고유
- 회차 간 LocalEdge 0

### 18.2 내용 게이트

- SceneCard 내용 깊이 표본
- 원본 행동·정보·선택과 의미 일치
- 앙상블 실제 변화 누락 감사
- 변화 없는 인물·관계 수량 채우기 탐지
- LocalEdge 구체 인과
- 반복 evidence·동일 skeleton
- placeholder·Python 의미 생성 흔적 0

blocking error가 하나라도 있으면 Stage04를 시작하지 않는다.

---

## 19. Stage04 — 후보 100% 전수 처분

전 회차 Stage01~03가 잠긴 뒤 별도 실행한다.

```text
모든 PayoffCandidate 목록화
→ 각 후보 원 장면 재확인
→ 후속 회차의 실제 회수·변형·반향 장면 확인
→ 양쪽 장면 의미 대조
→ 후보별 disposition 기록
→ 검증된 연결만 CrossEpisodeEdge
→ FullSeriesArc 재종합
```

### 19.1 허용 disposition

```text
PROMOTED_CROSS_EDGE
RECLASSIFIED_LOCAL_OR_ADJACENT_CAUSAL
RESOLVED_WITHIN_EPISODE
REJECTED_DUPLICATE
REJECTED_INSUFFICIENT_EVIDENCE
REJECTED_SOURCE_MISMATCH
```

```text
미처리 후보 = 0
```

한 건이라도 미처리면 Stage04 완료가 아니다.

---

## 20. CrossEpisodeEdge

LocalEdge와 같은 exact 12키를 사용하되 다음을 만족한다.

```text
tgt_episode_no > src_episode_no
gap_episodes == tgt_episode_no - src_episode_no
edge_type ∈ {callback, plant_payoff, subplot_counterpoint}
source/target scene exists
label == target SceneCard.core
```

### 20.1 금지

- 이전 회차 마지막 장면 → 다음 회차 첫 장면 자동 브리지
- 멀리 떨어졌다는 이유만으로 복선·회수 판정
- 모든 후보 일괄 승격
- 동일 note·review 문장 복사
- 단순 분위기·주제 유사성을 인과로 기록

---

## 21. FullSeriesArc

exact 17키다.

```text
series, episodes_total, scenes_total, sequences_total,
logline, central_dramatic_question, theme_statement,
protagonist, antagonist, season_structure,
macro_turning_points, resolution, open_ending,
tone, conflict_persist, series_core_dist, by
```

다음을 실제 Stage01~04에서 재계산·재종합한다.

- 전체 counts
- 중심 질문과 답의 변화
- 주인공 want→need 또는 파국 경로
- 대립축의 변화
- 관계·권력·정보의 장기 방향
- 주요 plant/payoff·callback
- macro turning point
- 해결과 잔여 갈등

기계적인 `setup → expansion → reversal → closure` 4등분을 강제하지 않는다.

---

## 22. 검증 게이트 0~6

```text
Gate 0 — Source Integrity
Gate 1 — Quarter Direct-Reading Integrity
Gate 2 — Stage01/02 Structural Integrity
Gate 3 — Stage01/03 Semantic Grounding
Gate 4 — EXT6 Contract (기본 비활성)
Gate 5 — Stage04 Full-Series Fan-in
Gate 6 — Package, Lineage, Release
```

### Gate 0

- archive/file SHA256
- 인코딩·회차 파일 존재
- canonical ordinal
- scene boundary·alignment
- SourceLock PASS

### Gate 1

- `direct_reading_completed=true`
- `python_semantic_generation=false`
- placeholder 0
- QuarterAudit 동시대 생성
- 다음 Quarter 전에 저장·잠금

### Gate 2

- SceneCard9·EpisodeMeta5·Sequence18
- coverage·partition·count·runtime·density
- CORE·turn registry·core_mix

### Gate 3

- EpisodeArc13
- CharacterArc8 trigger participant
- RelationshipArc9 양쪽 participant
- 앙상블 coverage 감사
- LocalEdge 동일 회차·구체 인과
- PayoffCandidate 참조·enum
- 반복·템플릿·환각 0

### Gate 4

EXT6/HXT6은 기본 비활성이다. 기존 pilot·audit은 보존하되 신규 분석 완료 조건에 포함하지 않는다.

### Gate 5

- 후보 disposition 100%
- CrossEpisodeEdge12
- 자동 회차 경계 브리지 0
- FullSeriesArc17 counts·span 일치

### Gate 6

- manifest
- SHA256SUMS
- ZIP integrity
- SourceLock·QuarterAudit·validation·lineage
- raw source·secret·임시 Python 제외
- fresh extraction 실제 CLI 재실행

---

## 23. 계보·격리·교정

### 23.1 덮어쓰기 금지

```text
source → run → validation → checkpoint → comparison → promotion
```

GPT·Claude·다른 모델 run은 서로 다른 `run_id`를 사용한다. 자동 union·평균·부분 혼합으로 정본을 만들지 않는다.

### 23.2 즉시 quarantine 조건

- Python 의미 생성
- keyword/template artifact
- 잘못된 scene boundary
- source mismatch
- Stage01 내용 FAIL
- Stage02 coverage FAIL
- 허위 Character/Relationship/Edge/Payoff

### 23.3 supersession 기록

```text
old_run_id / old_sha256
new_run_id / new_sha256
reason
semantic_text_changed
correction_ledger
```

SceneCard는 한 판본, Stage03·04는 다른 ordinal 판본처럼 혼합하지 않는다.

---

## 24. 작품 패키지 구조

권장 독립 작품 패키지:

```text
README.md
PACKAGE_MANIFEST.json
source_lock/
quarter_audits/
authored/
authored_seq/
authored_arc/
authored_chararc/
authored_relarc/
authored_edges/
validation/
reports/
lineage/
SHA256SUMS.txt
```

전체 DB 편입 시 Governance 구조:

```text
seqcard_ko/                              의미 데이터·원본·SourceLock
tools/current/                           현행 범용 검증기
tools/history/                           역사 도구
validation/current/                      단일 최신 전역 결과
validation/works/{작품}/current.json     작품별 current 증빙
validation/history/                      구버전·component 증빙
upgrade_audit/                            이전 판본·교정·migration
provenance/                               입수·변환 이력
release_state/                            상태 전이·checkpoint
```

---

## 25. 전체 DB 편입 절차

```text
1. 독립 작품 fresh extraction PASS
2. 작품 파일을 staging에 삽입
3. 파일명·work_id·episode_no 정규화
4. SceneCard ordinal lineage 일치 확인
5. Edge·Candidate ID 전역 중복 검사
6. source_lock current/registry 갱신
7. validation works/registry 갱신
8. _ALL_series_arc 재집계
9. 완료·잔여 작품 수 갱신
10. tools/current 전체 DB validator 실행
11. manifest·SHA256SUMS 생성
12. ZIP 생성
13. 별도 디렉터리 fresh extraction
14. 실제 CLI 재실행
15. pre/post 파일 수·해시·한글 경로 비교
16. PASS_CANDIDATE 보고
```

---

## 26. 실패 신호

다음 신호가 보이면 포장 무결성과 의미 품질을 분리 판정한다.

- 모든 Sequence가 같은 공식 문형
- goal·obstacle의 고유 문장이 극소수
- EpisodeArc가 매회 같은 수학적 비율
- CharacterArc·RelationshipArc가 회차 요약 복사
- 회차마다 Arc·Edge·Candidate 수가 정확히 동일
- LocalEdge가 자동 first→last 또는 next-scene 사슬
- 회차 간 LocalEdge 존재
- disposition 이유가 후보 description 복사
- 모든 후보 승격 또는 모든 후보 거절
- QuarterAudit가 완성본 이후 일괄 생성
- SourceLock 해시가 SceneCard JSON 해시와 동일
- Python 파일이 core data 폴더에 남아 있음
- ZIP은 PASS지만 원본·의미 증거가 없음

---

## 27. 최종 릴리스 체크리스트

```text
[ ] original_extracted/{작품명}/ UTF-8 원본 완비
[ ] SourceLock 이중 해시 PASS
[ ] Q1→Q4 동시대 QuarterAudit
[ ] SceneCard exact 9
[ ] EpisodeMeta exact 5
[ ] SequenceBlueprint exact 18
[ ] coverage·partition·runtime·density PASS
[ ] EpisodeArc exact 13
[ ] CharacterArc ensemble coverage audited
[ ] RelationshipArc ensemble coverage audited
[ ] 변화 없는 Arc 수량 채우기 0
[ ] LocalEdge cross-episode 0
[ ] LocalEdge adjacency auto-generation false
[ ] LocalEdge 과밀 트리거 수동 감사 완료
[ ] PayoffCandidate disposition 100%
[ ] CrossEpisodeEdge automatic boundary bridge 0
[ ] FullSeriesArc exact 17·counts 일치
[ ] exact duplicate·masked skeleton threshold PASS
[ ] Python semantic generation false
[ ] errors 0 / blocking warnings 0
[ ] lineage·supersession·quarantine 정리
[ ] SHA256SUMS PASS
[ ] ZIP CRC PASS
[ ] fresh extraction actual CLI PASS
[ ] 사용자 승인 전 PASS_CANDIDATE
```

---

## 28. 새 대화창 복사용 실행 지시문

```text
GitHub 저장소 limsanghyuk/v1700-literary-os의 현재 드라마 분석 권위 브랜치에서
다음 문서를 순서대로 읽어라.

1. docs/drama_analysis/README.md
2. docs/drama_analysis/DRAMA_NEW_WORK_ANALYSIS_MASTER_RUNBOOK_V2.md
3. docs/drama_analysis/SCHEMA_CONTRACTS_V2.md
4. docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json

새로 분석할 드라마 한 작품을 선택하고, 먼저 원본 파일을
seqcard_ko/original_extracted/{작품명}/에 UTF-8 TXT로 저장하라.
회차 수·중복·누락·인코딩을 감사하고 original_bytes_sha256과
canonical_storage_sha256을 구분한 SourceLock을 작성하라.

한 회차를 Q1→Q2→Q3→Q4로 직접 읽어 Stage01을 저작하고,
회차 전체를 다시 보아 SequenceBlueprint·EpisodeArc를 작성하라.
Stage03에서는 클로드식 장점인 회차별 앙상블 인물·관계 추적 폭을 채택하라.
주인공뿐 아니라 조직·가족·팀·경쟁 진영의 실제 변화 인물과 관계를 폭넓게 스캔하되,
단순 등장·변화 없는 인물·관계·고정 수량 채우기는 금지하라.

LocalEdge는 동일 회차의 구체적 causal 연결만 허용하고,
장면 번호 인접성·같은 시퀀스·유사 주제를 근거로 자동 연결하지 마라.
회차 간 연결은 LocalEdge에 저장하지 말고, 작품 전 시즌 종료 후
Stage04에서 검증된 CrossEpisodeEdge로만 확정하라.

모든 PayoffCandidate를 후보 원장에 기록하고 Stage04에서 개별 disposition하라.
미처리 후보는 0이어야 하며, 이전 회차 마지막 장면과 다음 회차 첫 장면을
자동 브리지하지 마라.

Python은 원본 추출·정렬·해시·검증·직렬화·패키징에만 사용하고
SceneCard·Sequence·Arc·Edge·Payoff·FullSeriesArc 의미를 생성하지 마라.

회차 경량 게이트, 약 8회차 블록 강검증, 전 시즌 Stage01~03 강검증을 분리하라.
Stage04 완료 후 독립 작품 ZIP을 만들고 fresh extraction에서 실제 CLI를 재실행하라.
전체 DB 편입 후에도 registry·SourceLock·manifest·SHA256·ZIP·fresh extraction을 다시 검증하라.
사용자 명시 승인 전에는 PASS_CANDIDATE, 승인 후에만 CANONICAL을 사용하라.
EXT6/HXT6은 별도 승인 전까지 비활성 상태로 보존하라.
```

---

## 29. 최종 원칙

```text
원본은 직접 읽는다.
앙상블 폭은 넓게 스캔한다.
Arc는 실제 변화만 기록한다.
LocalEdge는 인과가 아닌 것을 제거한다.
인접성은 인과 근거가 아니다.
회차 간 연결은 Stage04에서만 확정한다.
모든 후보는 전수 처분한다.
수량은 품질 목표가 아니다.
형식과 의미를 각각 검증한다.
실제 파일과 실제 CLI 결과가 완료 문장보다 우선한다.
사용자 승인 전에는 CANONICAL로 승격하지 않는다.
```
