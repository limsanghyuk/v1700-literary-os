# 한국 드라마 분석 — Sequence Boundary 판정·보강 실행 설명서 R1

**문서 ID**: `DRAMA_ANALYSIS_SEQUENCE_BOUNDARY_HANDOFF_MANUAL_R1_20260817`  
**상태**: `OPERATIONAL_HANDOFF / EXPERIMENTAL_BOUNDARY_STANDARD / NO_V10_1_SCHEMA_CHANGE`  
**적용 대상**: 현재 다른 GPT 세션에서 진행 중인 신규/보강 작품 분석 + 기존 34 CANONICAL THICK 작품의 Sequence Boundary 보강  
**현재 정본 전제**: 98작 Stage01~04 / 97작 V10.1-equivalent / 1 SOURCE_HOLD / 34 CANONICAL THICK / Release family V9  
**중요**: 본 문서는 Sequence 경계 문제를 다루기 위한 실행 설명서이며, 현행 V10.1의 Stage01~04 exact schema를 임의로 변경하지 않는다.

---

## 0. 다른 GPT 세션이 가장 먼저 읽어야 할 한 페이지

### 목적
우리가 지금 고치려는 것은 **Sequence의 내용 자체가 아니라, “어디서 하나의 Sequence가 끝나고 다음 Sequence가 시작되는가”라는 경계의 정당성**이다.

기존 DB는 Scene을 빠뜨리거나 겹치게 나눈 구조적 문제는 거의 없다. 최신 전수조사에서 98작·1,814회·114,371 SceneCard·16,125 Sequence의 partition 구조는 gap/overlap/중복 오류가 0이었다. 그러나 현재 Stage02 SequenceBlueprint에는 `member_scene_nos`, goal, obstacle, value_shift, turn 등은 있지만 **왜 바로 그 Scene 뒤가 경계인지 설명하는 공식 필드가 없다.**

따라서 앞으로의 분석은 다음 원칙을 따른다.

1. **현재 진행 중인 신규 작품을 멈추고 처음부터 다시 분석하지 않는다.**
2. Stage01 직접독해는 기존 V10.1 방식 그대로 진행한다.
3. **Stage02에서 Sequence를 묶을 때부터 본 설명서의 경계 규칙을 적용한다.**
4. 이미 Stage02가 끝난 작품은 THICK 전에 `Sequence Boundary Integrity`를 삽입한다.
5. 기존 34 THICK 작품은 별도 보강 트랙에서 경계를 검증한다.
6. 나머지 63작은 전면 재검하지 않고 **향후 THICK 승격 시 경계 검증을 함께 수행**한다.
7. THICK/R5/R8가 Stage02의 `member_scene_nos`를 조용히 바꾸는 것은 금지한다.
8. 경계를 바꾸어야 할 경우 **SOURCE → Stage02 → Stage03/04 영향검사 → THICK → R5/R8** 순서로 단일 truth를 다시 연결한다.
9. 장면 수를 비슷하게 맞추기 위한 등분은 금지한다. 작품별 평균 Sequence 수는 `prior`일 뿐 quota가 아니다.
10. 현재 경계 표준 R1은 실험적이므로 기존 V10.1 18-key SequenceBlueprint에 새 필드를 강제로 넣지 않는다. 경계 증거는 별도 append-only `SequenceBoundaryEvidenceR1`에 기록한다.

---

# 1. 왜 이 설명서가 필요한가

우리의 단기 목적은 완성 드라마를 설명하는 것이 아니라, 분석 DB를 통해 Literary OS가 나중에 스스로 다음을 하게 만드는 것이다.

- Sequence 기획
- Sequence 구성
- Sequence 구조화
- Sequence 설계
- Sequence 창조
- 여러 Sequence를 선택·배열하여 Episode Synopsis 설계

이 목적에서 가장 위험한 것은 **Sequence 내부 내용은 깊게 분석했지만 Sequence 단위 자체가 불안정한 상태**다.

