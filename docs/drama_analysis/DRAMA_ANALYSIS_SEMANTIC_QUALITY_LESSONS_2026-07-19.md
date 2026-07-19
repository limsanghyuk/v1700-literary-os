# 드라마 의미 품질 교훈과 재발 방지 보충서

- 상태: `AUTHORITATIVE SUPPLEMENT / CURRENT`
- 적용일: `2026-07-19`
- 적용: GPT·Claude 공동 Stage01~04 분석
- 상위 계약: `SCHEMA_CONTRACTS_V2.md`
- 실행 진입점: `START_HERE_NEW_DRAMA_ANALYSIS.md`
- EXT6: `DISABLED_BY_DEFAULT`

이 문서는 67작품 Stage01 동일 평가표 감사와 《라이벌》·《여우야 뭐하니》·《신화》 재검토, 이어진 Stage02~03 반복·비전진 결함 보강에서 확인된 교훈을 새 작품 분석 절차에 반영한다. exact keyset·enum·ID·FK를 바꾸지 않는다. 구조검사와 의미 품질검사의 역할을 분리하고, 직접독해 결과가 실제로 전진하는 분석 레코드가 되도록 한다.

## 1. 핵심 판정

`구조 PASS`는 다음만 입증한다.

- JSON/JSONL parse
- exact keyset·type
- ID·FK·참조 무결성
- 장면·시퀀스 coverage
- 허용 enum
- 파일·경로·집계 정합성

`구조 PASS`는 다음을 입증하지 않는다.

- 원문에 충실한 해석
- 장면별 고유한 의미
- 시퀀스 목표·장애의 전진
- 인물·관계 변화의 실제 발생
- LocalEdge의 반사실 인과
- 반복 템플릿 부재
- 복선과 회수의 실제 장거리 연결

따라서 작품 완료에는 구조검사와 별도로 의미 품질 PASS가 필요하다.

## 2. 67작품 감사에서 확인한 범위와 한계

동일 평가표는 작품별 최대 7개 결정론적 위치를 사용해 67작품 469개 Stage01 표본을 비교했다.

평가축:

1. 원문 충실도
2. 장면 경계
3. 사건 변화 밀도
4. 원문 대비 행동 밀도
5. 원문 대비 감정·상태 변화 밀도
6. 비반복성
7. 누락·coverage

이 평가는 전 작품의 상대적 편차와 위험 작품을 찾는 선별 감사다. 전체 SceneCard 전수 의미감사를 대신하지 않는다. 저점 작품은 자동 재저작하지 않고 원문을 직접 대조해 실제 결함과 원본 형식의 한계를 구분한다.

## 3. 세 작품에서 확인된 실패 유형

### 3.1 라이벌

확인된 문제:

- Stage01 반복 종결문
- 장면 근거보다 템플릿 비중이 큰 CharacterArc·RelationshipArc
- 단순 인접·같은 시퀀스·유사 감정을 인과로 확장한 LocalEdge 과밀

교훈:

- 레코드 수가 많아도 의미 변화가 고유하지 않으면 밀도가 아니다.
- Stage03은 회차별 고정 수량을 채우지 않는다.
- LocalEdge는 적고 강한 반사실 인과가 우선이다.

### 3.2 여우야 뭐하니

확인된 문제:

- Stage01 반복 문구
- 실제 원인→결과가 아닌 LocalEdge
- 일부 인물·관계 변화의 trigger 장면 불일치

교훈:

- 전 시즌 서사를 이해해도 장면 참조가 틀리면 정본 품질이 아니다.
- trigger에는 해당 인물의 발화·행동·통화·교신 근거가 있어야 한다.
- 분석자가 알고 있는 후속 결과를 앞 장면에 소급해 과잉 인과화하지 않는다.

### 3.3 신화

확인된 문제:

- Stage01 반복 종결문
- 관계 당사자·trigger의 부분 불일치
- 종결부 LocalEdge 과밀

교훈:

- 작품 결말의 중요성은 edge 수 증가의 근거가 아니다.
- 동일 관계쌍은 회차 안에서 하나의 복합 전진으로 통합한다.
- 종결부에서는 여러 장면의 단순 연속보다 핵심 선택을 만든 강한 인과만 남긴다.

