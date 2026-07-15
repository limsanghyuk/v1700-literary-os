# 드라마 분석 권위 인덱스 v3

- Document ID: `DRAMA-ANALYSIS-AUTHORITY-INDEX-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Version: `3.2`
- Date: 2026-07-15
- Scope: 원본 직접독해, Stage01~04, 앙상블 추적, 데이터베이스 편입, 검증·계보·세션 안전

## 1. 목적

분산된 exact schema, 직접독해, 검증, 계보, 세션 안전, 작품 상태를 연결하고 새 대화창이 과거 대화 전체를 읽지 않고 즉시 분석을 실행하도록 권위와 최소 로드 세트를 고정한다.

## 2. 새 대화창 최소 로드

```text
README.md
→ DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md
→ SCHEMA_CONTRACTS_V2.md
→ DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json
```

위 네 문서로 실행을 시작할 수 있다. 나머지는 충돌 해결·정밀 감사·중단 복구 시 참조한다.

## 3. 권위 순서

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset, type, enum, ID, FK, invariants
2. `DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md` — 실행 단위, DB 삽입, EXT6 보류
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md` — 신규 세션 통합 실행 순서
4. `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md` — 앙상블 폭, LocalEdge 선별, 후보 전수 처분
5. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 직접독해·내용 깊이
6. `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md` — 구조·내용·반게이밍·Stage04·패키지 검증
7. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — SourceLock, QuarterAudit, quarantine, supersession, ZIP, 허브 편입
8. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 세션 한도, 영속화, 중단 복구
9. `EXT6_DEFERRED_SIDECAR_POLICY_V1.md` — EXT6 현재 보류
10. `DRAMA_STAGE_EXT6_CONTRACT_MATRIX_V3.md` — EXT6 재활성화 시 보존 계약
11. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json` — 현재 49작품, 44완료, 5잔여
12. 최신 `docs/sessions/*drama*/README.md` — 작업 산출물·SHA·다음 진입점

## 4. 기존 자산과의 관계

- Stage01~04 exact schema는 변경하지 않는다.
- 새 실행 가이드는 기존 운영·마스터·검증 문서를 실행 순서로 통합한다.
- 앙상블 정책은 Stage03 레코드 폭을 넓히지만 키를 추가하지 않는다.
- 스토브리그의 인물·관계 폭은 채택한다.
- 스토브리그의 과도한 LocalEdge·인접 연결·미처리 후보는 채택하지 않는다.
- EXT6은 Stage01~04 파일에 필드를 추가하지 않는 비활성 sidecar다.

## 5. 기본 파이프라인

```text
source inventory
→ SourceLock
→ episode Q1→Q4 Stage01
→ episode Stage02
→ EpisodeArc
→ ensemble CharacterArc·RelationshipArc
→ selective LocalEdge·PayoffCandidate
→ episode gate·checkpoint
→ full Stage01~03 validation
→ Stage04 100% candidate disposition
→ CrossEpisodeEdge·FullSeriesArc
→ independent ZIP
→ seqcard_ko insertion
→ full DB validation·ZIP
```

## 6. 고정 규칙

- Python 의미 생성 금지
- 의미 저작 최소 단위 quarter
- 원자 범위 1회차
- 전달 블록 8회차
- Stage04는 전 작품 Stage01~03 검증 후 수행
- 앙상블 변화 누락 금지
- 변화 없는 인물·관계 수량 채우기 금지
- 회차 간 LocalEdge 0
- 인접 장면 자동 연결 금지
- PayoffCandidate disposition 100%
- 자동 회차 경계 브리지 0
- 사용자 승인 전 CANONICAL 금지

## 7. 현재 데이터베이스

```text
works: 49
episodes: 938
SceneCard: 58,945
Stage01~04 complete: 44
remaining upgrades: 5
canonical promoted works: 14
```

최신 artifact:

```text
seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_theking_newheart_killme_whitetower_mawang_skycastle_gung_kain_sign_sandglass_v1.zip
SHA256 f79e1962348216197ccf9687a5881c99621f42ad0693ccfc6ad580aba69c521e
```

## 8. CANONICAL 승격

사용자 명시 승인과 작품별 강검증 통과에 따라 다음 14작품을 CANONICAL로 승격한다.

```text
W, 경성스캔들, 미안하다사랑한다, 밀회,
더킹투하츠, 뉴하트, 킬미힐미, 하얀거탑,
마왕, 스카이캐슬, 궁, 카인과아벨, 싸인, 모래시계
```

## 9. 잔여 작품과 재진입

```text
공주의남자: 정상 후보
녹두꽃: 정상 후보
역전의여왕: Stage02 재저작·31회 블록
최강칠우: SOURCE_HOLD, 실제 EP03 필요
대장금: 최종 순서, 54회·8회차 블록
```

다음 진입점:

```text
DATABASE_STATUS
→ SELECT_ONE_ELIGIBLE_WORK
→ SOURCE_PREFLIGHT
→ EP01_Q1_OR_REQUIRED_REAUTHOR_POINT
→ FULL_STAGE01_03_VALIDATION
→ STAGE04_FAN_IN
→ INDEPENDENT_ZIP
→ DATABASE_ZIP_UPDATE
```

## 10. 권위 상태

```text
STAGE01_04_SCHEMA: AUTHORITATIVE
NEW_SESSION_EXECUTION_GUIDE: AUTHORITATIVE_CANDIDATE
ENSEMBLE_EDGE_POLICY: AUTHORITATIVE_CANDIDATE
CURRENT_OPERATING_SUPPLEMENT: AUTHORITATIVE_CANDIDATE
CLOSE_READING_PROTOCOL: AUTHORITATIVE_CANDIDATE
VALIDATION_GATES: AUTHORITATIVE_CANDIDATE
EXT6_DEFAULT: DEFERRED_DISABLED
DATABASE_STATUS: INTEGRATED_VALIDATED_PROGRESS_44_OF_49
CANONICAL_PROMOTION: USER_APPROVED_14_WORKS
```
