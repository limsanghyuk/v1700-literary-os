# 새 대화창 드라마 분석 즉시 실행 가이드 v1

- Document ID: `DRAMA-NEW-CONVERSATION-EXECUTION-GUIDE-V1`
- Status: `AUTHORITATIVE_CANDIDATE`
- Date: 2026-07-15
- Scope: 신규 드라마 분석 및 기존 작품 Stage01~04 업그레이드
- Exact schema authority: `SCHEMA_CONTRACTS_V2.md`
- EXT6: 기본 비활성

## 0. 목적

이 문서는 새 대화창·새 모델·새 실행 환경이 과거 대화 전체와 프로젝트 소스 전부를 다시 조사하지 않고도 드라마 한 작품을 선택하여 다음 작업을 즉시 수행하도록 만든 실행용 통합 설명서다.

```text
원본 확인
→ SourceLock
→ 회차별 Q1~Q4 직접독해
→ Stage01
→ Stage02
→ Stage03 앙상블 인물·관계 추적
→ 작품 전체 Stage01~03 강검증
→ Stage04 후보 전수 처분
→ FullSeriesArc
→ 독립 작품 ZIP
→ seqcard_ko 전체 DB 갱신
```

이 문서는 기존 권위 문서를 폐기하거나 exact schema를 변경하지 않는다. 세부 키셋·자료형·enum·ID·FK가 충돌하면 항상 `SCHEMA_CONTRACTS_V2.md`를 따른다.

## 1. 새 대화창의 최소 필독 세트

새 대화창은 다음 네 문서를 순서대로 읽으면 작업을 시작할 수 있다.

1. `docs/drama_analysis/README.md`
2. `docs/drama_analysis/DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md`
3. `docs/drama_analysis/SCHEMA_CONTRACTS_V2.md`
4. `docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json`

다음 문서는 충돌 해결·정밀 검증·중단 복구가 필요할 때 읽는다.

- `DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md`
- `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md`
- `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md`
- `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md`
- `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md`
- `DRAMA_SESSION_EXECUTION_SAFETY_V1.md`

따라서 프로젝트 전체 소스, 과거 세션, 모든 산출물, 흩어진 역사 문서를 매번 전수 조사할 필요는 없다.

## 2. 권위와 충돌 해결

```text
1. SCHEMA_CONTRACTS_V2
2. CURRENT_OPERATING_SUPPLEMENT
3. 이 실행 가이드
4. ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY
5. CLOSE_READING_MASTER_PROTOCOL
6. VALIDATION_AND_RELEASE_GATES
7. LINEAGE_PACKAGE_HANDOFF
8. SESSION_EXECUTION_SAFETY
9. DATABASE_STATUS
10. 최신 세션 README
```

이 가이드는 실행 절차를 통합하지만 exact schema를 재정의하지 않는다.

## 3. 작업 시작 전 작품 분류

원본과 기존 데이터를 감사한 뒤 작품을 다음 중 하나로 분류한다.

### 3.1 `NEW_ANALYSIS`

- 원본은 있으나 Stage01~04가 없음
- 회차별 직접독해부터 시작

### 3.2 `NORMAL_UPGRADE`

- Stage01·02가 원본에 밀착됨
- 현행 keyset·enum·ID 정규화 후 Stage03·04 보완 가능

### 3.3 `STAGE02_REAUTHOR_REQUIRED`

다음 중 하나가 있으면 기존 시퀀스 경계는 검토하되 의미 필드를 전면 재저작한다.

- 반복 골격 집중
- 미래 회차 내용이 앞 회차에 밀려 들어감
- goal·obstacle·value_shift가 원본과 불일치
- POV·장소·turn이 실제 시퀀스와 불일치

### 3.4 `SOURCE_HOLD`

- 회차 원본 누락
- 중복 판본
- 회차 번호 위장
- 원본과 Stage01 장면 수를 잠글 수 없음

