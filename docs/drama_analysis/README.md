# 드라마 분석 권위 진입점

- 상태: `AUTHORITATIVE ENTRYPOINT / CURRENT`
- 갱신: `2026-07-18`
- 적용: GPT·Claude 공동 분석
- DB 릴리즈: 사용자 명시 승인 전 동결

이 디렉터리는 한국 드라마 원본 직접독해, Stage01~04 저작, SourceLock, 최소 검증, 공동 정본 DB 편입의 단일 진입점이다.

## 현재 전체 DB 인계

- 전체 DB: **63작품 / 1,166회 / 73,018 SceneCard**
- 전 시즌 Stage01~04 완료: **61작품**
- 최신 편입 정본: **우리집 EP01~20**
- Governance 번호 증가: **없음 — V15 기반 증분 스냅샷**
- 인계 문서: `DRAMA_DATABASE_HANDOFF_63WORKS_OUR_HOME_2026-07-18.md`

## 새 대화창 최소 로드

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. 최신 DB 전체 작품 인덱스
4. 재개 작업이면 작품별 단일 checkpoint

압축 실행 가이드:

- `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`

과거 대화 전체, 모든 세션 README, 모든 역사 문서를 시작 전에 전수 조사하지 않는다.

## 권위 우선순위

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
2. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 실행·검증·릴리즈 정책
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` — 압축 실행 순서
4. `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` — machine-readable 정책
5. 작품 SourceLock Core·단일 checkpoint
6. 과거 operating manual·validation·incident 문서

과거 문서가 QuarterAudit, 약 8회차 강검사, 반복 validator, 매 작품 새 DB 릴리즈를 기본 의무로 요구하면 현재 START_HERE 정책이 우선한다.

## 표준 실행

```text
원본 inventory
→ 최신 DB 차집합
→ SourceLock Core
→ EP01 Q1→Q4 직접독해
→ EP01 Stage01~03 직접 저작
→ 정본 저장
→ 최소 구조검사 1회
→ 단일 checkpoint
→ EP02
→ ...
→ 전 시즌 Stage04
→ 작품 완료검사
→ 작품 ZIP Fresh Extraction 1회
→ DB 증분 편입
```

직접독해와 의미 저작이 본 작업이다. 검증은 이를 대신하지 않는다.

## 기본 검증

### 회차

- JSON/JSONL parse
- exact keyset·type
- ID 중복
- SceneCard ordinal coverage
- Sequence partition·span·budget·runtime
- Arc·Edge reference
- LocalEdge same episode/gap 0
- 필수 파일 존재

결과는 단일 checkpoint에 기록한다.

### 작품 완료

- 전 회차 Stage01~03 존재
- CandidateDisposition 100%
- CrossEpisodeEdge·FullSeriesArc 무결성
- 작품 ZIP
- Fresh Extraction 1회

## 기본에서 제거

- QuarterAudit 의무
- 회차별 다수 증빙 JSON
- 여러 checkpoint
- 반복 checksum
- 약 8회차 의무 강검사
- 회차·블록·전 시즌 중복 validator
- 회차별 ZIP·Fresh Extraction
- 중복 validation registry
- 작품마다 전체 DB 새 릴리즈

위 항목은 원본 불일치, 직접독해 누락 의심, 템플릿 반복, Edge 과밀, Provider 충돌, SourceLock 불일치, 정본 교체, 사용자 요청 때만 포렌식으로 사용한다.

## GPT·Claude 공동 정본

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

어느 Provider도 자동 상위가 아니다. 사용자 승인으로 공동 `CANONICAL`이 된다.

## SourceLock

작품당 Core 한 파일만 기본 유지한다. 장면별·Quarter별 상세 증빙은 사고 작품에서만 확장한다.

## EXT6

`EXT6_DISABLED_BY_DEFAULT`.

사용자 명시 지시 또는 별도 교차비교·연구 작업에서만 실행한다.

## 릴리즈 동결

- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 전체 DB ZIP·새 Governance 번호·release manifest는 사용자 명시 지시가 있을 때만 만든다.
- 문서 변경, validator 변경, 작품 한 편 추가만으로 릴리즈 번호를 올리지 않는다.

## 보고

사용자가 중간 보고를 요구하지 않으면 최소 보고만 한다.

```text
작품 / 완료 회차 / current pointer / 저장 Stage / 구조검사 / 차단 오류
```

실제 저장되지 않은 진행은 보고하지 않는다.

## 관련 문서

- `START_HERE_NEW_DRAMA_ANALYSIS.md`
- `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`
- `SCHEMA_CONTRACTS_V2.md`
- `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json`
- `DRAMA_ANALYSIS_AUTHORITY_INDEX_V5.md`
- `DRAMA_ANALYSIS_VALIDATION_SIMPLIFICATION_DECISION_2026-07-18.md`
- `DRAMA_DATABASE_HANDOFF_63WORKS_OUR_HOME_2026-07-18.md`

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 artifact name, SHA256, counts, lineage, handoff만 기록한다.
