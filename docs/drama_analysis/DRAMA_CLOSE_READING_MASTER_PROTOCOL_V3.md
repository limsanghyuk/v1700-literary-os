# 드라마 직접독해 마스터 프로토콜 v3

- Document ID: `DRAMA-CLOSE-READING-MASTER-PROTOCOL-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Supersedes operational guidance in Issue #60 where this document is more specific.

## 1. 목표

장편 드라마 원본을 직접 읽고, 장면 의미·시퀀스·회차 아크·인물/관계/인과·장거리 회수를 근거가 끊기지 않게 저작한다. 대량 범위 때문에 작업이 키워드 추출·템플릿 채우기·Python 의미 생성으로 전환되는 것을 금지한다.

## 2. 기본 생산 단위

```text
SAFE_DEFAULT = 1 episode × 4 quarters
Q1 → Q2 → Q3 → Q4
```

여러 회차를 하나의 납품 묶음으로 계획할 수 있으나 실제 저작과 잠금은 회차별로 수행한다. 앞 회차가 영속화·검증되지 않으면 다음 회차로 이동하지 않는다.

## 3. 회차 실행 순서

1. 원본 파일 SHA256과 인코딩 확인.
2. 물리 헤딩을 추출하고 논리 SceneCard 경계를 결정.
3. `scene_no=1..N` canonical ordinal 부여.
4. 원문을 Q1~Q4로 균등 분배하되 의미 경계는 변경하지 않음.
5. 각 Quarter에서 다음을 순서대로 수행.
   - 장면 원문 직접독해
   - Stage01 SceneCard 저작
   - 동일 장면 기준 EXT6 CastPresence 포착
   - SourceSceneAlignment 기록
   - QuarterAudit 검증·잠금
6. Q1~Q4 완료 후 Stage02 SequenceBlueprint를 회차 전체 기준으로 재구성.
7. EpisodeMeta와 Stage03 EpisodeArc·CharacterArc·RelationshipArc·LocalEdge·PayoffCandidate 직접 저작.
8. CharacterLoad를 Stage01/02/03 결과에서 결정론으로 파생.
9. 회차 강한 게이트 실행.
10. 회차 체크포인트와 SourceLock 진행 상태를 영속화.
11. 다음 회차로 이동.
12. 전체 시즌 완료 후 Stage04 fan-in과 FullSeriesArc 작성.

## 4. Stage01 직접독해 규율

SceneCard exact 9키는 `SCHEMA_CONTRACTS_V2.md`를 따른다.

### 의미 깊이

- `heading`: 원본 provenance와 대응.
- `title`: 사건 요약이 아니라 장면의 고유 전환을 압축.
- `intent_gist`: 누가 무엇을 원하고, 어떤 압력 때문에 무엇이 변하는지 기록.
- `core/core2`: 실제 극적 기능만 CORE_ENUM 16에서 선택.
- `skin`: 장면의 표면 장르·연출 질감. 극적 기능과 중복하지 않음.

### 내용 품질 기준

좋은 SceneCard는 다음을 구분한다.

```text
행동: 실제로 일어난 것
전략: 말하거나 숨기거나 회피한 방식
정보 변화: 새로 알게 된 사실·오해·조건
선택: 인물이 실제로 선택·거부·보류한 것
구조 기능: 회차에서 이 장면이 필요한 이유
잔여 동력: 다음 장면을 구체적으로 밀어내는 원인
```

9키 정본에는 이 여섯 질문의 답을 `title/intent_gist/core/core2/skin`에 압축하되, 내부 독해에서 질문을 생략하지 않는다.

### 금지

- 장면 요약 한 문장을 다른 필드에 반복 삽입
- 키워드 조각을 문장 템플릿에 삽입
- `[EPxx-Syy: ...]` 같은 가시적 참조 표식 잔류
- 여러 장면에 같은 골격 문장 반복
- 원문에 없는 인물·행동·감정·인과 생성
- Python 함수로 의미 필드 생성

## 5. Stage02 시퀀스 규율

SequenceBlueprint exact 18키와 turn registry는 `SCHEMA_CONTRACTS_V2.md`를 따른다.

### 시퀀스 분할 기준

시퀀스는 장면 수 균등분할이 아니라 다음 변화로 나눈다.

- 목표 주체 또는 목표가 바뀜
- 장애의 성격이 바뀜
- 정보·관계·권력 가치가 전환됨
- 새로운 장소가 아니라 새로운 극적 행동 단위가 시작됨

### 필수 불변식

```text
I-COVER: 모든 scene_no가 정확히 하나의 sequence에 포함
I-PARTITION: 중복 0, 누락 0
I-COUNT: sum(scene_budget) == episode_scene_count
runtime_share sum == 1.0
core_mix ⊆ member SceneCard의 실제 core/core2
turn_class == turn_type registry 파생값
```

Stage02는 Stage01의 검증층이기도 하다. 목표·장애·전환에 기여하지 못하는 SceneCard는 Stage01로 되돌려 보강한다.

## 6. Stage03 저작 규율

### EpisodeArc

회차의 입구 상태, 압력 상승, 전환점, 출구 상태를 실제 시퀀스 근거로 작성한다. 숫자상 4등분으로 act를 만들지 않는다.

### CharacterArc

```text
인물 × 실제 변화가 발생한 회차
```

- trigger_scene_no에 해당 인물이 실제 등장해야 함.
- `state_delta`는 작품 전체 성격 요약이 아니라 이번 회차의 변화량.
- 변화가 없는 단역을 수량 채우기 위해 생성하지 않음.

### RelationshipArc

```text
관계쌍 × 실제 상호작용·관계변화 회차
```

- trigger scene에 양쪽 인물이 등장·통화·교신해야 함.
- `(A,B)`와 `(B,A)` 중복 금지.

### LocalEdge

- 동일 회차만 허용.
- `edge_type=causal`, `gap_episodes=0`.
- `label`은 target SceneCard.core와 정확히 일치.
- 단순 인접성·유사 주제는 인과가 아님.

### PayoffCandidate

장거리 가능성을 후보로만 저장한다. 후속 회차 확인 전 CrossEpisodeEdge로 승격하지 않는다.

## 7. Stage04 전 시즌 fan-in

모든 회차 완료 후 다음 순서로 수행한다.

1. PayoffCandidate 전수 목록화.
2. 후보의 원 장면을 다시 확인.
3. 후속 회차의 실제 회수·변형·반향 장면 확인.
4. 양쪽 장면의 의미·인과·모티프를 대조.
5. 검증된 연결만 CrossEpisodeEdge로 승격.
6. 모든 후보에 disposition 기록.
7. 전체 counts와 시즌 구조를 재계산해 FullSeriesArc 저작.

금지:

```text
이전 회차 마지막 장면 → 다음 회차 첫 장면 자동 연결
회차 번호가 멀다는 이유만으로 plant/payoff 판정
미확인 후보의 일괄 승격
```

## 8. Python 사용 경계

### 허용

- 원본 추출·인코딩 확인
- 헤딩 탐지와 ordinal 정렬 보조
- SHA256·offset·line span 생성
- JSON/JSONL 직렬화
- exact keyset·enum·FK·coverage 검사
- 결정론적 CharacterLoad 계산
- 반복 문형·placeholder 탐지
- ZIP·manifest·checksum 생성

### 금지

- SceneCard 의미 문장 생성
- Sequence goal/obstacle/value_shift 생성
- CharacterArc/RelationshipArc 의미 생성
- LocalEdge/Payoff/CrossEdge 의미 생성
- 키워드 기반 주제·감정·기능 자동 판정

## 9. 품질 깊이 척도

- 4: 행동·전략·정보·선택·구조 기능·다음 동력이 모두 구체적.
- 3: 대부분 구체적이나 한 축이 약함.
- 2: 사건 요약은 있으나 선택·정보 변화가 추상적.
- 1: 키워드·템플릿 중심.
- 0: 자동 생성·복사·환각.

권장 회차 기준:

```text
평균 >= 3.0
최저 >= 2.5 또는 해당 장면 재저작
0점/1점 장면 = 0
```

## 10. PASS 원칙

```text
형식 PASS ≠ 내용 PASS
Stage02 coverage PASS ≠ Stage01 의미 PASS
사람용 보고서 PASS ≠ 실제 데이터 PASS
```

구조·내용·반게이밍·근거·파생 재계산을 모두 통과해야 `PASS_CANDIDATE`를 선언한다. `CANONICAL`은 사용자 승인 후에만 사용한다.