`SOURCE_HOLD` 작품은 추정·줄거리·창작으로 채우지 않는다.

### 3.5 `LONG_FORM_BLOCKED_PLAN`

30회 이상 장편은 8회차 블록으로 계획하되 실제 의미 저작과 잠금은 한 회차씩 수행한다.

## 4. 원본·SourceLock preflight

Stage01을 시작하기 전에 반드시 다음을 확인한다.

1. 작품별 회차 파일 존재
2. 파일명과 실제 회차 일치
3. 인코딩과 텍스트 추출 가능 여부
4. 중복 판본·누락 판본
5. 물리 장면 마커와 논리 장면 경계
6. canonical `scene_no=1..N`
7. 기존 SceneCard와 회차별 장면 수 대응
8. 원본 및 정규화본 SHA256
9. quarter 범위
10. 다음 재개 지점

개발자용 로컬 데이터베이스에는 다음 경로로 원본을 보관할 수 있다.

```text
seqcard_ko/original_extracted/<work>/<work>_<NN>.txt
```

GitHub 허브에는 원본 대본·대사·raw text를 커밋하지 않는다.

## 5. 안전 작업 단위

```text
의미 독해 최소 단위 = quarter
원자 체크포인트 = 1 episode
개발자 전달 블록 = 8 episodes
Stage04 = full-series fan-in
```

한 실행에서 여러 회차를 한꺼번에 의미 생성하지 않는다.

회차 내부 순서:

```text
Q1 직접독해·Stage01·QuarterAudit
→ Q2
→ Q3
→ Q4
→ 회차 전체 Stage02
→ EpisodeMeta
→ Stage03
→ 회차 강검증
→ 체크포인트
```

## 6. Stage01 — SceneCard

정본은 정확히 9키다.

```text
work_id, scene_no, heading, title, intent_gist,
core, core2, skin, by
```

각 장면을 읽을 때 내부적으로 다음 여섯 질문에 답한다.

1. 실제 행동은 무엇인가.
2. 누가 어떤 전략을 사용하거나 무엇을 숨기는가.
3. 정보·오해·조건 중 무엇이 바뀌는가.
4. 누가 무엇을 선택·거부·유예하는가.
5. 이 장면이 회차 구조에서 왜 필요한가.
6. 어떤 잔여 동력이 다음 장면이나 시퀀스를 밀어내는가.

`title`은 장면의 고유 전환을 압축하고, `intent_gist`는 욕망·압력·변화를 구체적으로 기록한다.

금지:

- 키워드 조각
- 동일 문장 골격 반복
- 장면 요약을 여러 필드에 복사
- 원문에 없는 인물·감정·인과
- Python 또는 템플릿 의미 생성

## 7. EpisodeMeta

정확히 5키다.

```text
work_id, scene_count, core_dist, episode_function, by
```

`scene_count`와 `core_dist`는 실제 SceneCard에서 결정론적으로 재계산한다.

## 8. Stage02 — SequenceBlueprint

정확히 18키다.

```text
seq_id, work_id, episode_no, seq_index,
member_scene_nos, scene_span, scene_budget,
sequence_intent, goal, obstacle, value_shift,
turn_type, turn_class, core_mix, pov_char,
place_cluster, runtime_share, by
```

시퀀스는 장면 수 균등분할이 아니라 다음 변화에서 나눈다.

- 목표 주체 또는 목표 변화
- 장애 성격 변화
- 정보·관계·권력 가치 전환
- 새로운 극적 행동 단위 시작

필수 불변식:

```text
모든 장면이 정확히 하나의 sequence에 포함
중복 0 / 누락 0
sum(scene_budget) == scene_count
runtime_share sum == 1.0 ± 1e-6
core_mix는 실제 member SceneCard의 core/core2만 사용
sequence_count / scene_count >= 0.11
```

기존 Stage02가 반복 오염 상태면 형식 정규화만 하지 말고 원본·SceneCard를 다시 읽어 의미 필드를 재저작한다.

