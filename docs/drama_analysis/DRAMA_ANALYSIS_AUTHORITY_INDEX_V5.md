# 드라마 분석 권위 인덱스 v5

- 상태: `AUTHORITATIVE / CURRENT`
- 갱신: `2026-07-18`
- 문서·DB 릴리즈 번호 자동 증가 금지

## 새 대화창 필수 로드

1. `START_HERE_NEW_DRAMA_ANALYSIS.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. 최신 DB 전체 작품 인덱스
4. 재개 작업이면 작품별 단일 checkpoint

## 권위 우선순위

| 순위 | 영역 | 문서 |
|---:|---|---|
| 1 | exact keyset·enum·ID·FK | `SCHEMA_CONTRACTS_V2.md` |
| 2 | 현재 실행·검증·릴리즈 정책 | `START_HERE_NEW_DRAMA_ANALYSIS.md` |
| 3 | 압축 실행 순서 | `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` |
| 4 | machine-readable 정책 | `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` |
| 5 | 작품 실행 상태 | SourceLock Core·단일 checkpoint |
| 6 | 과거 상세 사례·incident | 필요할 때만 부분 조회 |

과거 문서가 QuarterAudit, 약 8회차 강검사, 반복 validator, 매 작품 새 DB 릴리즈를 기본 의무로 요구하면 현재 START_HERE 정책이 우선한다.

## 현재 실행

```text
Q1→Q4 원본 직접독해
→ 회차 Stage01~03 직접 저작
→ 정본 저장
→ 최소 구조검사 1회
→ 단일 checkpoint
→ 다음 회차
→ 전 시즌 Stage04
→ 작품 완료검사
→ 작품 ZIP Fresh Extraction 1회
→ DB 증분 편입
```

## 기본에서 제외

- QuarterAudit 의무
- 회차별 다수 증빙 JSON
- 여러 checkpoint
- 반복 checksum
- 약 8회차 의무 강경검사
- 회차·블록·전 시즌 중복 validator
- 회차별 ZIP·Fresh Extraction
- 중복 validation registry
- 작품마다 전체 DB 새 릴리즈

위 항목은 원본 불일치, 직접독해 누락 의심, 템플릿 반복, Edge 과밀, Provider 충돌, SourceLock 불일치, 정본 교체, 사용자 요청 때만 포렌식으로 실행한다.

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

작품당 Core 한 파일만 기본 유지한다. 장면별·Quarter별 상세 해시는 사고 작품에서만 확장한다.

## EXT6

`EXT6_DISABLED_BY_DEFAULT`.

사용자 명시 요청 또는 별도 교차비교·연구 작업에서만 실행한다.

## DB 릴리즈 동결

- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 새 Governance 번호·전체 DB ZIP·release manifest는 사용자 명시 지시가 있을 때만 만든다.
- 문서·validator 변경 또는 작품 한 편 추가만으로 릴리즈 번호를 올리지 않는다.

## 최소 보고

```text
작품 / 완료 회차 / current pointer / 저장 Stage / 구조검사 / 차단 오류
```

실제 저장되지 않은 진행을 보고하지 않는다.