THICK가 깊다고 경계가 맞다는 뜻은 아니다. THICK는 주어진 `member_scene_nos`를 바탕으로 목표·갈등·정보·관계·payoff를 깊게 설명할 수 있지만, 그 membership 자체가 올바른지는 별도의 문제다.

실제 전수조사에서도 Stage02와 THICK가 서로 다른 Sequence membership을 가진 legacy 작품이 발견되었다.

- `경성스캔들`: Stage02 150 Sequence / THICK 138 Sequence
- `개와늑대의시간`: Stage02 143 Sequence / THICK 132 Sequence

이 두 작품은 최근 손상이 아니라 과거 THICK 정본화 과정에서 문서화되지 않은 별도 segmentation이 생긴 것으로 확인됐다. 따라서 앞으로는 **한 작품에 하나의 Sequence Boundary Truth만 존재**하도록 해야 한다.

---

# 2. Sequence의 공식 작업 정의 R1

> **Sequence는 하나의 지배적 극적 거래(dominant dramatic transaction)가 진행되는 최소 연속 Scene 묶음이다.**

하나의 극적 거래에는 다음이 있어야 한다.

1. **입구 행동 전제** — 누가 움직이는가, 무엇을 원하는가, 무엇을 알고/믿는가, 무엇이 제약하는가.
2. **지배적 Local Dramatic Question** — 이 묶음에서 해결·변형되어야 하는 핵심 질문 하나.
3. **행동과 저항** — 인물의 시도와 그것을 방해하는 힘.
4. **결제 또는 재지향** — 성공·실패·유예·정보 획득·관계 변화·권력 변화·결심 등.
5. **다음 행동 전제의 변화** — 결과 때문에 이후 Scene들이 다른 질문·목표·제약으로 움직이기 시작함.

### Sequence가 끝나는 지점

Sequence는 **현재 지배적 거래가 충분히 결제 또는 재지향되고, 다음 Scene부터 다른 지배적 거래가 시작되는 가장 이른 타당한 지점**에서 끝난다.

### 중요한 원칙

- Scene 수는 정의가 아니다.
- 1 Scene도 완전한 거래를 수행하면 Sequence가 될 수 있다.
- 20 Scene 이상이어도 하나의 지배적 거래가 유지되면 한 Sequence일 수 있다.
- 장소가 바뀌었다고 자동으로 Sequence가 바뀌지 않는다.
- 광고 브레이크나 비슷한 길이에 맞추지 않는다.

---

# 3. 경계를 판정할 때 보는 8개 상태 차원

Sequence의 경계는 단순 장소 변화가 아니라 **이후 행동의 전제를 바꾸는 상태 변화**로 설명해야 한다.

| 코드 | 상태 차원 | 질문 |
|---|---|---|
| G | Goal / Attempt | 목표·시도가 성공, 실패, 유예, 재정의되었는가? |
| K | Knowledge Premise | 새 정보가 이후 행동의 전제를 실제로 바꾸는가? |
| R | Relationship / Affiliation | 신뢰·결속·단절·공개/비공개 관계 상태가 바뀌는가? |
| P | Power / Control | 주도권·협상력·통제권·권한이 바뀌는가? |
| C | Constraint / Risk | 위협·규칙·기한·자원·외부 조건이 바뀌는가? |
| M | Commitment / Decision | 선택·결심이 구속력을 갖거나 기존 결정을 철회하는가? |
| W | World / Time Regime | 시간·공간 도약 자체가 새 행동 전제를 만드는가? |
| L | Plot-line Handoff | 단순 교차편집이 아니라 다른 plot의 지속적 거래로 넘어가는가? |

**주의**: 장소/시간 heading 변화만으로는 경계 근거가 되지 않는다. 전수 실측에서 heading change는 canonical boundary와 Sequence 내부에서 거의 비슷하게 발생해 판별력이 거의 없었다.

---

# 4. Boundary Reason Code B1~B7

경계에는 최소 하나의 **primary reason**을 부여한다.