## 9. EpisodeArc

정확히 13키다.

```text
work_id, episode_no, scene_count, sequence_count,
dramatic_question, act_structure, entry_state, exit_state,
turning_point, central_conflict_axis, episode_function,
core_dist, by
```

- 실제 시퀀스 전환을 근거로 한다.
- 모든 시퀀스를 act가 gap·overlap 없이 덮는다.
- 기계적으로 4막을 강제하지 않는다.
- `turning_point.seq_index`는 실제 시퀀스를 참조한다.

## 10. Stage03 — 앙상블 확장형 인물·관계 추적

클로드 분석의 장점인 **회차별 앙상블 인물·관계 추적 폭**을 현행 계약 안에서 채택한다.

### 10.1 회차별 앙상블 스캔

Stage03 저작 전 해당 회차의 다음 층을 모두 검토한다.

- 주인공·대립자
- 핵심 조력자·경쟁자
- 조직 내부 의사결정자
- 반대 진영의 기능 인물
- 반복 등장하는 실무자·가족·동료
- 이번 회차에서 관계의 방향을 바꾸는 단역

검토했다고 해서 모두 Arc로 생성하지 않는다. 실제 상태 변화나 관계 변화가 발생한 대상만 기록한다.

### 10.2 CharacterArc

정확히 8키다.

```text
work_id, character, episode_no, state_label,
state_delta, trigger_scene_no, by, evidence
```

기존의 주인공 2~3명만 기계적으로 추적하는 방식으로 제한하지 않는다. 앙상블·조직극에서는 실제 변화가 발생한 조연과 기능 인물도 포함한다.

그러나 다음은 금지한다.

- 단순 등장만으로 Arc 생성
- 회차별 고정 수량 채우기
- 같은 evidence 복사
- trigger 장면에 없는 인물

### 10.3 RelationshipArc

정확히 9키다.

```text
work_id, char_a, char_b, episode_no,
relation_state, relation_delta, trigger_scene_no,
evidence, by
```

주인공 관계만이 아니라 동맹·경쟁·상하·가족·조직·거래·은폐·공모 관계의 실제 변화를 폭넓게 검토한다.

- 양쪽 인물이 함께 등장하거나 직접 통화·교신해야 한다.
- `(A,B)`와 `(B,A)`를 중복 생성하지 않는다.
- 관계 상태와 이번 회차 변화량을 구분한다.
- 변화가 없는 관계를 수량 때문에 생성하지 않는다.

### 10.4 폭의 기준

레코드 수는 목표가 아니라 결과다.

```text
고정 최소치 없음
고정 최대치 없음
실제 변화 누락 금지
수량 채우기 금지
```

`싸인` 적용 사례의 회차당 CharacterArc 5건·RelationshipArc 4건은 앙상블 폭을 구현한 참고 사례일 뿐 모든 작품의 할당량이 아니다.

## 11. LocalEdge — 선별적 인과만 허용

정확히 12키이며 다음이 필수다.

```text
edge_type == causal
src_episode_no == tgt_episode_no
gap_episodes == 0
label == target SceneCard.core
```

### 11.1 인과 판정 질문

다음 질문에 구체적으로 답할 수 있어야 한다.

```text
source 장면의 행동·정보·선택이 없었다면
target 장면이 발생하지 않거나 실질적으로 달라졌는가?
```

답이 아니면 LocalEdge로 만들지 않는다.

### 11.2 금지

- 모든 장면을 다음 장면에 연결
- 번호 인접성을 인과로 간주
- 같은 시퀀스라는 이유로 연결
- 유사한 주제·감정을 연결
- 회차 간 연결을 LocalEdge에 저장
- LocalEdge 수량을 품질 목표로 사용

인접 장면 사이에도 직접 인과가 있을 수 있으나 **인접하다는 사실 자체는 근거가 아니다**.

