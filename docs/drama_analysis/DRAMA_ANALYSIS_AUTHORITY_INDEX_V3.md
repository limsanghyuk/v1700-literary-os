# 드라마 분석 권위 인덱스 v3

- Document ID: `DRAMA-ANALYSIS-AUTHORITY-INDEX-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Version: `3.4`
- Date: 2026-07-16
- Scope: 원본 직접독해, Stage01~04, 앙상블 추적, 블록 실행, 데이터베이스 편입, 문자열·경로 검증, 계보·세션 안전

## 1. 목적

분산된 exact schema, 직접독해, 장편 블록 실행, 검증, 계보, 원본 저장, 문자열 인코딩, 세션 안전과 최신 작품 상태를 연결한다. 새 대화창은 과거 대화를 전수 조사하지 않고 최소 권위 문서만 읽고 분석을 재개할 수 있어야 한다.

## 2. 새 대화창 최소 로드

```text
README.md
→ DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md
→ SCHEMA_CONTRACTS_V2.md
→ DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json
→ DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md
```

## 3. 권위 순서

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset, type, enum, ID, FK, invariants
2. `DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md` — 현재 실행 단위·DB 삽입·EXT6 보류
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md` — 신규 세션 통합 실행
4. `DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md` — 직접독해·블록 속도·장편 토큰 관리·SourceLock·중단 복구
5. `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md` — 앙상블 폭·LocalEdge 선별·후보 처분
6. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 내용 깊이
7. `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md` — 구조·내용·반게이밍·Stage04·패키지 검증
8. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — SourceLock·QuarterAudit·quarantine·supersession·ZIP·허브 편입
9. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 세션 한도·영속화·중단 복구
10. `EXT6_DEFERRED_SIDECAR_POLICY_V1.md` — EXT6/HXT6 보류·보존
11. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json` — 최신 51작품 DB 상태
12. 최신 `docs/sessions/*drama*/README.md` — 산출물·SHA·validation·handoff

## 4. 기본 파이프라인

```text
source inventory
→ original_extracted/{작품명}/ UTF-8 TXT 저장
→ SourceLock
→ episode Q1→Q4 Stage01
→ Stage02 SequenceBlueprint·EpisodeArc
→ Stage03 CharacterArc·RelationshipArc·LocalEdge·PayoffCandidate
→ episode light gate
→ approximately 8-episode block strong validation
→ full Stage01~03 validation
→ Stage04 100% candidate disposition
→ CrossEpisodeEdge·FullSeriesArc
→ independent ZIP
→ seqcard_ko insertion
→ full DB validation·ZIP fresh extraction
```

## 5. 고정 규칙

- Python 의미 생성 금지
- 기존 정상 자산은 유지하고 결함 범위만 재저작
- 기존 SceneCard는 색인, 원본은 최종 증거
- 의미 저작 최소 단위 quarter
- 원자 잠금 단위 episode
- 전달·강검증 기본 단위 약 8 episodes
- 매 회차 의미 강검증 반복 금지
- Stage03 회차별 수직 처리
- 변화 없는 인물·관계 수량 채우기 금지
- LocalEdge 동일 회차·gap 0
- 회차 간 연결은 Stage04 CrossEpisodeEdge
- PayoffCandidate disposition 100%
- 자동 회차 경계 브리지 0
- 사후 일괄 QuarterAudit 금지
- 사용자 승인 전 CANONICAL 금지
- ZIP 한글 경로는 UTF-8 flag 필수
- 정본 텍스트는 UTF-8, U+FFFD 0을 릴리스 게이트로 적용

## 6. 데이터베이스 디렉터리 권위

```text
seqcard_ko/                              의미 데이터·규격 문서
seqcard_ko/original_extracted/{work}/   회차별 UTF-8 TXT
seqcard_ko/source_lock/                  단일 SourceLock 루트
seqcard_ko/AUTHORED_WORK_INDEX_V7.json  51작품 분석 계층 전수 인덱스
tools/                                   실행 검증기
validation/                              검증 결과·휴대형 검증기
upgrade_audit/                           감사·이전 판본·lineage
provenance/                              원본 입수·변환 이력
```

`seqcard_ko` core에는 Python·ZIP·TMP·BAK·LOG를 두지 않는다. `_quarantine`, 독립 `docs`, 독립 `quarter_audits`, 독립 `source_alignment`, 중복 `source_lock`은 core에 두지 않는다. EXT6/HXT6 관련 `_ext6_audit`은 유지한다.

## 7. 현재 데이터베이스

```text
artifact: seqcard_ko_developer_release_51works_50complete_utf8_repaired_v7.zip
SHA256: 8a27d901d7122a1d9aebcadde459864adffd56c31553931327652744662e851f
works: 51
episodes: 970
SceneCard: 60,875
authored files: 1,994
analysis-layer files: 7,790
Stage01~04 complete: 50
remaining: 최강칠우 / SOURCE_HOLD_EXPERIMENTAL
canonical promoted works: 14
```

```text
ZIP CRC PASS
fresh extraction PASS
SHA256 ledger 9,742 / mismatch 0
filename mojibake 0
invalid UTF-8 0
U+FFFD files 0
JSON/JSONL parse errors 0
analysis files missing versus V6 0
errors 0 / warnings 0
```

V6은 한글 ZIP 경로 인코딩 결함으로 superseded 처리한다. 분석 파일은 삭제되지 않았으며 V4→V5/V6에서 제거된 11개는 비정본 build·dump·temporary·cache 파일이다.

대용량 DB ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 artifact name, SHA256, count, validation, lineage, handoff만 기록한다.

## 8. 개와늑대의시간 레거시 보강

16회 숫자행 EpisodeArc를 원본 TXT·SceneCard·SequenceBlueprint 직접 검토를 거친 exact ARC13으로 교체했다.

```text
episodes 16
scenes 880
sequences 143
ARC13 16/16
legacy numeric remaining in canonical 0
legacy numeric preserved for lineage 16
Python semantic generation false
errors 0 / warnings 0
```

상세 기록:

```text
docs/sessions/2026-07-16-drama-db-clean-tree-wolf-arc13/README.md
docs/sessions/2026-07-16-drama-db-v7-utf8-repair/README.md
```

## 9. 권위 상태

```text
STAGE01_04_SCHEMA: AUTHORITATIVE
NEW_SESSION_EXECUTION_GUIDE: AUTHORITATIVE_CANDIDATE
DIRECT_READING_BLOCK_SUPPLEMENT: AUTHORITATIVE_CANDIDATE
ENSEMBLE_EDGE_POLICY: AUTHORITATIVE_CANDIDATE
VALIDATION_GATES: AUTHORITATIVE_CANDIDATE
DATABASE_DIRECTORY_STANDARD: AUTHORITATIVE_CANDIDATE
UTF8_PATH_AND_TEXT_GATE: AUTHORITATIVE_CANDIDATE
EXT6_HXT6_DEFAULT: DEFERRED_DISABLED_PRESERVED
DATABASE_STATUS: INTEGRATED_VALIDATED_50_OF_51_V7
CANONICAL_PROMOTION: USER_APPROVED_14_WORKS_UNCHANGED
```