| 코드 | 이름 | 의미 |
|---|---|---|
| B1 | GOAL_SETTLEMENT | 목표·시도가 성공/실패/유예/재정의로 결제 |
| B2 | KNOWLEDGE_PREMISE_SHIFT | 새 정보 때문에 이후 행동 전제가 변화 |
| B3 | RELATIONSHIP_OR_COMMITMENT_SHIFT | 관계 또는 결심 상태가 변화 |
| B4 | POWER_OR_CONSTRAINT_SHIFT | 주도권·권력·위험·제약 조건이 변화 |
| B5 | WORLD_REGIME_SHIFT | 시간·공간·환경 변화가 실제로 새로운 국면을 만듦 |
| B6 | PLOT_LINE_HANDOFF | 지속적인 다른 plot 거래로 전환 |
| B7 | COMPOUND_TERMINAL | B1~B6 중 둘 이상이 함께 강하게 종결 |

Secondary code는 허용하지만, **왜 이 지점이 경계인지 primary code 하나는 명확해야 한다.**

---

# 5. 가장 중요한 판정법 — Two-Sided Boundary Test

Scene N 뒤를 경계 후보로 잡았다면 다음을 반드시 검사한다.

## 5.1 LEFT TERMINAL

Scene N까지의 왼쪽 Sequence에서 다음 중 하나 이상이 **결제·변형·재지향**되었는가?

- G 목표
- K 정보
- R 관계
- P 권력/주도권
- C 제약/위험
- M 결심
- W 세계/시간 국면
- L plot-line

“아직 같은 질문을 그대로 계속하고 있다”면 경계가 아닐 가능성이 높다.

## 5.2 RIGHT RESET

Scene N+1부터 다음 중 하나가 새로 활성화되는가?

- 새로운 local dramatic question
- 새로운 owner 또는 주도 인물
- 새로운 목표/시도
- 새로운 제약/위험
- 새로운 정보 전제
- 지속적인 다른 plot-line

오른쪽 Scene이 단순히 같은 거래의 다음 단계라면 경계를 의심한다.

## 5.3 MINIMALITY — ±1 Scene Challenge

경계를 한 Scene 앞/뒤로 옮겨본다.

- Scene N을 오른쪽으로 넘기면 왼쪽 거래가 미완성되는가?
- Scene N+1을 왼쪽으로 넣으면 왼쪽에 두 개의 지배 거래가 섞이는가?
- N-1 / N / N+1 중 N이 가장 자연스럽게 거래를 분리하는가?

**정확히 같은 거래인데 장면 수를 맞추기 위해 N에서 잘랐다면 MERGE_CANDIDATE다.**

---

# 6. Granularity — 너무 잘게 또는 너무 크게 나누지 않는 법

## 금지되는 기계 규칙

- “Sequence는 최소 2씬” → hard rule 금지
- “Sequence는 7씬 정도여야 한다” → 금지
- “회차당 8개여야 한다” → 금지
- “turn은 반드시 후반 1/3” → 금지
- “장소가 바뀌면 경계” → 금지

현재 DB 실측은 median 7 Scene/Sequence, 회차당 median 8 Sequence지만 이것은 **reference distribution**일 뿐이다.

## 지배적 settlement 원칙

한 Sequence에는 **하나의 지배적 settlement**가 있어야 한다.

하위 관계·정보·감정 변화 여러 개가 같이 있어도 괜찮다. 단, 서로 독립적인 두 개의 거래가 각각 결제된다면 SPLIT을 검토한다.

## Singleton Sequence

1 Scene Sequence는 자동 FAIL이 아니다.

다음처럼 한 Scene만으로 독립 transaction이 완결될 수 있다.

- 회차 종결 반전
- 공개 선언
- 죽음/체포/결별
- 구속력 있는 결심
- cliffhanger를 만드는 결정적 reveal

단, 1 Scene Sequence는 반드시 명확한 boundary evidence를 남긴다.

---

# 7. 작품별 Sequence 개수 k를 사용하는 법

기존 작품에는 작품 고유의 리듬이 있다.

전수조사에서 같은 작품의 다른 회차 `scene_count / k` 중앙값으로 현재 회차의 k를 예측했을 때:

- MAE 약 0.595
- 정확 적중 약 58.6%
- ±1 이내 약 88.8%