### 11.3 반과밀 감사 트리거

다음은 자동 실패가 아니라 반드시 수동 재감사를 요구하는 경고 기준이다.

```text
LocalEdge / SceneCard > 0.10
또는
바로 다음 장면을 target으로 하는 LocalEdge 비율 > 0.50
```

회차 간 LocalEdge가 한 건이라도 있으면 blocking error다.

## 12. PayoffCandidate

정확히 7키다.

```text
candidate_id, work_id, episode_no, scene_no,
edge_type_guess, description, by
```

장거리 가능성을 후보로만 저장한다. 후속 회차 확인 전 CrossEpisodeEdge로 승격하지 않는다.

후보 수량을 늘리는 것이 목적이 아니다. 후속 회수 가능성이 있는 구체적 장면만 남긴다.

## 13. 작품 전체 Stage01~03 강검증

Stage04 전에 전 회차를 하나의 작품 validator로 검사한다.

필수:

- SourceLock 장면 수와 Stage01 일치
- exact keyset·type·enum
- Stage02 coverage·partition·runtime·density·core_mix
- EpisodeArc act tiling
- CharacterArc trigger participant
- RelationshipArc 양쪽 participant
- 앙상블의 실제 변화 누락 감사
- LocalEdge 동일 회차·구체 인과
- 회차 간 LocalEdge 0
- LocalEdge 과밀·인접 편향 감사
- PayoffCandidate 참조·enum
- ID 전역 고유
- 정확 중복·마스킹 골격 반복
- placeholder·Python 의미 생성 흔적 0

blocking error가 하나라도 있으면 Stage04로 이동하지 않는다.

## 14. Stage04 — 후보 전수 fan-in

작품 전 회차 Stage01~03가 잠긴 뒤 별도 실행으로 수행한다.

```text
모든 PayoffCandidate 목록화
→ 원 장면 재확인
→ 후속 실제 회수·변형·반향 확인
→ 후보별 disposition
→ 검증된 연결만 CrossEpisodeEdge
→ FullSeriesArc 재종합
```

허용 disposition:

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

한 건이라도 처분되지 않으면 Stage04 완료가 아니다.

## 15. CrossEpisodeEdge

LocalEdge와 같은 12키를 사용하되 다음 조건을 만족한다.

```text
tgt_episode_no > src_episode_no
gap_episodes == tgt_episode_no - src_episode_no
edge_type ∈ {callback, plant_payoff, subplot_counterpoint}
```

금지:

- 이전 회차 마지막 장면 → 다음 회차 첫 장면 자동 브리지
- 멀리 떨어졌다는 이유만으로 복선·회수 판정
- 후보 일괄 승격
- 동일 note·review 문장 복사

## 16. FullSeriesArc

정확히 17키다.

```text
series, episodes_total, scenes_total, sequences_total,
logline, central_dramatic_question, theme_statement,
protagonist, antagonist, season_structure,
macro_turning_points, resolution, open_ending,
tone, conflict_persist, series_core_dist, by
```

실제 매크로 전환·인물 변화·복선 회수 결과를 기준으로 재작성한다. 기존 FullSeriesArc가 존재해도 Stage03·04 변경 후 counts와 구조를 다시 계산한다.

## 17. Python 사용 경계

허용:

- ZIP 해제·인코딩
- 헤딩 탐지·ordinal
- SHA256·offset·line span
- JSON/JSONL 직렬화
- keyset·enum·coverage·FK·중복·반복 검증
- runtime·core_mix·ID 같은 결정론적 계약 교정
- manifest·checksum·ZIP

금지:

- SceneCard 의미 생성
- Sequence 의미 생성
- CharacterArc·RelationshipArc 생성
- LocalEdge·Payoff·CrossEdge 판단
- 후보 disposition 자동화
- FullSeriesArc 의미 생성

## 18. 패키지와 데이터베이스 통합

