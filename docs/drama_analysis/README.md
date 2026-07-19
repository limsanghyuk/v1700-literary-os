# 드라마 분석 권위 진입점

- 상태: `AUTHORITATIVE ENTRYPOINT / CURRENT`
- 갱신: `2026-07-19`
- 적용: GPT·Claude 공동 분석
- DB 릴리즈: 사용자 명시 승인 전 동결

이 디렉터리는 한국 드라마 원본 직접독해, Stage01~04 저작, SourceLock, 최소 검증, 공동 정본 DB 편입의 단일 진입점이다.

## 현재 전체 DB 인계

- 전체 DB: **64작품 / 1,182회 / 74,078 SceneCard**
- 전 시즌 Stage01~04 완료: **62작품**
- 최신 편입 정본: **수호천사 EP01~16**
- 사용자 승인 정본: **20작품**
- Governance 번호 증가: **없음 — V15 기반 증분 스냅샷**
- 최신 인계 문서: `DRAMA_DATABASE_HANDOFF_64WORKS_SUHO_CHUNSA_2026-07-18.md`

## 새 대화창 최소 로드

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. `DRAMA_ANALYSIS_SEMANTIC_QUALITY_LESSONS_2026-07-19.md`
4. 최신 DB 전체 작품 인덱스
5. 재개 작업이면 작품별 단일 checkpoint

압축 실행 가이드:

- `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`

과거 대화 전체, 모든 세션 README, 모든 역사 문서를 시작 전에 전수 조사하지 않는다.

## 권위 우선순위

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
2. `START_HERE_NEW_DRAMA_ANALYSIS.md` — 현재 실행·검증·릴리즈 정책
3. `DRAMA_ANALYSIS_SEMANTIC_QUALITY_LESSONS_2026-07-19.md` — 의미 품질·재발 방지 상세
4. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` — 압축 실행 순서
5. `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` — machine-readable 정책
6. 작품 SourceLock Core·단일 checkpoint
7. 과거 operating manual·validation·incident 문서

과거 문서가 QuarterAudit, 반복 강검사, 반복 validator, 매 작품 새 DB 릴리즈를 기본 의무로 요구하면 현재 정책이 우선한다.

## 표준 실행

```text
원본 inventory·전체 회차 경계 선확정
→ 최신 DB 차집합
→ SourceLock Core
→ EP01 Q1→Q4 직접독해
→ EP01 Stage01~03 직접 저작
→ 정본 저장
→ 최소 구조검사 1회
→ 단일 checkpoint
→ 다음 회차를 순서대로 연속 처리
→ 전체의 약 50% 지점에서 의미검사·보강 1회
→ 교정 규칙을 후반부에 적용
→ 마지막 회차까지 연속 처리
→ 전 시즌 의미검사 1회
→ 전 시즌 Stage04
→ 작품 완료검사
→ 작품 ZIP Fresh Extraction 1회
→ DB 증분 편입
→ 사용자 요청 시 전체 DB 호환 ZIP 1회
```

직접독해와 의미 저작이 본 작업이다. 검증은 이를 대신하지 않는다.

중간의 약 50% 의미검사는 과거의 회차별·8회차별 반복 강검사와 다르다. 작품당 한 번만 수행하며, 전반부에서 발견한 원문 불일치·템플릿 반복·Arc 남발·LocalEdge 과밀·PayoffCandidate 오류를 보강하여 후반부에 재발하지 않게 하는 의미 캘리브레이션이다.

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

### 작품 중간 50% 의미 게이트

- 원문 대비 title·intent 정확성
- exact semantic duplicate
- masked skeleton·동일 종결 템플릿
- CharacterArc trigger participant
- RelationshipArc 양쪽 participant·역방향 중복
- 앙상블 변화 누락
- LocalEdge 반사실 인과·과밀·인접 편향
- PayoffCandidate 구체 근거·중복·회차 내 해결
- 문제 레코드 보강 후 후반부 진행

### 작품 완료

- 전 회차 Stage01~03 존재
- 전 시즌 의미검사 PASS
- CandidateDisposition 100%
- CrossEpisodeEdge·FullSeriesArc 무결성
- 작품 ZIP
- Fresh Extraction 1회

## 기본에서 제거

- QuarterAudit 의무
- 회차별 다수 증빙 JSON
- 여러 checkpoint
- 반복 checksum
- 회차별·다중 블록별 반복 강검사
- 회차·블록·전 시즌 중복 validator
- 회차별·블록별 ZIP·Fresh Extraction
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

Claude의 의미 증거 밀도·앙상블 폭·다축 관계 분석·인과 중간 메커니즘을 수용하되, 최종 스키마·ID·FK·패키징은 동일 계약으로 정규화한다.

## SourceLock

작품당 Core 한 파일만 기본 유지한다. 작품 분석 전에 전체 회차 경계·인코딩·장면 번호 정책을 먼저 잠근다. 장면별·Quarter별 상세 증빙은 사고 작품에서만 확장한다.

## 압축 호환 정책

전체 DB ZIP은 다음을 기본으로 한다.

- 짧은 ASCII archive root
- 실제 Unicode 파일명과 UTF-8 filename flag
- standard ZIP Deflate
- 암호화 없음
- 분할 압축 없음
- 내부 경로 길이 260자 미만 목표
- system unzip test
- 전체 Fresh Extraction
- SHA ledger 검증

## EXT6

`EXT6_DISABLED_BY_DEFAULT`.

사용자 명시 지시 또는 별도 교차비교·연구 작업에서만 실행한다.

## 릴리즈 동결

- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 전체 DB ZIP·새 Governance 번호·release manifest는 사용자 명시 지시가 있을 때만 만든다.
- 문서 변경, validator 변경, 작품 한 편 추가만으로 Governance 번호를 올리지 않는다.

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
- `DRAMA_ANALYSIS_SEMANTIC_QUALITY_LESSONS_2026-07-19.md`
- `DRAMA_ANALYSIS_VALIDATION_SIMPLIFICATION_DECISION_2026-07-18.md`
- `DRAMA_DATABASE_HANDOFF_64WORKS_SUHO_CHUNSA_2026-07-18.md`
- `DRAMA_DATABASE_HANDOFF_63WORKS_OUR_HOME_2026-07-18.md` — 이전 스냅샷 기록

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 artifact name, SHA256, counts, lineage, handoff만 기록한다.
