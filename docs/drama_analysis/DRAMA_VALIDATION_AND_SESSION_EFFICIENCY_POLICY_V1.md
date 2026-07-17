# 드라마 분석 검증·세션 효율 정책 v1

- Document ID: `DRAMA-VALIDATION-SESSION-EFFICIENCY-POLICY-V1`
- Status: `AUTHORITATIVE`
- Updated: 2026-07-17
- Incident basis: `굿캐스팅` EP09~16 execution

## 1. 확인된 문제

`굿캐스팅` 후반부 작업에서 원문 직접독해와 의미 초안은 EP09~16까지 완료됐지만 정본 JSON/JSONL 직렬화 이전에 세션이 중단된 것처럼 보였다. 실제 병목은 의미 분석 속도가 아니라 다음 운영 방식이었다.

1. 회차마다 강검증 항목을 반복 실행
2. 의미 초안→Python module→JSONL의 이중 직렬화
3. SourceLock 전체 해시·중복·인물·관계·Edge 선택성을 매 회차 재검사
4. 강검증·패키징·Fresh extraction을 하나의 장기 실행에 결합
5. 새 대화창마다 권위 문서와 과거 세션을 전수 재학습
6. 이미 검증된 전체 DB를 신규 작품 편입 때마다 작품별로 전수 재검증

결과적으로 같은 데이터를 반복 읽어 세션 실행 한도와 컨텍스트를 소비했다.

## 2. 원인 판정

```text
ROOT_CAUSE = VALIDATION_SCOPE_OVERLAP
SECONDARY = REPEATED_ONBOARDING
SECONDARY = DOUBLE_SERIALIZATION
SECONDARY = NON_INCREMENTAL_DATABASE_VALIDATION
```

원본 손상, 의미 초안 소실, 디스크 부족이 원인이 아니었다.

## 3. 검증 계층 재분리

### Episode Light Gate

구조와 재개 가능성만 검사한다.

- parse
- exact schema·ID
- SceneCard coverage
- Sequence partition·runtime sum
- trigger·reference existence
- LocalEdge same-episode/gap0
- checkpoint·next pointer

### Half-season / 8-episode Strong Gate

의미 품질과 전역 선택성을 검사한다.

- exact/masked repetition
- Stage02 grounding
- ensemble omission
- relationship reverse duplicate
- LocalEdge density·adjacency·counterfactual causality
- PayoffCandidate duplication
- block ID/FK consistency

### Full-series Gate

- Stage01~03 full integration
- Stage04 candidate disposition 100%
- selective CrossEpisodeEdge
- FullSeriesArc

### Package Gate

- checksum
- ZIP CRC
- fresh extraction
- pre/post tree comparison

각 항목은 자기 계층에서 한 번만 실행한다.

## 4. 실행 한도 보호

- 의미 저작은 한 회차씩 한다.
- deterministic serialization/light validation은 최대 4회차 묶음 허용.
- strong validation은 전반부/약 8회차 뒤 한 번.
- 패키징은 validation PASS 뒤 별도 프로세스.
- Fresh extraction은 최종 ZIP 한 번.
- 실패 시 기존 tree를 지우지 않고 checkpoint부터 재개.

## 5. 새 대화창 온보딩

필수 로드는 두 문서로 제한한다.

1. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md`
2. `SCHEMA_CONTRACTS_V2.md`

신규 작품 선택 시 최신 DB status/index를 하나 추가하고, 중단 재개 시 작품 checkpoint JSON을 하나 추가한다. 나머지 문서는 reference-only다.

다음 행동은 금지한다.

```text
모든 과거 대화 읽기
모든 세션 README 읽기
모든 방법론 문서 전수 요약
작업 시작 전 허브 전체 검색 반복
```

## 6. DB 증분 검증

이전 릴리스가 다음을 만족하면 immutable validated base로 계승한다.

- ZIP SHA256 고정
- 외부 Fresh Extraction 검증서 존재
- pre/post tree mismatch 0
- current registries PASS

신규 작품 편입 시:

```text
previous certified release
+ new work validator
+ new SourceLock
+ full registry/source/encoding/database/release gates
+ final fresh extraction
```

이전 의미 파일이 바뀌지 않았으면 기존 작품별 의미 validator 53개를 다시 실행하지 않는다. 이전 tree 변경, SHA 불일치, validator contract 변경, 증빙 부재 중 하나가 있을 때만 full revalidation한다.

## 7. 증빙 경량화

운영 DB 본체는 검색·개발에 필요한 current evidence만 유지한다.

- SourceLock current
- validation work current
- aggregate hashes
- original independent package SHA
- lineage/provenance report

대량 raw evidence는 독립 작품 패키지 또는 history archive에 보존한다. 운영 DB의 `quarter_audits/`, `direct_reading_evidence/`는 기본 제외한다.

이 정책은 직접독해 증거를 폐기하는 것이 아니라 저장 계층을 분리하는 것이다.

## 8. 상태 판정

```text
EPISODE_LIGHT_PASS
BLOCK_STRONG_PASS
FULL_STAGE01_03_PASS
STAGE04_PASS
PACKAGE_BUILT
FRESH_EXTRACTION_PASS
RELEASE_READY
```

채팅 보고가 아니라 파일·checkpoint·validator exit code가 상태 권위다.

## 9. 적용 결과 — 굿캐스팅/V10

- `굿캐스팅`: 16회 Stage01~04 완료
- SceneCard 1,020
- SequenceBlueprint 117
- CharacterArc 128
- RelationshipArc 128
- LocalEdge 93
- PayoffCandidate 152
- CrossEpisodeEdge 48
- CandidateDisposition 152/152
- 신규 작품 validation errors 0 / warnings 0
- V10: 54작품 / 1,018회 / 63,941 SceneCard
- 전역 encoding/source/registry/database/release gate PASS
- Fresh extraction PASS
- 운영 DB bulk direct-reading evidence directory 0

## 10. 승격 규칙

이 정책과 `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md`가 실행 cadence에 관해 V1 guide, V3 validation 문서의 모호하거나 더 무거운 회차별 규칙보다 우선한다. Exact schema는 계속 `SCHEMA_CONTRACTS_V2.md`가 우선한다.
