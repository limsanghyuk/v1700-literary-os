# 드라마 분석 권위 인덱스 v3

- Document ID: `DRAMA-ANALYSIS-AUTHORITY-INDEX-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Version: `3.5`
- Date: 2026-07-16
- Scope: 원본 직접독해, Stage01~04, 앙상블 추적, 블록 실행, 데이터베이스 편입, UTF-8·검증 거버넌스, SourceLock·계보·세션 안전

## 1. 목적

분산된 exact schema, 직접독해, 장편 블록 실행, 검증, 계보, 원본 저장, 문자열 인코딩, 재개 가능한 릴리스 상태와 최신 작품 상태를 연결한다. 새 대화창은 과거 대화를 전수 조사하지 않고 최소 권위 문서만 읽고 분석과 데이터베이스 운영을 재개할 수 있어야 한다.

## 2. 새 대화창 최소 로드

```text
README.md
→ DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md
→ SCHEMA_CONTRACTS_V2.md
→ DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json
→ DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md
→ docs/sessions/2026-07-16-drama-db-governance-v8/README.md
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
11. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json` — 최신 51작품 V8 DB 상태
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
→ process A: validation-only
→ validation/current/release_gate.json
→ process B: package-only
→ fresh extraction·actual CLI rerun
→ external final validation certificate
```

## 5. 고정 규칙

- Python 의미 생성 금지
- 기존 정상 자산은 유지하고 결함 범위만 재저작
- 기존 SceneCard는 색인, 원본은 최종 증거
- 의미 저작 최소 단위 quarter
- 원자 잠금 단위 episode
- 전달·강검증 기본 단위 약 8 episodes
- Stage03 회차별 수직 처리
- LocalEdge 동일 회차·gap 0
- 회차 간 연결은 Stage04 CrossEpisodeEdge
- PayoffCandidate disposition 100%
- 자동 회차 경계 브리지 0
- 사후 일괄 QuarterAudit 금지
- ZIP 비 ASCII 경로 UTF-8 flag 필수
- 정본 텍스트 UTF-8·U+FFFD 0
- 검증 실패 시 exit code 1, 실행·사용 오류 시 exit code 2
- 사용자 승인 전 CANONICAL 금지

## 6. V8 데이터베이스 디렉터리 권위

```text
seqcard_ko/                                  의미 데이터·규격 문서
seqcard_ko/original_extracted/{work}/       회차별 UTF-8 TXT
seqcard_ko/source_lock/current/              51작품 current lock/inventory
seqcard_ko/source_lock/INDEX.json            SourceLock registry
seqcard_ko/AUTHORED_WORK_INDEX_V8.json       51작품 분석 계층 인덱스
tools/current/                               package-relative current validators
tools/history/                               non-authoritative historical validators
validation/current/                          one current global release gate set
validation/works/{work}/current.json         51 work current fan-in
validation/history/                          superseded/component evidence
upgrade_audit/                               감사·이전 판본·lineage
provenance/                                  원본 입수·변환 이력
release_state/                               재개 가능한 상태 전이
```

## 7. 현재 데이터베이스

```text
artifact: seqcard_ko_developer_release_51works_50complete_governance_v8.zip
SHA256: a0249986653b330b309aded67b6c7e52aa977eecaab2f8d53ad79d36639e099a
size: 49,085,365 bytes
ZIP entries: 9,976
works: 51
episodes: 970
SceneCard: 60,875
analysis-layer files: 7,790
Stage01~04 complete: 50
remaining: 최강칠우 / SOURCE_HOLD_EXPERIMENTAL
validation coverage: 51/51
SourceLock coverage: 51/51
canonical promoted works: 14 unchanged
```

```text
fresh extraction PASS
actual CLI rerun PASS
SHA256 ledger 9,975 / missing 0 / mismatch 0
filename mojibake 0
non-ASCII paths without UTF-8 flag 0
invalid UTF-8 0
U+FFFD files 0
pre/post tree missing 0 / extra 0 / hash mismatch 0
errors 0 / warnings 0
```

SourceLock 51개는 contemporaneous/legacy evidence를 정규화한 16개와 retroactive inventory 35개로 구성된다. retroactive inventory는 `direct_reading_attested:false`이며 과거 직접독해 증거를 소급 창작하지 않는다.

## 8. V8 구조 마이그레이션

회차 간 LocalEdge 114건을 의미 문구 변경 없이 CrossEpisodeEdge로 이동했다.

```text
affected works: 8
records migrated: 114
affected local files: 97
remaining cross-episode LocalEdge: 0
meaning_text_changed: false
python_semantic_generation: false
```

대상은 `구르미그린달빛`, `내이름은김삼순`, `미생`, `배가본드`, `비밀의숲`, `스토브리그`, `신사의품격`, `커피프린스`다.

## 9. 릴리스 상태 모델

```text
TREE_READY
→ VALIDATION_IN_PROGRESS
→ VALIDATION_PASS
→ PACKAGE_IN_PROGRESS
→ PACKAGE_BUILT
→ FRESH_EXTRACTION_PASS
→ RELEASE_READY
```

ZIP 내부 checkpoint는 아티팩트 생성 시점의 `PACKAGE_BUILT_PENDING_FRESH_EXTRACTION`을 유지한다. 외부 최종 검증 인증서와 작업 트리 checkpoint가 post-ZIP 검증 및 `RELEASE_READY`를 인증한다.

## 10. 권위 상태

```text
STAGE01_04_SCHEMA: AUTHORITATIVE
NEW_SESSION_EXECUTION_GUIDE: AUTHORITATIVE_CANDIDATE
DIRECT_READING_BLOCK_SUPPLEMENT: AUTHORITATIVE_CANDIDATE
ENSEMBLE_EDGE_POLICY: AUTHORITATIVE_CANDIDATE
VALIDATION_GATES: AUTHORITATIVE_CANDIDATE
DATABASE_DIRECTORY_STANDARD: AUTHORITATIVE_CANDIDATE
UTF8_PATH_AND_TEXT_GATE: AUTHORITATIVE_CANDIDATE
VALIDATION_GOVERNANCE_V8: AUTHORITATIVE_CANDIDATE
SOURCE_LOCK_REGISTRY_V8: AUTHORITATIVE_CANDIDATE
EXT6_HXT6_DEFAULT: DEFERRED_DISABLED_PRESERVED
DATABASE_STATUS: RELEASE_READY_50_OF_51_V8
CANONICAL_PROMOTION: USER_APPROVED_14_WORKS_UNCHANGED
```