따라서 k는 유용하다. 그러나 **quota가 아니라 prior**로만 쓴다.

### 허용

> “이 작품은 보통 8~9 Sequence 리듬이므로 후보 설계의 prior로 참고한다.”

### 금지

> “원래 8개니까 이번 회차도 무조건 8개가 되도록 Scene을 자른다.”

Finale, midpoint, crisis episode 등은 작품 평균을 벗어날 수 있다.

---

# 8. 현재 진행 중인 신규 작품 분석 세션 적용법

## 경우 A — Stage01 진행 중

그대로 진행한다.

`SOURCE 직접독해 → SceneCard exact 9-key` 규격을 변경하지 않는다.

Stage02로 올라갈 때부터 본 경계 규칙을 적용한다.

## 경우 B — Stage02 저작 중

각 Sequence를 만들 때 다음 순서로 작성한다.

1. 이번 묶음의 local dramatic question을 한 문장으로 쓴다.
2. owner/cast와 goal/attempt를 정한다.
3. obstacle/resistance를 확인한다.
4. 입구 상태 G/K/R/P/C/M/W/L을 정리한다.
5. 사건 진행 후 terminal 상태를 정한다.
6. LEFT TERMINAL을 확인한다.
7. 다음 Scene의 RIGHT RESET을 확인한다.
8. ±1 minimality challenge를 수행한다.
9. Stage02 18-key SequenceBlueprint는 현행 V10.1 규격 그대로 저작한다.
10. 경계 근거는 별도 `SequenceBoundaryEvidenceR1`에 기록한다.

## 경우 C — Stage02가 이미 끝났고 Stage03~04 진행 중

현재 작업을 전부 폐기하지 않는다.

- 먼저 Stage02 partition 구조를 검사한다.
- 위험 경계를 SOURCE로 감사한다.
- 경계를 바꾸지 않는 경우 Stage03~04를 계속한다.
- 경계를 바꾸는 경우 해당 Episode의 Stage02부터 영향 계층을 재검한다.

## 경우 D — THICK 직전

THICK를 쓰기 전에 반드시:

1. Sequence Boundary Integrity 검사
2. Stage02 membership freeze
3. THICK가 동일 `member_scene_nos`를 사용하는지 확인

THICK에서 독자적으로 merge/split하지 않는다.

---

# 9. 기존 34 CANONICAL THICK 작품 보강 원칙

34작은 자율 Sequence/Episode 설계 연구에서 가장 깊게 사용할 학습 코퍼스이므로 우선 보강한다.

그러나 **34작 전부를 처음부터 재분석하지 않는다.** 다음 3단계로 처리한다.

## Phase A1 — 전 작품 결정론 Screening

34작 모두에 대해:

- partition integrity
- Sequence length CV
- equal-cut reproduction
- singleton 수
- value_shift quality signal
- Stage02↔THICK membership parity
- Stage02↔R5/R8 origin parity

를 검사한다.

## Phase A2 — SOURCE 직접감사

다음 순서로 직접 SOURCE를 읽는다.

1. `경성스캔들`, `개와늑대의시간` — legacy dual segmentation 최우선
2. 등분 관성 HIGH 회차
3. singleton/long-sequence/동일 value_shift 등 복합 경고 회차
4. MEDIUM/LOW에서도 층화 표본을 넣어 진단 편향 방지

## Phase A3 — 선택 보강

경계마다 아래 verdict를 부여한다.

- VALID
- NEARBY_VALID
- MERGE_CANDIDATE
- SPLIT_CANDIDATE
- REVIEW_REQUIRED

SOURCE가 실제 수정을 요구하는 경계만 고친다.

### 34작 상태 관리 권고

- `BOUNDARY_SCREENED_THICK`: 결정론 screening 완료
- `BOUNDARY_AUDITED_THICK`: SOURCE 표본/위험 경계 감사 완료
- `BOUNDARY_QUALIFIED_THICK`: 요구되는 경계 보강 + downstream parity + fresh validation 완료

