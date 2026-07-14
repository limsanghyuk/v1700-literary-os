# 드라마 분석 권위 인덱스 v3

- Document ID: `DRAMA-ANALYSIS-AUTHORITY-INDEX-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Date: 2026-07-15
- Scope: 한국 드라마 원본 직접독해, Stage01~04, 데이터베이스 편입, 검증·계보·세션 안전, EXT6 별도 sidecar

## 1. 목적

드라마 분석 관련 규범이 기존 exact schema 계약, 직접독해 운영 문서, EXT6 파일럿, 작품별 체크포인트와 데이터베이스 작업에 분산되어 있었다. 이 인덱스는 각 문서의 권위와 적용 순서를 연결하고, 새 대화창이 즉시 다음 작품을 분석·업그레이드하도록 현재 상태를 고정한다.

## 2. 권위 순서

1. `docs/drama_analysis/SCHEMA_CONTRACTS_V2.md`
   - Stage01~04 exact keyset, enum, ID, FK, 불변식의 최상위 권위.
2. `docs/drama_analysis/DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md`
   - 8회차 블록, 작품 내부 품질검증, 데이터베이스 삽입, EXT6 기본 보류에 대한 현재 운영 결정.
3. `docs/drama_analysis/DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md`
   - 원본 직접독해 방식, Q1→Q4, 내용 깊이, Stage별 저작 순서.
4. `docs/drama_analysis/DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md`
   - 구조·내용·반게이밍·Stage04·패키지 검증. EXT6 Gate는 활성 run에서만 적용.
5. `docs/drama_analysis/DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md`
   - SourceLock, QuarterAudit, quarantine, supersession, ZIP, 허브·DB 편입.
6. `docs/drama_analysis/DRAMA_SESSION_EXECUTION_SAFETY_V1.md`
   - 세션 한도, 영속화 경계, 작업공간 정리, 재시작 규칙.
7. `docs/drama_analysis/EXT6_DEFERRED_SIDECAR_POLICY_V1.md`
   - EXT6의 현재 보류 상태와 재활성화 조건.
8. `docs/drama_analysis/DRAMA_STAGE_EXT6_CONTRACT_MATRIX_V3.md`
   - EXT6 파일럿을 다시 활성화할 경우의 보존 계약.
9. `docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json`
   - 현재 49작품 데이터베이스·34작품 완료·15작품 잔여 상태.
10. 최신 `docs/sessions/*drama*/README.md`
   - 작업 산출물·SHA·보강 이력·다음 진입점.

## 3. 기존 자산과의 관계

- `SCHEMA_CONTRACTS_V2.md`의 Stage01~04 exact schema는 변경하지 않는다.
- v3 문서는 exact schema를 확장하지 않고 직접독해·검증·세션 안전·계보를 강화한다.
- Issue #60의 Stage1/2 co-authoring quality gate 핵심을 승계한다.
- EXT6은 Stage01~04 파일에 필드를 추가하지 않는 sidecar다.
- EXT6은 현재 기본 비활성·보류이며 Stage01~04 완료 조건이 아니다.
- CharacterVoice·MotifLedger·ThematicStance·AffectRegister 등은 별도 계약·ablation 전까지 실험 계층이다.

## 4. 기본 운영 파이프라인

```text
원본 archive inventory
→ SourceLock v2
→ 회차 Q1→Q2→Q3→Q4 Stage01 직접독해
→ 회차 전체 Stage02 재통합
→ Stage03 직접 저작
→ 회차 강한 게이트
→ 회차 체크포인트 영속화
→ 8회차 블록 통합 게이트
→ 전 회차 Stage01~03 전수 강검증
→ Stage04 PayoffCandidate 전수 fan-in
→ FullSeriesArc
→ 독립 작품 ZIP
→ seqcard_ko 데이터베이스 직접 삽입
→ 전체 DB ZIP 검증
```

EXT6은 이 기본 파이프라인에 포함하지 않는다. 명시적으로 활성화한 별도 파일럿에서만 sidecar로 수행한다.

## 5. 고정 규칙

- 동일 SourceLock과 동일 canonical scene boundary.
- exact keyset·자료형·enum·ID·FK는 v2 계약 준수.
- Python 의미 생성 금지.
- 의미 저작 최소 단위 quarter.
- 한 실행의 원자 범위 1회차.
- 개발자 전달 블록 8회차.
- Stage04는 전 작품 Stage01~03 강검증 후 수행.
- 기존 작품과의 교차품질 비교는 선택 사항.
- 사용자 승인 전 `CANONICAL` 금지.

## 6. 현재 데이터베이스 상태

```text
works: 49
episodes: 938
SceneCard: 58,945
Stage01~04 complete: 34
remaining upgrades: 15
```

최신 데이터베이스 artifact:

```text
seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_v1.zip
SHA256 fbcff3f8d184d4d36a4364fe8caca14b3591ae0c8b64b07ebccfaf2564b3ad6c
```

오늘 신규 삽입: `칼잡이오수정`, `드림`, `강남엄마따라잡기`  
오늘 Stage04 업그레이드: `W`, `경성스캔들`, `미안하다사랑한다`, `밀회`

## 7. 권위 상태

```text
STAGE01_04_SCHEMA: AUTHORITATIVE
CURRENT_OPERATING_SUPPLEMENT: AUTHORITATIVE_CANDIDATE
CLOSE_READING_PROTOCOL_V3: AUTHORITATIVE_CANDIDATE
VALIDATION_GATES_V3: AUTHORITATIVE_CANDIDATE
EXT6_DEFAULT: DEFERRED_DISABLED
EXT6_SCHEMA: PRESERVED_EXPERIMENTAL_SIDECAR
DATABASE_STATUS: INTEGRATED_VALIDATED_PROGRESS
CANONICAL_PROMOTION: USER_APPROVAL_REQUIRED
```

## 8. 다음 진입점

```text
DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json
→ SELECT_ONE_REMAINING_WORK
→ SOURCE_AND_EXISTING_STAGE_PREFLIGHT
→ EP01_Q1_OR_NEXT_REQUIRED_EPISODE
→ FULL_STAGE01_03_VALIDATION
→ STAGE04_FAN_IN
→ INDEPENDENT_ZIP
→ DATABASE_ZIP_UPDATE
```