## 4. 새 작품 필수 실행 흐름

```text
원본 inventory·회차 경계 잠금
→ 최신 DB 작품 인덱스와 차집합
→ SourceLock Core
→ EP01 Q1→Q4 직접독해
→ EP01 Stage01~03 직접 저작
→ 구조검사
→ 단일 checkpoint
→ 순차 회차 진행
→ 전체의 약 50%에서 의미 캘리브레이션 1회
→ 발견 규칙을 후반부 저작에 적용
→ 전 회차 Stage01~03 완료
→ 전 시즌 의미 품질검사 1회
→ Stage04
→ 작품 완료검사
→ 작품 ZIP Fresh Extraction 1회
→ DB 증분 편입
```

중간 의미 캘리브레이션과 완료 의미검사는 과거의 Q별 QuarterAudit·다중 증빙·반복 ZIP을 부활시키는 것이 아니다. 각각 작품당 한 번 수행한다.

## 5. Stage01 저작·검사 규칙

각 SceneCard는 해당 장면만의 변화 단위를 가져야 한다.

- `title`: 고유 행동·선택·전환
- `intent_gist`: 주체·목표·전략·장애·변화
- `skin`: 구체 상황과 표면 사건
- `core/core2`: 실제 극적 기능

금지:

- 인물명·장소명만 바꾼 동일 골격
- “다음 장면으로 압력을 넘긴다” 같은 전 회차 공통 종결문
- 장면에 없는 감정·행동·인과 추가
- 원문이 짧다는 이유로 장황한 해석을 보충
- 원본 블록 경계가 불명확한데 임의로 장면을 세분

점검:

- exact·masked 반복
- 원문과 title·intent의 주체/행동/결과 대조
- 장면 경계에서 장소·시간·행동 전환 보존
- 기능 장면과 변화 장면을 구분해 밀도를 상대 평가

## 6. Stage02 저작·검사 규칙

SequenceBlueprint는 장면 묶음이 아니라 하나의 전진 단위다.

각 시퀀스는 다음에 답해야 한다.

1. 시작 상태는 무엇인가.
2. 누가 무엇을 원하는가.
3. 이 시퀀스 고유의 장애물은 무엇인가.
4. 어떤 행동 계획이 실행되는가.
5. 종료 상태가 어떻게 달라지는가.

금지:

- 여러 시퀀스에 같은 `goal`·`obstacle` 복사
- 범용 갈등어만 반복
- 장면 수 균등분할
- `sequence_intent`와 무관한 목표·장애
- 동일 목표가 상태 변화 없이 연속 반복되는 비전진 시퀀스

검사:

- `sequence_intent/goal/obstacle` exact·masked 반복
- 각 시퀀스의 시작→종료 가치 변화
- member SceneCard의 행동·정보·관계 변화와의 대응
- turn_type→turn_class 계약
- coverage·span·budget·runtime 정합성

## 7. Stage03 저작·검사 규칙

### CharacterArc

- 실제 상태 변화가 있는 인물만 기록한다.
- `state_label`은 `DESIRE`, `CONFLICT`, `series_start` 같은 범용 표지로 대체하지 않는다.
- `state_delta`는 이전 상태와 새 상태를 구분한다.
- trigger 장면에 인물의 직접 행동·발화 또는 명시적 사건 영향이 있어야 한다.
- evidence를 여러 인물에게 복사하지 않는다.

### RelationshipArc

- 동일 회차의 unordered pair `{A,B}`는 하나만 허용한다.
- 같은 장면에서 신뢰·권력·정보·의존이 함께 변하면 하나의 복합 변화로 통합한다.
- 양쪽 당사자의 등장·통화·교신 또는 관계를 직접 바꾸는 명시적 행위가 필요하다.
- `relation_state`와 `relation_delta`를 구분한다.
- 별칭·축약은 evidence로 확인하되 검사 통과만을 위해 이름을 인위적으로 반복하지 않는다.

### LocalEdge

필수:

```text
src_episode_no = tgt_episode_no
src_scene_no < tgt_scene_no
gap_episodes = 0
```

반사실 질문:

```text
source 장면이 없었다면 target의 핵심 선택·행동·상태가 발생하지 않거나 실질적으로 달라지는가?
```