이 상태명은 운영용이며, 사용자 승인 없이 V9 numeric release나 V10.1 schema version을 올리지 않는다.

---

# 10. 나머지 63작 처리 원칙

나머지 63작은 Sequence Boundary 문제만을 이유로 전면 재검하지 않는다.

향후 작품별로 THICK 보강할 때 다음을 하나의 승격 파이프라인으로 묶는다.

`기존 Stage01~04 확인`
→ `Sequence Boundary Screening`
→ `필요한 SOURCE 경계 감사/선택 수정`
→ `Stage02 membership freeze`
→ `THICK V3 저작`
→ `PlannerInput R5`
→ `Runtime R8`
→ `Stage02↔THICK↔R5↔R8 parity`
→ `Deep Semantic / Thread / Subplot / fresh extraction`
→ `CANONICAL`

즉 **Boundary 보강과 THICK 확대를 따로 하지 않는다.**

---

# 11. Existing Canonical Boundary를 감사하는 방법 — CT-12D 방식

기존 작품을 감사할 때 정본 경계를 먼저 보면 confirmation bias가 생긴다.

따라서 다음 순서를 지킨다.

1. SOURCE를 순서대로 읽는다.
2. canonical Sequence 파일을 열지 않은 상태에서 transaction closure 후보를 표시한다.
3. 후보 경계와 B-code를 freeze한다.
4. 그 후 canonical Stage02 경계를 연다.
5. 비교하고 verdict를 부여한다.

### Verdict 정의

**VALID**  
canonical 좌표가 같고 본 표준으로 충분히 설명된다.

**NEARBY_VALID**  
같은 transaction을 인식했으나 가장 자연스러운 경계가 ±1 Scene 차이난다.

**MERGE_CANDIDATE**  
canonical boundary가 하나의 계속되는 transaction을 인위적으로 둘로 자른다.

**SPLIT_CANDIDATE**  
canonical Sequence 안에 두 개 이상의 독립 dominant transaction이 존재한다.

**REVIEW_REQUIRED**  
SOURCE 자체가 복수 해석을 허용하고 근거가 충분히 모호하다.

---

# 12. SequenceBoundaryEvidenceR1 — 별도 증거 레코드

현재 V10.1 SequenceBlueprint 18-key를 변경하지 않는다.

경계 증거는 append-only sidecar로 기록한다.

필수 필드:

```text
work_id
episode_no
boundary_after_scene_no
left_seq_id
right_seq_id
primary_boundary_code
secondary_boundary_codes[]
state_dimensions_changed[]
left_terminal_summary
right_reset_summary
evidence_scene_nos[]
source_refs[]
minimality_minus1
minimality_plus1
verdict
confidence
by
```

### 기록 예시

```json
{
  "work_id": "예시작품",
  "episode_no": 4,
  "boundary_after_scene_no": 18,
  "left_seq_id": "EP04_S03",
  "right_seq_id": "EP04_S04",
  "primary_boundary_code": "B1_GOAL_SETTLEMENT",
  "secondary_boundary_codes": ["B3_RELATIONSHIP_OR_COMMITMENT_SHIFT"],
  "state_dimensions_changed": ["G", "R"],
  "left_terminal_summary": "주인공의 화해 시도가 명시적 거절로 결제된다.",
  "right_reset_summary": "다음 장면부터 주인공은 화해가 아니라 증거 확보를 새로운 행동 목표로 삼는다.",
  "evidence_scene_nos": [17,18,19],
  "minimality_minus1": "FAIL: Scene18을 제외하면 거절 결제가 완결되지 않는다.",
  "minimality_plus1": "FAIL: Scene19를 왼쪽에 포함하면 새 조사 거래가 섞인다.",
  "verdict": "VALID",
  "confidence": 0.94,
  "by": "GPT_SOURCE_AUDIT"
}
```

---

# 13. 경계를 실제로 수정할 때의 절대 규칙

**THICK에서 경계를 조용히 바꾸지 않는다.**

경계 수정은 반드시 다음 단일 migration 순서로 한다.

