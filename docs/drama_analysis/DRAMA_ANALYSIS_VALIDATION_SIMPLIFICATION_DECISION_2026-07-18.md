# 드라마 분석 검증 간소화·릴리즈 동결 결정

- 상태: `AUTHORITATIVE DECISION`
- 결정일: `2026-07-18`
- 적용: GPT·Claude 공동 드라마 분석

## 배경

현재의 QuarterAudit, 블록 강검사, 다중 checkpoint, 반복 checksum, 중복 validator는 GPT가 대본 직접독해·Stage 저작·실제 저장을 누락하거나 미완료 상태를 완료로 보고한 사고를 막기 위해 단계적으로 추가되었다.

개별 안전장치는 유효했지만 모든 정상 작품에 의무 적용되면서 다음 역효과가 발생했다.

```text
직접독해·의미 저작보다 검증·증빙·패키징 비용 증가
→ 세션·실행 한도 소진
→ 새 대화창 이동·재학습 증가
→ 분석 중단과 오류 가능성 증가
```

따라서 의미 저작의 본체와 사고 대응용 포렌식을 분리한다.

## 유지

- 원본 직접독해
- 회차 순차 처리
- Stage01~04 exact schema
- SceneCard·Sequence coverage
- ID·FK·enum 무결성
- 실제 변화만 Arc 기록
- LocalEdge 동일 회차·반사실 인과
- CandidateDisposition 100%
- SourceLock Core
- 작품별 단일 checkpoint
- 작품 완료 후 ZIP Fresh Extraction 1회
- Provider provenance
- 사용자 승인 CANONICAL

## 기본에서 제거

- Q별 QuarterAudit
- 회차별 다수 증빙 JSON
- 여러 checkpoint
- 반복 checksum
- 약 8회차 의무 강검사
- 회차·블록·전 시즌 중복 validator
- 회차별 ZIP·Fresh Extraction
- 중복 validation registry
- 신규 작품마다 기존 DB 전체 재검증
- 작품마다 새 전체 DB 릴리즈

## 조건부 포렌식

다음 상황에서만 과거 강검사 도구를 사용한다.

- 원본과 산출물 불일치
- 직접독해 누락·자동 생성 의심
- 동일 문장 골격 대량 반복
- LocalEdge 과밀·자동 인접 연결
- GPT·Claude 동일 작품 충돌
- SourceLock 해시 불일치
- 정본 교체·스키마 마이그레이션
- 사용자 요청

## 새 기본 실행

```text
Q1→Q4 직접독해
→ 해당 회차 Stage01~03 직접 저작
→ 정본 저장
→ 최소 구조검사 1회
→ 단일 checkpoint
→ 다음 회차
```

전 시즌:

```text
PayoffCandidate 전수 검토
→ CandidateDisposition 100%
→ CrossEpisodeEdge
→ FullSeriesArc
→ 작품 완료검사 1회
→ 작품 ZIP
→ Fresh Extraction 1회
→ DB 증분 편입
```

## SourceLock

작품당 Core 한 파일만 기본 유지한다. 장면별 hash·Quarter별 hash·원문 offset·판본 정렬표는 사고 작품에서만 확장한다.

## GPT·Claude 공동 규격

통일:

- Stage01~04 exact schema
- ID·enum·FK
- SourceLock Core
- 단일 checkpoint
- Edge 계층
- CandidateDisposition
- 정본 상태와 provenance

통일하지 않음:

- 내부 프롬프트
- 독해 메모
- 세션 분할
- Provider 고유 보조 분석
- 문장 스타일

## EXT6

`EXT6_DISABLED_BY_DEFAULT`.

사용자 명시 요청, GPT×Claude 교차비교, 연구용 고밀도 코퍼스에서만 별도 실행한다.

## 릴리즈 동결

- 작품 완료와 전체 DB 릴리즈 생성을 분리한다.
- 전체 DB ZIP·새 Governance 번호·release manifest는 사용자 명시 지시가 있을 때만 생성한다.
- 문서 변경, validator 변경, 작품 한 편 추가만으로 릴리즈 번호를 올리지 않는다.
- 최신 인증 DB 릴리즈는 사용자 승인 전까지 동결한다.

## 재발 방지

검증 규칙을 기본 의무로 다시 추가하려면 실제 사고, 기존 최소검사로 막을 수 없는 이유, 실행 비용, 조건부 포렌식으로 해결 불가한 이유, 사용자 승인을 제시해야 한다.

현재 실행 권위는 `START_HERE_NEW_DRAMA_ANALYSIS.md`다.
