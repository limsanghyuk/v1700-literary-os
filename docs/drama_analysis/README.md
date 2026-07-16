# 드라마 분석 권위 인덱스

Document status: **AUTHORITATIVE ENTRYPOINT / V3 CANDIDATE BRANCH**  
Version: 3.5-candidate  
Updated: 2026-07-16 (Asia/Seoul)

이 디렉터리는 한국 드라마 원본을 직접 읽어 Stage01~04 분석 산출물을 만들고, 검증된 결과를 `seqcard_ko` 데이터베이스에 편입하는 권위 문서군의 단일 진입점이다.

## 1. 새 대화창 최소 시작 세트

1. 이 `README.md`
2. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md`
3. `SCHEMA_CONTRACTS_V2.md`
4. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json`
5. `DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md`
6. 최신 세션 핸드오프 `docs/sessions/2026-07-16-drama-db-governance-v8/README.md`

## 2. 권위 순서

1. `SCHEMA_CONTRACTS_V2.md` — Stage01~04 exact schema·enum·ID·FK·불변식
2. `DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md` — 현재 작업 단위·DB 삽입·EXT6 보류
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md` — 새 대화창 실행 절차
4. `DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md` — 직접독해·블록 속도·중단 복구·SourceLock
5. `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md` — 앙상블 폭·LocalEdge 선별·후보 전수 처분
6. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 직접독해·내용 깊이
7. `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md` — fail-closed 강검증
8. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — SourceLock·계보·ZIP·허브 편입
9. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 세션 한도·체크포인트·중단 복구
10. `EXT6_DEFERRED_SIDECAR_POLICY_V1.md` — EXT6/HXT6 보류·보존
11. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json` — 최신 DB 상태
12. 최신 `docs/sessions/*drama*/README.md` — 산출물·SHA·validation·handoff

## 3. 기본 파이프라인

```text
original_extracted/{작품명}/ 원본 TXT 저장
→ SourceLock
→ 회차 Q1→Q4 직접독해
→ Stage01 SceneCard
→ Stage02 SequenceBlueprint·EpisodeArc
→ Stage03 CharacterArc·RelationshipArc·LocalEdge·PayoffCandidate
→ 회차 경량 게이트
→ 약 8회차 블록 강검증
→ 전 시즌 Stage01~03 강검증
→ Stage04 후보 100% disposition
→ CrossEpisodeEdge·FullSeriesArc
→ 독립 ZIP
→ DB 삽입
→ 전체 DB validator
→ ZIP fresh extraction·실제 CLI 재실행
```

## 4. 고정 운영 규칙

- Python·템플릿 의미 생성 금지
- 기존 정상 자산은 유지하고 의미 결함 범위만 재저작
- 기존 SceneCard는 색인, 원본은 최종 증거
- Stage03는 회차별 수직 처리
- LocalEdge는 동일 회차·gap 0만 허용
- 회차 간 연결은 Stage04 CrossEpisodeEdge만 사용
- PayoffCandidate disposition 100%
- 이전 회 마지막→다음 회 첫 장면 자동 브리지 0
- QuarterAudit 사후 일괄 생성 금지
- ZIP 한글 경로 UTF-8 flag 필수
- 정본 텍스트 UTF-8·U+FFFD 0
- 사용자 승인 전 CANONICAL 금지

## 5. V8 디렉터리 표준

```text
seqcard_ko/                                  의미 데이터·규격 문서
seqcard_ko/original_extracted/{작품명}/     작품별 UTF-8 TXT
seqcard_ko/source_lock/current/              51작품 current lock/inventory
seqcard_ko/source_lock/INDEX.json            51작품 SourceLock registry
seqcard_ko/AUTHORED_WORK_INDEX_V8.json       51작품 분석 계층 전수 인덱스
tools/current/                               현행 범용 검증기
tools/history/                               비권위 역사 검증기
validation/current/                          단일 최신 전역 결과
validation/works/{작품}/current.json         51작품 current fan-in
validation/history/                          구버전·component 증빙
upgrade_audit/                               감사·이전 판본·lineage
provenance/                                  원본 입수·변환 이력
release_state/                               재개 가능한 상태 전이
```

## 6. 현재 데이터베이스 상태

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
CANONICAL promoted: 14 unchanged
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

SourceLock coverage는 기존 직접독해 증빙 16작품과 `direct_reading_attested:false`인 retroactive source inventory 35작품으로 구성된다. 과거 직접독해 증거를 소급 창작하지 않는다.

## 7. V8 구조 마이그레이션

현행 계약을 위반하던 회차 간 LocalEdge 114건을 의미 문구 변경 없이 CrossEpisodeEdge로 이동했다.

```text
affected works: 8
records migrated: 114
affected local files: 97
remaining cross-episode LocalEdge: 0
meaning_text_changed: false
python_semantic_generation: false
```

대상: `구르미그린달빛`, `내이름은김삼순`, `미생`, `배가본드`, `비밀의숲`, `스토브리그`, `신사의품격`, `커피프린스`.

## 8. 상태·권한

V8은 `PASS_CANDIDATE_GOVERNANCE_NORMALIZED / RELEASE_READY`다. `최강칠우`의 작품 검증 PASS는 구조·레지스트리 정합성 PASS이며 작품 분류는 계속 `SOURCE_HOLD_EXPERIMENTAL`이다.

사용자 명시 승인에 따른 기존 CANONICAL 14작품은 변경하지 않았다. EXT6/HXT6은 `DEFERRED_OPTIONAL_SIDECAR`로 보존한다.

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 파일명·SHA·count·validation·lineage·handoff만 기록한다.