1. SOURCE 직접재독해
2. `SequenceBoundaryEvidenceR1` 작성
3. 변경 전 Stage02 boundary snapshot/hash 보존
4. Stage02 SequenceBlueprint membership 수정
5. EpisodeArc 영향 검사/재저작 필요 여부 판단
6. Stage03 CharacterArc/RelationshipArc/LocalEdge 영향 검사
7. Stage04 Payoff/CrossEpisodeEdge 영향 검사
8. THICK를 수정된 Stage02 membership으로 재저작 또는 provenance 재결속
9. PlannerInput R5 재생성
10. Runtime R8 재생성
11. Stage02↔THICK↔R5↔R8 membership parity 검사
12. exact/provenance + semantic + thread + subplot gate
13. fresh extraction
14. migration ledger / supersession 기록

### 금지

- Stage02는 그대로 두고 THICK만 merge/split
- THICK를 고친 뒤 R5/R8만 맞추고 Stage02 불일치 방치
- Python으로 의미적 경계를 자동 생성하여 정본 승격
- 숫자/등분률을 좋게 만들기 위한 경계 조정
- 기존 경계 근거가 약하다는 이유만으로 전체 작품 자동 재분할

---

# 14. Sequence Boundary Integrity Gate R1

## G1 PARTITION — HARD

- Scene 연속
- gap 0
- overlap 0
- Scene이 정확히 한 Sequence에 1회 포함
- scene_span / scene_budget 일치

## G2 BOUNDARY EVIDENCE — HARD for new/audited boundaries

신규 분석 또는 수정·감사 경계는 `SequenceBoundaryEvidenceR1`이 있어야 한다.

## G3 TWO-SIDED TRANSACTION — SEMANTIC HARD

LEFT TERMINAL + RIGHT RESET이 모두 SOURCE로 설명되어야 한다.

## G4 MINIMALITY

현재 R1에서는 REVIEW 중심. CT-12C calibration 후 hard gate 승격 여부 결정.

## G5 UNIFORMITY — DIAGNOSTIC ONLY

- length CV
- equal-cut reproduction
- equal-cut distance

높다고 자동 FAIL 금지. 낮다고 자동 PASS 금지.

## G6 SINGLETON — DIAGNOSTIC

1 Scene Sequence는 terminal/reveal/hook/commitment 근거를 검사한다.

## G7 VALUE SHIFT QUALITY — DIAGNOSTIC

`from == to`, generic value, transaction과 불일치하면 semantic review를 요청한다. 경계 자동 FAIL 금지.

## G8 STAGE02↔DOWNSTREAM MEMBERSHIP PARITY — HARD

승인된 resegmentation migration이 없다면:

`Stage02.member_scene_nos == THICK.member_scene_nos == Planner origin membership == Runtime membership`

이어야 한다.

## G9 SOURCE HOLD — HARD

SOURCE_HOLD 작품은 Sequence boundary positive exemplar와 표준 자격시험에서 제외한다.

---

# 15. 경성스캔들·개와늑대의시간 특별 처리

현재 두 작품에는 문서화되지 않은 이중 segmentation이 존재한다.

따라서:

- 어느 쪽도 자동 삭제하지 않는다.
- V10.1 Stage02 authority는 현재 그대로 유지한다.
- 두 작품은 Sequence boundary positive learning exemplar에서 임시 제외한다.
- THICK/R5/R8는 기존 창작 기능 연구에는 사용할 수 있으나 Stage02 경계의 정답 증거로 사용하지 않는다.
- SOURCE adjudication으로 Stage02 vs THICK 중 어느 granularity가 더 타당한지 판정한다.
- 필요하면 둘 중 하나를 정본으로 선택하고 downstream을 전부 재생성한다.

---

# 16. 다른 GPT 세션의 산출물 규칙

각 작품/블록마다 최소 다음을 남긴다.

```text
sequence_boundary/
  <work_id>/
    SCREENING.json
    evidence/
      EP01.boundary_evidence.jsonl
      EP02.boundary_evidence.jsonl
      ...
    repair/
      BOUNDARY_REPAIR_LEDGER.json
    validation/
      BOUNDARY_INTEGRITY_VALIDATION.json
    CHECKPOINT.json
```