독립 작품 패키지 최소 구조:

```text
README.md
authored/
authored_seq/
authored_arc/
authored_chararc/
authored_relarc/
authored_edges/
quarter_audits/
source_lock/
validation/
reports/
lineage/
FINAL_MANIFEST.json
SHA256SUMS.txt
```

통합 후 반드시 수행한다.

1. 작품 파일 삽입
2. 파일명·work_id·episode_no 정규화
3. Edge·Candidate ID 전역 중복 검사
4. `_ALL_series_arc.json` 재집계
5. 완료·잔여 작품 수 갱신
6. 전체 DB validator
7. ZIP CRC와 내부 SHA256
8. fresh extraction 재검증

## 19. 상태와 승격

```text
DRAFT
QUARANTINE
PASS_CANDIDATE
CANONICAL
SUPERSEDED
SOURCE_HOLD
```

- 검증 통과·사용자 승인 전: `PASS_CANDIDATE`
- 검증 통과·사용자 명시 승인 후: `CANONICAL`
- 원본 결함: `SOURCE_HOLD`
- 의미 오염: `QUARANTINE` 또는 재저작

## 20. 최종 릴리스 체크리스트

```text
SourceLock PASS
Stage01 exact 9 keys
EpisodeMeta exact 5 keys
Stage02 exact 18 keys
Stage02 coverage/partition errors 0
EpisodeArc exact 13 keys
CharacterArc ensemble coverage audited
RelationshipArc ensemble coverage audited
LocalEdge cross-episode count 0
LocalEdge automatic adjacency generation false
PayoffCandidate disposition 100%
CrossEpisodeEdge automatic boundary bridge 0
FullSeriesArc counts match
semantic exact duplicates 0 above justified exception
masked skeleton gaming 0 above threshold
errors 0
blocking warnings 0
ZIP CRC PASS
SHA256SUMS PASS
fresh extraction PASS
```

## 21. 새 대화창 복사용 실행 지시문

```text
GitHub 저장소 limsanghyuk/v1700-literary-os의 현재 드라마 분석 권위 브랜치에서
다음 문서를 순서대로 읽어라.

1. docs/drama_analysis/README.md
2. docs/drama_analysis/DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md
3. docs/drama_analysis/SCHEMA_CONTRACTS_V2.md
4. docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json

현재 상태 JSON에서 완료 작품을 제외하고 작품 한 편을 선정하라.
원본 inventory와 SourceLock을 먼저 만들고, 한 회차를 Q1→Q4로 직접 읽어
Stage01→Stage02→Stage03을 저작·검증·영속화한 뒤 다음 회차로 이동하라.

Stage03에서는 주인공만이 아니라 실제 변화가 있는 앙상블 인물과 관계를 폭넓게 추적하라.
다만 수량을 채우지 말고 실제 변화만 기록하라.
LocalEdge는 동일 회차의 구체 인과만 선별하고 장면 인접성을 자동 연결하지 마라.
모든 PayoffCandidate를 Stage04에서 개별 처분하고 미처리 후보를 0으로 만들어라.
EXT6은 적용하지 마라.
Python은 추출·정규화·검증·패키징에만 사용하라.

전 회차 Stage01~03 강검증 후 Stage04 fan-in을 수행하고,
독립 작품 ZIP과 갱신된 seqcard_ko 전체 DB ZIP을 생성하라.
사용자 승인 전에는 PASS_CANDIDATE, 승인 후에만 CANONICAL을 사용하라.
```

## 22. 현재 참조 사례

- 의미 깊이·Stage04·계보 기준: `킬미힐미`
- 앙상블 인물·관계 폭의 장점: `스토브리그`의 분석 범위
- 현행 계약 안에서 앙상블 폭을 적용한 사례: `싸인`

스토브리그의 과도한 LocalEdge, 인접 연결 편향, 회차 간 LocalEdge, 미처리 후보 방식은 채택하지 않는다.