금지:

- 단순 인접
- 같은 인물 등장
- 같은 시퀀스
- 유사 감정·주제
- 첫 장면→마지막 장면 자동 연결
- 역방향 edge
- 결말이라는 이유만으로 edge 증식

## 8. Stage04 저작·검사 규칙

- 모든 PayoffCandidate를 승격·재분류·해결·기각 중 하나로 처분한다.
- CrossEpisodeEdge는 실제 plant→보존/변형→payoff가 확인돼야 한다.
- 자동 회차 브리지와 규칙적 n→n+1·n+2 연결을 금지한다.
- 여러 독립 복선이 한 결말로 모이는 fan-in은 중복과 구분한다.
- FullSeriesArc는 실제 매크로 전환을 사용하며 기계적 4분할을 금지한다.

## 9. 작품 중간 50% 의미 캘리브레이션

전반부 Stage01~03에서 다음을 한 번 검사한다.

- Stage01 원문 충실도·장면 경계·반복 골격
- Stage02 목표·장애·의도의 exact/masked 반복과 비전진
- CharacterArc 범용 상태어·trigger participant·evidence 복사
- RelationshipArc 동일 unordered pair·당사자·trigger
- LocalEdge 방향·반사실 인과·인접 편향·과밀
- PayoffCandidate의 구체성·중복·회차 내 해결 여부

실패 레코드만 원문과 대조해 보강한다. 전면 재저작은 실제 계층 전체가 오염됐을 때만 시행한다. 교정한 규칙을 후반부에 적용한다.

## 10. 전 시즌 의미 품질 게이트

Stage04 전에 다음이 모두 충족돼야 한다.

- 구조검사 PASS
- Stage01 원문 불일치·대량 템플릿 반복 없음
- Stage02 exact 반복·masked 반복 임계 실패 없음
- Stage03 범용 상태어 대량 반복 없음
- 동일 회차 RelationshipArc unordered pair 중복 없음
- LocalEdge 역방향·회차 간 연결 없음
- LocalEdge 표본 반사실 검사 통과
- trigger·evidence 표본 원문 대조 통과
- 미처리 의미 실패 0

경고는 자동 수정하지 않는다. 별칭·축약·한쪽 당사자만 제목에 나타나는 경우처럼 validator 휴리스틱의 한계인지 원문으로 판정한다. 검사 통과를 위한 이름 삽입·문장 장문화는 금지한다.

## 11. 완료·보고 규칙

완료 보고는 다음을 구분한다.

- `STRUCTURAL PASS`: 스키마·키·참조·coverage 통과
- `SEMANTIC PASS`: 반복·근거·전진·인과 품질 통과
- `PASS_CANDIDATE`: 구조·의미·Stage04·패키지 검사 완료
- `CANONICAL`: 사용자 승인 완료

표본 감사는 전수 의미감사라고 보고하지 않는다. 평균점수 상승은 모든 작품·모든 장면의 개선으로 일반화하지 않는다. 실제 수정한 작품과 검토 후 유지한 작품을 분리해 기록한다.

## 12. 자동화 경계

자동화 허용:

- 원본 추출·인코딩 정규화
- 해시·직렬화·수량 집계
- exact keyset·ID·FK 검사
- 반복·방향·밀도 위험 탐지
- ZIP·Fresh Extraction·SHA 검증

자동화 금지:

- SceneCard 의미 문장 생성
- Sequence goal·obstacle 생성
- CharacterArc·RelationshipArc 상태 변화 생성
- LocalEdge·CrossEpisodeEdge 인과 결정
- 원문 미독해 상태의 완료 판정

의미 validator는 위험 후보를 찾는다. 최종 의미 판정과 보강 문장은 원문 직접독해로 수행한다.

## 13. 권위 관계

충돌 시 우선순위:

1. `SCHEMA_CONTRACTS_V2.md` — exact schema
2. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 실행 정책
3. 이 문서 — 의미 품질·재발 방지 상세
4. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` — 압축 실행 순서
5. 작품 SourceLock·checkpoint
6. 과거 incident·세션 문서

이 문서는 새 스키마나 새 DB 릴리즈를 만들지 않는다. 현재 V5 권위 체계에 의미 품질 교훈을 편입한다.