현재 DB exact schema를 변경하지 않는 한 이 계층은 **append-only audit evidence**로 취급한다.

### Checkpoint 권고

회차 단위로 즉시 저장한다.

```json
{
  "work_id": "작품명",
  "completed_episodes": [1,2,3,4],
  "next_episode": 5,
  "boundaries_checked": 31,
  "valid": 23,
  "nearby_valid": 3,
  "merge_candidate": 2,
  "split_candidate": 2,
  "review_required": 1,
  "semantic_data_frozen_after_episode": 4
}
```

작업 중단 후에도 완료된 회차를 다시 추측해서 쓰지 말고 checkpoint에서 이어간다.

---

# 17. 다른 GPT가 절대로 해서는 안 되는 것

1. 장면 수를 비슷하게 만들려고 Sequence를 자르지 말 것.
2. 장소·시간이 바뀌었다는 이유만으로 자르지 말 것.
3. `k_prior`에 맞추려고 merge/split하지 말 것.
4. 기존 Stage02 좌표를 정답이라고 먼저 본 뒤 SOURCE에서 이유를 억지로 찾지 말 것.
5. THICK의 깊이를 경계 정당성의 증거로 착각하지 말 것.
6. value_shift 문자열 하나만 보고 경계를 자동 수정하지 말 것.
7. Python/규칙 기반으로 semantic boundary를 정본 저작하지 말 것.
8. 경계가 애매하면 억지로 VALID/FAIL로 만들지 말고 REVIEW_REQUIRED를 사용할 것.
9. 경계 변경 후 Stage03/04/THICK/R5/R8 영향을 무시하지 말 것.
10. 사용자 승인 없이 V10.1 schema 또는 V9 numeric release를 올리지 말 것.

---

# 18. 다른 GPT가 반드시 해야 하는 것

1. SOURCE를 직접 순차독해한다.
2. 경계마다 LEFT TERMINAL과 RIGHT RESET을 설명한다.
3. G/K/R/P/C/M/W/L 중 무엇이 변했는지 기록한다.
4. B1~B7 중 primary reason을 지정한다.
5. ±1 Scene minimality를 확인한다.
6. 기존 작품 감사에서는 canonical 경계를 보기 전 blind candidate를 freeze한다.
7. 수정은 SOURCE 근거가 있을 때만 한다.
8. Stage02 membership을 downstream 전체의 단일 truth로 관리한다.
9. THICK 전에 boundary parity를 검사한다.
10. 신규/보강 작품은 fresh extraction까지 통과해야 정본 승격한다.

---

# 19. 현재 34작 보강과 다른 세션 신규 분석을 동시에 운영하는 방법

두 작업은 충돌하지 않는다.

## 트랙 A — 기존 34 THICK 보강

`Screening → 위험 경계 SOURCE 감사 → 선택 보강 → downstream 재결속 → BOUNDARY_QUALIFIED`

## 트랙 B — 현재 다른 GPT 세션 신규 작품

`Stage01 → Stage02 + Boundary Evidence → Stage03 → Stage04 → Boundary Gate → THICK → R5 → R8 → Fresh validation`

## 트랙 C — 기존 63작 향후 승격

`작품 선택 → Boundary Screening → 필요한 SOURCE 보강 → THICK 승격`

이 세 트랙 모두 같은 Sequence definition을 사용한다.

---

# 20. 표준의 현재 지위와 다음 검증

이 R1은 **실제 98작 전수 실측을 반영한 운영 표준 초안**이다. 그러나 아직 독립 주석자 재현성 실험 CT-12C가 끝나지 않았다.

따라서:

- 지금부터 신규/보강 분석의 **작업 원칙과 감사 evidence**로는 사용한다.
- 기존 98작 전체 schema migration에는 사용하지 않는다.
- 34작 전체를 기계적으로 재경계하지 않는다.
- CT-12D SOURCE 감사와 CT-12C 독립 재분할 결과로 문구·threshold를 보정한다.
- CT-12C에서 boundary location agreement ≥ 0.85 및 사전등록된 boundary-code agreement 기준을 통과하면 정식 표준 승격을 검토한다.

