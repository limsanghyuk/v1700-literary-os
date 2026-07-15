# 앙상블 추적·인과 엣지 선별 정책 v1

- Document ID: `DRAMA-ENSEMBLE-TRACKING-EDGE-SELECTIVITY-POLICY-V1`
- Status: `AUTHORITATIVE_CANDIDATE`
- Date: 2026-07-15
- Exact schema impact: 없음
- Evidence basis: `킬미힐미`·`스토브리그` 품질 비교와 `싸인` 적용 결과

## 1. 목적

스토브리그 분석의 장점인 넓은 인물·관계망 추적을 신규 드라마 분석의 Stage03에 흡수한다. 동시에 과도한 LocalEdge, 장면 인접성 자동 연결, 회차 간 LocalEdge, PayoffCandidate 미처리를 차단한다.

## 2. 채택하는 장점

- 주인공 중심에 갇히지 않는 회차별 인물 변화 추적
- 조직·팀·가족·경쟁 진영의 조연과 기능 인물 추적
- 동맹·경쟁·상하·공모·거래·은폐 관계 변화 추적
- 앙상블 드라마의 검색·학습 재료 폭 확대

## 3. 채택하지 않는 방식

- 등장인물 전원을 기계적으로 CharacterArc화
- 관계쌍 전부를 기계적으로 RelationshipArc화
- 모든 장면을 다음 장면과 LocalEdge로 연결
- 같은 시퀀스라는 이유로 LocalEdge 생성
- 회차 간 연결을 LocalEdge에 저장
- 후보를 만들고 disposition 없이 방치
- 레코드 수량을 품질 점수로 사용

## 4. 회차별 앙상블 스캔

Stage03 저작 전 내부 감사에서 다음을 확인한다.

1. 이번 회차에서 상태가 변한 주인공·대립자
2. 의사결정권을 얻거나 잃은 조연
3. 조직의 방향을 바꾼 실무자·관리자
4. 새로운 정보로 입장이 바뀐 인물
5. 충성·신뢰·공모·갈등이 바뀐 관계쌍
6. 단역이지만 이후 사건축을 바꾼 인물 또는 관계

내부 감사 목록은 패키지 report 또는 validation metadata에 남길 수 있으나 Stage03 exact schema에 새 필드를 추가하지 않는다.

## 5. CharacterArc 범위

기록 조건:

- 회차 입구와 출구 사이에 식별 가능한 상태 변화가 있음
- trigger 장면에 해당 인물이 실제 등장함
- evidence가 변화의 구체 근거를 설명함

제외 조건:

- 단순 등장
- 반복 대사만 있음
- 상태 변화 없음
- 다른 인물 evidence를 복사해야만 설명 가능

고정 수량은 없다. 주연 2명만 기록하는 하한 고정도 금지하고, 모든 등장인물을 기록하는 상한 없는 증식도 금지한다.

## 6. RelationshipArc 범위

기록 조건:

- 신뢰·권력·의무·갈등·거리·연합·거래 조건 중 하나가 바뀜
- trigger 장면에 양쪽 인물이 함께 등장하거나 직접 교신함
- relation_state와 relation_delta가 분리됨

제외 조건:

- 같은 공간에 있었을 뿐 상호작용이 없음
- 관계가 변하지 않음
- 다른 회차의 변화 요약을 복사함

## 7. 앙상블 커버리지 검증

validator 또는 수동 검토 보고서는 다음 질문에 답해야 한다.

```text
회차의 핵심 의사결정자 중 실제 변화가 있는데 누락된 인물이 있는가?
회차의 핵심 동맹·갈등·상하 관계 중 실제 변화가 있는데 누락된 관계쌍이 있는가?
수량을 맞추기 위해 변화 없는 인물·관계가 포함됐는가?
```

누락은 보강하고, 수량 채우기는 삭제한다.

## 8. LocalEdge 선택 규칙

LocalEdge는 같은 회차에서 source 사건이 target 사건을 실제로 발생시키거나 실질적으로 바꾼 경우만 기록한다.

### 필수 반사실 질문

```text
source가 없었더라도 target이 같은 방식으로 발생했는가?
```

- 예: LocalEdge가 아닐 가능성이 높음
- 아니오: 구체 근거를 note에 기록하고 후보로 검토

### 하드 게이트

```text
cross-episode LocalEdge == 0
edge_type == causal
gap_episodes == 0
label == target core
source/target scene exists
```

### 인접 장면

바로 다음 장면 연결은 허용될 수 있으나 직접 인과 증명이 있어야 한다. 번호 인접성은 근거가 아니다.

### 과밀 감사 트리거

```text
LocalEdge / SceneCard > 0.10
또는
adjacent-target LocalEdge ratio > 0.50
```

트리거 발생 시 다음을 재검토한다.

- 단순 순서 연결인지
- 유사 주제 연결인지
- 시퀀스 내부 모든 장면을 사슬로 만든 것인지
- 하나의 인과를 여러 엣지로 중복 분할했는지

트리거는 자동 실패가 아니지만 감사 없이 PASS할 수 없다.

## 9. PayoffCandidate와 Stage04

- 후보는 장거리 가능성이 구체적인 장면만 생성한다.
- 작품 전체를 읽기 전 확정하지 않는다.
- 모든 후보는 개별 disposition을 가져야 한다.
- 미처리 후보가 1건이라도 있으면 Stage04 실패다.
- 회차 간 연결은 검증 후 CrossEpisodeEdge에서만 관리한다.

## 10. 적용 사례

### 킬미힐미

- 의미 깊이와 Stage04 전수 처분의 우선 참조
- 선별적 LocalEdge
- SourceLock·강검증·계보 존재

### 스토브리그

채택:

- 26명 인물 추적
- 38개 관계쌍 추적
- 조직극 앙상블 폭

배제:

- 회차당 44.38 LocalEdge
- 바로 다음 장면 연결 70%
- 회차 간 LocalEdge 16건
- 미처리 후보 83건

### 싸인

현행 계약 안에서 채택 결과:

```text
20 episodes
CharacterArc 100
RelationshipArc 80
LocalEdge 60
PayoffCandidate 40 / disposition 40
CrossEpisodeEdge 36
auto boundary bridge 0
errors 0 / warnings 0
```

싸인의 수량은 참고 사례이며 다른 작품의 고정 할당량이 아니다.

## 11. 최종 원칙

```text
앙상블 폭은 넓게 검토한다.
Arc는 실제 변화만 기록한다.
LocalEdge는 적게 만들기 위해 줄이는 것이 아니라 인과가 아닌 것을 제거한다.
PayoffCandidate는 반드시 전수 처분한다.
스키마는 변경하지 않는다.
```
