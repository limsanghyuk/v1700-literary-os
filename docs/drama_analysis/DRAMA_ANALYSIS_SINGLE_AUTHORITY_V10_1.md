# 한국 드라마 분석 단일 권위 V10.1

Authority ID: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`  
Version: `10.1.0`  
Effective date: `2026-07-28`  
Status: `ACTIVE_SINGLE_AUTHORITY`

## 0. 권위 관계

V10.1은 `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10`의 Stage01~04 exact schema, 원본 직접독해, Python 의미 생성 금지, 저작·감사 run 분리, SourceLock, CandidateDisposition 100%, Fresh Extraction 원칙을 모두 승계한다.

V10.1이 추가하는 것은 다음 세 가지다.

1. 신규 작품의 `Arc Coverage Expansion Pass`
2. 외부 GPT·Claude·Gemini·사람 분석의 선택 수용 계약
3. 독립 Functional Holdout과 비대상 작품 불변성 게이트

충돌 시 V10.1이 우선한다. V10은 역사·기초 계약으로 보존한다.

## 1. 핵심 결정

기존 의미 PASS 작품 86개를 전부 다시 직접 재작업하지 않는다.

```text
기존 PASS 작품 전면 재작업
→ 기본값 금지

결손·편중 신호 탐지
→ 외부 분석 후보 수집
→ 원문·SceneCard 접지
→ 중복·참여자·lineage 검사
→ 독립 Functional Holdout
→ 입증된 레코드만 SELECTIVE_APPEND
```

Claude 등 외부 provider의 분석은 폐기하지 않지만 정답으로도 취급하지 않는다. 모든 외부 분석은 `EXTERNAL_ANALYSIS_CANDIDATE`다.

## 2. Core schema

V10.1은 다음 core exact schema를 변경하지 않는다.

- SceneCard 9키
- EpisodeMeta 5키
- SequenceBlueprint 18키
- EpisodeArc 13키
- CharacterArc 8키
- RelationshipArc 9키
- Local/CrossEpisodeEdge 12키
- PayoffCandidate 7키
- FullSeriesArc 17키

추가되는 것은 의미 record가 아니라 감사·계보·기능 증거다.

## 3. 신규 작품 실행 순서

```text
SourceBoundaryReview
→ 원본 전체 순차 독해
→ Stage01 SceneCard
→ Stage02 SequenceBlueprint
→ Stage03 1차 Arc·Edge·Payoff
→ Arc Coverage Expansion Pass
→ 회차 경량 게이트
→ 독립 원문 감사
→ EPISODE_CHECKPOINT_LOCKED
```

전 회차 Stage01~03 잠금 후에만 Stage04를 수행한다.

### 3.1 Arc Coverage Expansion Pass

Stage03 초안 뒤 같은 회차 원문과 저장된 SceneCard를 다시 보며 보조 인물·관계의 실제 상태 변화 누락을 검사한다.

- 주요 인물뿐 아니라 독립 선택·정보 획득·권력 변화·관계 전환을 겪은 보조 인물을 조사한다.
- 등장했다는 이유만으로 Arc를 만들지 않는다.
- CharacterArc 당사자는 trigger 장면에 실제 등장해야 한다.
- RelationshipArc 양쪽 당사자는 같은 장면에 등장하거나 직접 통화·교신해야 한다.
- 동일 인물·동일 관계·동일 회차 키 중복을 금지한다.
- 고정 수량이나 밀도 목표를 두지 않는다.
- 후보·채택·거부 이유를 `arc_coverage_audit.json`에 남긴다.

## 4. 기존 작품 보강 우선순위

다음 신호가 있는 작품만 선택 감사한다.

- 주·조연 등장 빈도 대비 CharacterArc가 없거나 매우 낮음
- 반복 상호작용 관계인데 RelationshipArc가 전무함
- provider 판본 간 Arc 수 차이가 크고 SceneCard lineage가 동일함
- 보조 인물·관계 검색 질문이 지속 실패함
- trigger 장면은 존재하지만 현재 Arc가 핵심 인물에만 편중됨
- semantic warning, 장면 번호 불일치, 반복 증거가 집중됨

모든 작품을 같은 강도로 다시 읽지 않는다. 작품별 coverage·밀도 대시보드로 우선순위를 정한다.

## 5. 외부 분석 선택 수용

허용 mode:

- `SELECTIVE_APPEND`: 기존 record를 보존하고 검증된 신규 record만 추가
- `SELECTIVE_REPLACE_WITH_LEDGER`: 명백한 오류만 원문 근거와 supersession ledger로 교체
- `FULL_WORK_REPLACE`: source hash·ordinal lineage가 동일하고 작품 전체 재검증을 통과할 때만 허용
- `REJECT_EXTERNAL_CANDIDATE`: 근거 부족·중복·장면 불일치·미래 정보 혼입

기본 mode는 `SELECTIVE_APPEND`다.

### 5.1 수용 필터

후보 record는 다음을 모두 통과해야 한다.

- target work·episode·scene 존재
- source hash 또는 canonical ordinal lineage 호환
- trigger 참여자 실제 존재
- 기존 동일 키 record 없음
- 실제 state/relationship delta 존재
- evidence와 장면 의미 일치
- 미래 회차 정보 혼입 없음
- provider 내부 exact duplicate·골격 반복 아님
- 독립 원문 감사 완료

하나라도 실패하면 수용하지 않는다.

## 6. Functional Holdout

선택 수용은 record 수 증가가 아니라 기능 개선을 입증해야 한다.

- 질문 세트와 정답키를 후보 Arc에서 자동 생성하지 않는다.
- 기존 핵심 질문과 보조 인물·관계 질문을 분리한다.
- baseline과 reinforced 판본의 Recall@5·MRR을 비교한다.
- 핵심 질문 Recall@5가 하락하면 기본적으로 실패다.
- 보조 질문 개선이 없으면 수용하지 않는다.
- 수용 후 구조·의미·SourceLock·Fresh Extraction을 다시 통과한다.

권장 기준:

```text
core Recall@5: 유지 또는 개선
supplemental Recall@5: 유의미한 개선
semantic errors: 0
SELECTIVE_APPEND overwrite: 0
non-target hash mismatch: 0
```

## 7. 필수 증거

```text
coverage_audits/{work_id}/arc_coverage_audit.json
provider_adoption/{work_id}/provider_selective_adoption_ledger.json
functional_holdout/{work_id}/functional_holdout.json
seqcard_ko/authorship/PROVIDER_AUTHORSHIP_PROVENANCE_INDEX.json
validation/works/{work_id}/coverage_and_adoption_validation.json
```

## 8. 외부 분석 열람 시점

신규 작품의 동일 작품 외부 의미문은 최초 author lock 전에 열지 않는다.

```text
원본 직접독해·Stage01~03 초안 잠금
→ Arc Coverage Expansion Pass
→ 독립 원문 감사
→ 외부 분석 후보 열람
→ 누락 후보 선택 감사
→ Functional Holdout
```

기존 작품 선택 보강에서는 외부 분석을 후보 목록화할 수 있지만, 수용은 원문·SceneCard·SourceIndex를 다시 확인한 뒤 내린다.

## 9. 금지

- provider 판본 Arc 전량 복사
- record 수가 많다는 이유로 우수 판정
- 장면 참여자 검사 없는 trigger 수용
- source hash·ordinal이 다른 판본 혼합
- 기존 핵심 Arc 이유 없는 덮어쓰기
- 후보 분석에서 질문과 정답키를 동시에 파생한 자기검증
- 보조 인물 coverage 고정 수량 강제
- Python으로 coverage 의미 생성

## 10. 검증된 선례

《하얀거탑》 앵커 실험에서 Claude 추가 Arc 160건 중 63건만 선택 수용하고 97건을 거부했다.

- 기존 핵심 질문 Recall@5: 1.00 유지
- 보조 질문 Recall@5: 0.00 → 1.00
- 기존 GPT Arc 덮어쓰기: 0
- 장면 번호 불일치·중복·간접 추정 후보: 거부

따라서 Claude 분석 활용은 효과적이지만 전량 수용은 위험하다는 결론을 채택한다.

## 11. 최종 운영 원칙

```text
새 작품:
처음부터 V10.1 확장 분석 포함

기존 PASS 작품:
전면 재작업하지 않음

외부 분석:
후보 증거로 활용

수용:
원문 접지 + 선택 감사 + holdout 통과분만

core schema:
V10과 동일 유지
```