---

# 21. 다른 GPT 세션에 그대로 전달할 실행 지시문

> 현재 진행 중인 드라마 분석을 중단하거나 처음부터 재분석하지 마라. 기존 V10.1 Stage01 직접독해·Stage01~04 규격은 유지한다. 다만 Stage02 Sequence를 구성할 때부터 `Sequence Boundary R1`을 적용하라. Sequence는 고정 장면 수가 아니라 하나의 지배적 극적 거래가 진행되는 최소 연속 Scene 묶음이다. 모든 경계는 LEFT TERMINAL과 RIGHT RESET을 SOURCE에서 확인하고, G/K/R/P/C/M/W/L 중 어떤 상태가 변했는지와 B1~B7 primary boundary reason을 기록하라. ±1 Scene minimality를 확인하라. 장소 변화·비슷한 길이·작품 평균 k를 경계의 충분조건으로 사용하지 마라. 현재 V10.1 18-key SequenceBlueprint는 변경하지 말고 `SequenceBoundaryEvidenceR1`을 별도 append-only evidence로 작성하라. 이미 Stage02가 끝났다면 THICK 전에 Boundary Integrity를 수행하라. THICK/R5/R8가 Stage02 membership을 조용히 변경하는 것은 금지하며, 경계를 고쳐야 하면 SOURCE 재독해 → Stage02 수정 → Stage03/04 영향검사 → THICK 재저작/재결속 → R5/R8 재생성 → parity/fresh validation 순으로 처리하라. 기존 정본 감사에서는 canonical boundary를 먼저 보지 말고 SOURCE에서 blind candidate를 freeze한 뒤 비교하라. 모든 판정은 VALID / NEARBY_VALID / MERGE_CANDIDATE / SPLIT_CANDIDATE / REVIEW_REQUIRED 중 하나로 남겨라. 경성스캔들과 개와늑대의시간은 legacy dual segmentation 상태이므로 boundary positive exemplar로 사용하지 말고 SOURCE adjudication 전에는 어느 segmentation도 임의 정답으로 승격하지 마라.

---

# 22. 근거 문서

본 설명서는 다음 현재 연구 산출물을 통합해 작성했다.

- `SEQUENCE_STANDARD_V1_2026-08-17.md` — Claude 제안 시퀀스 표준 v1
- `2026-08-17_session_summary_home.md` — CT-11/11B/11C/12A/12B 실험 종합
- `SEQUENCE_BOUNDARY_FULL_CORPUS_CENSUS_R1_20260817.md` — 98작 전수 계측
- `SEQUENCE_DEFINITION_BOUNDARY_DESIGN_STANDARD_R1_DRAFT_20260817.md` — DB 전수실측 기반 정의·설계 R1
- `SEQUENCE_BOUNDARY_INTEGRITY_GATE_R1_DRAFT_20260817.md` — 경계 검증 게이트
- `SEQUENCE_STAGE02_THICK_DUAL_SEGMENTATION_LINEAGE_FINDING_R1_20260817.md` — Stage02↔THICK 이중 segmentation 계보
- `CLAUDE_SEQUENCE_STANDARD_V1_ADOPTION_DECISION_R1_20260817.md` — Claude v1 채택/수정 판정
- `CT12D_SEQUENCE_BOUNDARY_SOURCE_AUDIT_PROTOCOL_R1_20260817.md` — 기존 정본 SOURCE blind 감사 절차
- `sequence_boundary_evidence_r1.schema.json` — append-only 경계 증거 계약
- `validate_sequence_boundary_integrity_r1.py` — 휴대형 검증기

---

## 최종 한 문장

> **앞으로 Sequence를 “몇 Scene씩 나눈 묶음”으로 학습시키지 말고, “하나의 극적 거래가 왜 시작되고 어떻게 결제되며 왜 바로 이 지점에서 다음 거래로 넘어가는가”를 SOURCE 근거와 함께 학습시킨다.**
