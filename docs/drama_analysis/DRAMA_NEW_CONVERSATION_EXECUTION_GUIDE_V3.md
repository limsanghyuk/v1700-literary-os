# 새 대화창 한국 드라마 분석 즉시 실행 가이드 v3

- 상태: `AUTHORITATIVE / CURRENT`
- 갱신: `2026-07-18`
- 상세 권위: `START_HERE_NEW_DRAMA_ANALYSIS.md`
- exact schema: `SCHEMA_CONTRACTS_V2.md`
- 문서·DB 릴리즈 번호 자동 증가 금지

## 최소 로드

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. 최신 DB 전체 작품 인덱스
4. 재개 작업이면 단일 checkpoint

## 즉시 실행

```text
원본 inventory
→ DB 차집합
→ SourceLock Core
→ EP01 Q1→Q4 직접독해
→ EP01 Stage01~03 직접 저작
→ 정본 저장
→ 최소 구조검사
→ 단일 checkpoint
→ EP02
→ ...
→ 전 시즌 Stage04
→ 작품 완료검사
→ 작품 ZIP Fresh Extraction 1회
→ DB 증분 편입
```

## 직접독해 질문

각 장면에서 확인한다.

1. 실제 행동
2. 목표·전략·은폐·회피
3. 정보·관계·권력·의존 변화
4. 선택·거부·유예
5. 회차 구조 기능
6. 다음 장면을 미는 잔여 압력

## 회차 산출물

```text
SceneCard
EpisodeMeta
SequenceBlueprint
EpisodeArc
CharacterArc
RelationshipArc
LocalEdge
PayoffCandidate
checkpoint
```

파일이 실제로 저장되기 전에는 완료로 보고하지 않는다.

## Stage01

- SceneCard는 exact 9키를 사용한다.
- 사건 요약이 아니라 행동·전략·변화·선택·구조 기능을 압축한다.
- CORE는 `SCHEMA_CONTRACTS_V2.md`의 16종만 사용한다.
- 원문 복사, 동일 문장 골격, 존재하지 않는 인과를 금지한다.

## Stage02

- SequenceBlueprint exact 18키.
- 목표·장애·가치·행동 계획·POV·장소·극적 방향 변화로 경계를 둔다.
- 모든 장면은 정확히 한 시퀀스에 포함한다.
- 누락·중복 0, span·budget 일치, runtime 합 1.0.

## EpisodeArc·Stage03

- EpisodeArc는 실제 entry→turning point→exit 변화를 기록한다.
- CharacterArc는 실제 상태 변화가 있는 인물만 기록한다.
- RelationshipArc는 양쪽 인물이 실제 접촉한 관계 변화만 기록한다.
- LocalEdge는 같은 회차의 반사실 인과만 허용한다.
- PayoffCandidate는 구체적인 장거리 plant 가능성만 기록한다.
- 고정 수량은 없다.

## 회차 최소 구조검사

회차마다 한 번만 실행한다.

```text
parse
exact keyset·type
ID 중복
SceneCard coverage
Sequence partition·span·budget·runtime
Arc·Edge reference
LocalEdge same episode/gap0
필수 파일 존재
```

의미를 다시 채점하지 않는다. 결과는 단일 checkpoint에 기록한다.

## Stage04

모든 회차 Stage01~03 저장 후 한 번 수행한다.

- PayoffCandidate disposition 100%
- 실제 장거리 plant/payoff만 CrossEpisodeEdge 승격
- 자동 회차 브리지 금지
- FullSeriesArc 작성

## 작품 완료검사

전 시즌 완료 후 한 번만 실행한다.

```text
전 회차 Stage01~03 존재
ID·FK 무결성
CandidateDisposition 100%
CrossEpisodeEdge 유효
FullSeriesArc counts 일치
작품 ZIP
Fresh Extraction 1회
```

## 기본에서 제거

- QuarterAudit 의무
- 회차별 다수 증빙 JSON
- 여러 checkpoint
- 반복 checksum
- 약 8회차 강경검사
- 회차·블록·전 시즌 중복 validator
- 회차별 ZIP/Fresh Extraction
- 중복 validation registry
- 작품마다 전체 DB 새 릴리즈

위 항목은 원본 불일치, 직접독해 누락 의심, 템플릿 반복, Edge 과밀, Provider 충돌, SourceLock 불일치, 정본 교체, 사용자 요청 때만 포렌식으로 사용한다.

## GPT·Claude 공동 규격

공통:

- 원본 직접독해
- 회차 순차 처리
- exact Stage01~04 schema
- 동일 ID·enum·FK
- SourceLock Core
- 단일 checkpoint
- LocalEdge 동일 회차
- CandidateDisposition 100%
- Provider provenance

어느 Provider도 자동 상위가 아니며 사용자 승인으로 공동 `CANONICAL`이 된다.

## EXT6

`EXT6_DISABLED_BY_DEFAULT`.

사용자 명시 지시 또는 별도 교차비교·연구 작업에서만 실행한다.

## 릴리즈 동결

- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 새 Governance 번호·전체 DB ZIP·release manifest는 사용자 명시 지시가 있을 때만 만든다.
- 문서 변경, validator 변경, 작품 한 편 추가만으로 릴리즈 번호를 올리지 않는다.

## 최소 보고

```text
작품 / 완료 회차 / current pointer / 저장 Stage / 구조검사 / 차단 오류
```

## 권위

1. `SCHEMA_CONTRACTS_V2.md`
2. `START_HERE_NEW_DRAMA_ANALYSIS.md`
3. 이 문서
4. 작품 SourceLock·checkpoint
5. 과거 playbook·incident 문서

충돌 시 현재 간소화 정책이 우선한다.
